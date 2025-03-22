from django.db import models
from django.contrib.auth.models import User

LEAGUE_CHOICES = [
    ('PL', 'Premier League'),
    ('LI', 'League of Ireland'),
]

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

class Club(models.Model):
    name = models.CharField(max_length=100)
    stadium = models.CharField(max_length=100, blank=True)
    founded = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    league = models.CharField(max_length=2, choices=LEAGUE_CHOICES, default='PL')

    def __str__(self):
        return self.name

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('ticketing', 'Ticketing'),
        ('merchandise', 'Merchandise'),
        ('general', 'General Inquiry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
