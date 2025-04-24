from django.db import models
from django.contrib.auth.models import User

# League Choices
LEAGUE_CHOICES = [
    ('LI', 'League of Ireland'),
]

# Ticket Priority Levels
PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Urgent', 'Urgent'),
]

# Ticket Categories
CATEGORY_CHOICES = [
    ('ticketing', 'Ticketing'),
    ('merchandise', 'Merchandise'),
    ('general', 'General Inquiry'),
    ('technical', 'Technical Issue'),
    ('billing', 'Billing'),
]

# Ticket Status Choices
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Escalated', 'Escalated'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed'),
]

class Club(models.Model):
    """
    Model representing a football club in the League of Ireland.
    """
    name = models.CharField(max_length=100, help_text="Name of the football club.")
    stadium = models.CharField(max_length=100, blank=True, help_text="Name of the club's stadium.")
    founded = models.DateField(null=True, blank=True, help_text="Date the club was founded.")
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True, help_text="Club logo image.")
    league = models.CharField(max_length=2, choices=LEAGUE_CHOICES, default='LI', help_text="League the club belongs to.")

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """
    Model representing a support ticket created by a user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_tickets',
        help_text="User who submitted the ticket."
    )

    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='club_tickets',
        help_text="Club associated with the ticket."
    )

    subject = models.CharField(max_length=200, help_text="Brief subject of the ticket.")
    description = models.TextField(help_text="Detailed explanation of the issue.")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general',
        help_text="Ticket category."
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Low',
        help_text="Priority level of the ticket."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        help_text="Current status of the ticket."
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        help_text="Support agent assigned to this ticket."
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the ticket was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the ticket was last updated.")
    resolved_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the ticket was resolved.")

    def __str__(self):
        return f"{self.subject} - {self.status}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"
