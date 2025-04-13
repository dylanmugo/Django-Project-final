Feature: Dashboard Analytics
  As a user
  I want to view a dashboard of my support tickets
  So that I can see a summary and statistics of my tickets

  Scenario: Display ticket status chart on dashboard
    Given I am logged in as "user1"
    And I have multiple tickets with varying statuses
    When I navigate to the dashboard page
    Then I should see a pie chart displaying the number of tickets by status

  Scenario: Display list of tickets on dashboard
    Given I am logged in as "user1"
    When I navigate to the dashboard page
    Then I should see a list of my tickets with subject, category, priority, status, and creation date
