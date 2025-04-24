# Django-Project
Django WFD Project 
League of Ireland Fan Support - Django Web Application

Overview

League of Ireland Fan Support is a multi-role ticketing support system built with Django. The platform is designed to handle support requests from fans across various football clubs in the League of Ireland, and enables role-specific workflows for Support Agents, Escalation Managers, Billing Specialists, and Supervisors.

Features

User Registration & Login: Fans and staff members can securely register and log into their accounts.

Ticket Submission: Users can create support tickets specifying priority, category, and associated club.

Role-Based Dashboards:

Support Agent: View assigned tickets, update status, escalate issues.

Escalation Manager: Manage escalated tickets and assign them to agents.

Support Supervisor: Monitor all ticket activity, assign roles, review agent performance.

Billing Specialist: Focused interface for handling billing-related tickets.

Administrator: Manage user roles and access permissions via an admin dashboard.

Email Notifications: Users receive email alerts when ticket statuses change.

Responsive UI: Built using Bootstrap 5 for seamless experience across devices.

Dynamic Dashboard Visuals: View ticket statuses and trends with interactive Chart.js graphs.

Resolved Tickets Overview: Display resolved tickets grouped by club.

Technology Stack

Backend: Django 5.1.7 (Python 3.10)

Frontend: HTML5, CSS3, Bootstrap 5, Chart.js, Animate.css

Database: SQLite (default)

Installation

Clone the repository:

git clone <your-repo-url>
cd django-project

Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Run the server:

python manage.py runserver

Usage

Access the app at http://127.0.0.1:8000/

Register a user or log in as admin.

Navigate based on your role from the dashboard.

Media & Static Files

Club logos are stored in media/club_logos/

Ensure MEDIA_URL and MEDIA_ROOT are set correctly in settings.py.

Admin Management

Admins can log in via /admin/

Use the built-in interface to assign users to specific groups (roles).

Testing

Manual tests are aligned with Cucumber-style scenarios.

Each use case has at least one defined test.

Future Enhancements

In-app notifications.

Auto-assignment rules for ticket categories.

User feedback and rating system for support responses.
