from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import Group, User
import json

from .models import Club, Ticket
from .forms import TicketForm, RegistrationForm


# -------------------- Utility Role Checkers --------------------
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# -------------------- Public Views --------------------
def home_view(request):
    ireland_clubs = Club.objects.filter(league='LI')
    return render(request, 'FanSupport/home.html', {'league_of_ireland_clubs': ireland_clubs})


@login_required
def create_ticket(request):
    form = TicketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('ticket_list')
    return render(request, 'FanSupport/create_ticket.html', {'form': form})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    category = request.GET.get('category')
    priority = request.GET.get('priority')

    if category:
        tickets = tickets.filter(category=category)
    if priority:
        tickets = tickets.filter(priority=priority)

    return render(request, 'FanSupport/ticket_list.html', {
        'tickets': tickets,
        'selected_category': category,
        'selected_priority': priority,
    })


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'FanSupport/ticket_detail.html', {'ticket': ticket})


@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != ticket.status:
            old_status = ticket.status
            ticket.status = new_status
            ticket.resolved_at = timezone.now() if new_status.lower() == 'resolved' else None
            ticket.save()

            # Notify user by email
            subject = "Your Ticket Status Has Been Updated"
            message = f"Hi {ticket.user.username},\n\nYour ticket '{ticket.subject}' has changed from {old_status} to {ticket.status}."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [ticket.user.email], fail_silently=True)

        return redirect('ticket_detail', ticket_id=ticket.id)

    return render(request, 'FanSupport/update_ticket_status.html', {'ticket': ticket})


@login_required
def resolve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'Resolved'
    ticket.resolved_at = timezone.now()
    ticket.save()
    return redirect('ticket_detail', ticket_id=ticket.id)


@login_required
def dashboard(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    status_counts = user_tickets.values('status').annotate(count=Count('status'))

    return render(request, 'FanSupport/dashboard.html', {
        'user_tickets': user_tickets,
        'status_labels': json.dumps([s['status'] for s in status_counts]),
        'status_data': json.dumps([s['count'] for s in status_counts]),
    })


@login_required
def resolved_tickets_by_club(request):
    resolved_tickets = Ticket.objects.filter(user=request.user, resolved_at__isnull=False)
    tickets_by_club = {}

    for ticket in resolved_tickets:
        club_key = ticket.club or "Unassigned"
        tickets_by_club.setdefault(club_key, []).append(ticket)

    return render(request, 'FanSupport/resolved_tickets_by_club.html', {'tickets_by_club': tickets_by_club})


# -------------------- Role-Based Dashboards --------------------
@user_passes_test(lambda u: in_group(u, 'SupportAgent'))
def support_agent_dashboard(request):
    agent_tickets = Ticket.objects.filter(assigned_to=request.user)
    return render(request, 'FanSupport/roles/agent_dashboard.html', {'agent_tickets': agent_tickets})


@user_passes_test(lambda u: in_group(u, 'EscalationManager'))
def escalation_dashboard(request):
    escalated_tickets = Ticket.objects.filter(status='Escalated')
    return render(request, 'FanSupport/roles/escalation_dashboard.html', {'escalated_tickets': escalated_tickets})


@user_passes_test(lambda u: in_group(u, 'SupportSupervisor'))
def supervisor_dashboard(request):
    all_tickets = Ticket.objects.all()
    return render(request, 'FanSupport/roles/supervisor_dashboard.html', {'all_tickets': all_tickets})


@user_passes_test(lambda u: in_group(u, 'BillingSpecialist'))
def billing_dashboard(request):
    billing_related = Ticket.objects.filter(category='billing')
    return render(request, 'FanSupport/roles/billing_dashboard.html', {'billing_related': billing_related})


# -------------------- Authentication --------------------
def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        send_mail(
            subject="Welcome to League of Ireland Fan Support",
            message=f"Hi {user.username},\n\nThank you for registering.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True
        )
        return redirect('home')
    return render(request, 'FanSupport/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'FanSupport/profile.html')


# -------------------- Admin Group Management --------------------
@staff_member_required
def manage_user_roles(request):
    users = User.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, id=group_id)
        user.groups.clear()
        user.groups.add(group)
        return redirect("manage_user_roles")

    return render(request, "FanSupport/admin/manage_user_roles.html", {
        "users": users,
        "groups": groups,
    })
