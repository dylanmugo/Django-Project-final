from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Club, Ticket

admin.site.register(Club)
admin.site.register(Ticket)
