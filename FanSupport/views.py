from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
import json
from .models import Club, Ticket
from .forms import TicketForm, RegistrationForm

# Home Page: Lists only League of Ireland clubs
def home_view(request):
    ireland_clubs = Club.objects.filter(league='LI')
    context = {
        'league_of_ireland_clubs': ireland_clubs,
    }
    return render(request, 'FanSupport/home.html', context)

# Ticket Submission Page: Allows creation of a new ticket
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

# Ticket List Page: Lists all tickets for the logged-in user with filtering options
@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    
    # Retrieve filter parameters from GET request
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

# Ticket Detail Page: Shows details for a single ticket
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, 'FanSupport/ticket_detail.html', {'ticket': ticket})

# Update Ticket Status: Allows updating a ticket's status and sends an email if the status changes
@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != ticket.status:
            old_status = ticket.status
            ticket.status = new_status
            ticket.save()
            # Send email notification to the ticket owner
            subject = "Your Ticket Status Has Been Updated"
            message = (
                f"Hi {ticket.user.username},\n\n"
                f"Your ticket '{ticket.subject}' status has changed from {old_status} to {ticket.status}.\n\n"
                "Thank you for using our support system."
            )
            from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'no-reply@example.com'
            send_mail(subject, message, from_email, [ticket.user.email], fail_silently=False)
        return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        return render(request, 'FanSupport/update_ticket_status.html', {'ticket': ticket})

# Dashboard Page: Displays a chart of ticket statuses and a list of tickets
@login_required
def dashboard(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    # Compute ticket counts by status
    status_counts = user_tickets.values('status').annotate(count=Count('status'))
    
    status_labels = [entry['status'] for entry in status_counts]
    status_data = [entry['count'] for entry in status_counts]

    context = {
        'user_tickets': user_tickets,
        'status_labels': json.dumps(status_labels),  # Convert Python list to JSON string
        'status_data': json.dumps(status_data),
    }
    return render(request, 'FanSupport/dashboard.html', context)

# Registration Page: Allows new users to register and sends a welcome email
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create and save the new user
            login(request, user)  # Log the user in

            # Send a welcome email
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

# Profile Page: Displays the user's profile
@login_required
def profile(request):
    return render(request, 'FanSupport/profile.html')
