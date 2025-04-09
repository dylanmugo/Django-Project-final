from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
import json
from .models import Club, Ticket
from .forms import TicketForm, RegistrationForm

# Utility functions for role checking
def is_support_agent(user):
    return user.groups.filter(name='SupportAgent').exists()

def is_escalation_manager(user):
    return user.groups.filter(name='EscalationManager').exists()

def is_support_supervisor(user):
    return user.groups.filter(name='SupportSupervisor').exists()

def is_billing_specialist(user):
    return user.groups.filter(name='BillingSpecialist').exists()

# -------------------- Public Views --------------------

def home_view(request):
    ireland_clubs = Club.objects.filter(league='LI')
    context = {
        'league_of_ireland_clubs': ireland_clubs,
    }
    return render(request, 'FanSupport/home.html', context)

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'FanSupport/create_ticket.html', {'form': form})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    category_filter = request.GET.get('category')
    priority_filter = request.GET.get('priority')

    if category_filter:
        tickets = tickets.filter(category=category_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)

    context = {
        'tickets': tickets,
        'selected_category': category_filter,
        'selected_priority': priority_filter,
    }
    return render(request, 'FanSupport/ticket_list.html', context)

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, 'FanSupport/ticket_detail.html', {'ticket': ticket})

@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != ticket.status:
            old_status = ticket.status
            ticket.status = new_status
            if new_status.lower() == 'resolved':
                ticket.resolved_at = timezone.now()
            else:
                ticket.resolved_at = None
            ticket.save()

            subject = "Your Ticket Status Has Been Updated"
            message = (
                f"Hi {ticket.user.username},\n\n"
                f"Your ticket '{ticket.subject}' status has changed from {old_status} to {ticket.status}.\n\n"
                "Thank you for using our support system."
            )
            from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'no-reply@example.com'
            send_mail(subject, message, from_email, [ticket.user.email], fail_silently=False)

        return redirect('ticket_detail', ticket_id=ticket.id)
    return render(request, 'FanSupport/update_ticket_status.html', {'ticket': ticket})

@login_required
def dashboard(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    status_counts = user_tickets.values('status').annotate(count=Count('status'))
    status_labels = [entry['status'] for entry in status_counts]
    status_data = [entry['count'] for entry in status_counts]

    context = {
        'user_tickets': user_tickets,
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data),
    }
    return render(request, 'FanSupport/dashboard.html', context)

@login_required
def resolved_tickets_by_club(request):
    resolved_tickets = Ticket.objects.filter(user=request.user, resolved_at__isnull=False)
    tickets_by_club = {}
    for ticket in resolved_tickets:
        key = ticket.club if ticket.club else "Unassigned"
        tickets_by_club.setdefault(key, []).append(ticket)

    return render(request, 'FanSupport/resolved_tickets_by_club.html', {'tickets_by_club': tickets_by_club})

# -------------------- Admin & Role-Based Views --------------------

@user_passes_test(is_support_agent)
def support_agent_dashboard(request):
    agent_tickets = Ticket.objects.filter(assigned_to=request.user)
    return render(request, 'FanSupport/roles/agent_dashboard.html', {'agent_tickets': agent_tickets})

@user_passes_test(is_escalation_manager)
def escalation_dashboard(request):
    escalated_tickets = Ticket.objects.filter(status='Escalated')
    return render(request, 'FanSupport/roles/escalation_dashboard.html', {'escalated_tickets': escalated_tickets})

@user_passes_test(is_support_supervisor)
def supervisor_dashboard(request):
    all_tickets = Ticket.objects.all()
    return render(request, 'FanSupport/roles/supervisor_dashboard.html', {'all_tickets': all_tickets})

@user_passes_test(is_billing_specialist)
def billing_dashboard(request):
    billing_related = Ticket.objects.filter(category='billing')
    return render(request, 'FanSupport/roles/billing_dashboard.html', {'billing_related': billing_related})

# -------------------- Auth & Registration --------------------

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            subject = "Welcome to League of Ireland Fan Support"
            message = (
                f"Hi {user.username},\n\n"
                "Thank you for registering at League of Ireland Fan Support. "
                "We're excited to have you on board!\n\n"
                "Best regards,\n"
                "The Fan Support Team"
            )
            from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'no-reply@example.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'FanSupport/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'FanSupport/profile.html')
