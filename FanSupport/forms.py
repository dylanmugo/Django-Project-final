from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['club', 'subject', 'description', 'category', 'priority']
        widgets = {
            'club': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your issue', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
