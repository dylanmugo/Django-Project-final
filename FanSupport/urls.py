from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/update_status/', views.update_ticket_status, name='update_ticket_status'),
    path('ticket/<int:ticket_id>/resolve/', views.resolve_ticket, name='resolve_ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tickets/resolved/', views.resolved_tickets_by_club, name='resolved_tickets_by_club'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # ✅ NEW ROLE-BASED DASHBOARDS
    path('support-agent/', views.support_agent_dashboard, name='support_agent_dashboard'),
    path('escalation-manager/', views.escalation_manager_dashboard, name='escalation_manager_dashboard'),
    path('support-supervisor/', views.support_supervisor_dashboard, name='support_supervisor_dashboard'),
    path('billing-specialist/', views.billing_specialist_dashboard, name='billing_specialist_dashboard'),
]
