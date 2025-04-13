Feature: Ticket Status Update
  As a user
  I want to update the status of my ticket
  So that I can track the progress of my support request

  Scenario: Update ticket status to "In Progress"
    Given I am logged in as "user1"
    And I have a ticket with subject "Issue with Ticketing" in status "Pending"
    When I navigate to the ticket detail page for that ticket
    And I select "In Progress" from the status dropdown
    And I submit the status update form
    Then the ticket status should change to "In Progress"
    And an email notification should be sent to "user1@example.com" indicating the status change

  Scenario: Attempt to update ticket status without change
    Given I am logged in as "user1"
    And I have a ticket with status "Pending"
    When I navigate to the ticket detail page for that ticket
    And I select "Pending" from the status dropdown
    And I submit the status update form
    Then the ticket status remains "Pending"
    And no email notification is sent
