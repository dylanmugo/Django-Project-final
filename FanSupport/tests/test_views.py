from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from FanSupport.models import Ticket, Club

class TicketViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='pass123')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('ticket_list'))
        self.assertRedirects(response, '/accounts/login/?next=/tickets/')

    def test_logged_in_user_can_view_tickets(self):
        self.client.login(username='viewer', password='pass123')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FanSupport/ticket_list.html')


class CreateTicketViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='submitter', password='test123')
        self.club = Club.objects.create(name='Dundalk', stadium='Oriel Park')

    def test_create_ticket_logged_in(self):
        self.client.login(username='submitter', password='test123')
        response = self.client.post(reverse('create_ticket'), {
            'subject': 'New Ticket',
            'description': 'Some issue here.',
            'category': 'general',
            'priority': 'Medium',
            'club': self.club.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ticket.objects.filter(subject='New Ticket').exists())


class UpdateTicketStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='updater', password='pass123')
        self.ticket = Ticket.objects.create(
            user=self.user,
            subject='Escalation Test',
            description='Needs escalation',
            category='general',
            priority='High',
            status='Pending'
        )

    def test_escalate_ticket(self):
        self.client.login(username='updater', password='pass123')
        response = self.client.post(reverse('update_ticket_status', args=[self.ticket.id]), {
            'status': 'Escalated'
        })
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'Escalated')


class AgentDashboardAccessTest(TestCase):
    def setUp(self):
        agent_group = Group.objects.create(name='SupportAgent')
        self.agent = User.objects.create_user(username='agentuser', password='agent123')
        self.agent.groups.add(agent_group)

    def test_agent_dashboard_access(self):
        self.client.login(username='agentuser', password='agent123')
        response = self.client.get(reverse('support_agent_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FanSupport/roles/agent_dashboard.html')
