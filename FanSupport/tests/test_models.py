from django.test import TestCase
from django.contrib.auth.models import User
from FanSupport.models import Club, Ticket

class ClubModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name="Shamrock Rovers",
            stadium="Tallaght Stadium",
            founded="1901-01-01",
            league="LI"
        )

    def test_club_str_representation(self):
        self.assertEqual(str(self.club), "Shamrock Rovers")

class TicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.club = Club.objects.create(name="Dundalk FC", stadium="Oriel Park", league="LI")
        self.ticket = Ticket.objects.create(
            user=self.user,
            club=self.club,
            subject="Test Subject",
            description="Test Description",
            category="general",
            priority="High",
            status="Pending"
        )

    def test_ticket_str_representation(self):
        self.assertEqual(str(self.ticket), "Test Subject")

    def test_ticket_defaults(self):
        self.assertEqual(self.ticket.status, "Pending")
        self.assertIsNone(self.ticket.resolved_at)

    def test_ticket_association(self):
        self.assertEqual(self.ticket.user.username, "tester")
        self.assertEqual(self.ticket.club.name, "Dundalk FC")
