from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    # Ticket management
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/update_status/', views.update_ticket_status, name='update_ticket_status'),
    path('ticket/<int:ticket_id>/resolve/', views.resolve_ticket, name='resolve_ticket'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tickets/resolved/', views.resolved_tickets_by_club, name='resolved_tickets_by_club'),

    # Auth
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Role-Based Dashboards
    path('support-agent/', views.support_agent_dashboard, name='support_agent_dashboard'),
    path('escalation-manager/', views.escalation_dashboard, name='escalation_manager_dashboard'),
    path('support-supervisor/', views.supervisor_dashboard, name='support_supervisor_dashboard'),
    path('billing-specialist/', views.billing_dashboard, name='billing_specialist_dashboard'),

    # Admin role management
    path('admin/assign-groups/', views.manage_user_roles, name='manage_user_roles'),
]
