from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Club

class HomeViewTest(TestCase):
    def setUp(self):
        Club.objects.create(name="Test FC", stadium="Test Stadium")

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Test FC")
