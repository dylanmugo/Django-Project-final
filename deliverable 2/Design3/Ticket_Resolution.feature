Feature: Ticket Resolution
  As a user
  I want to mark my ticket as resolved
  So that I know my issue has been addressed

  Scenario: Mark ticket as resolved successfully
    Given I am logged in as "user1"
    And I have a ticket with subject "Issue with Ticketing" in status "Pending"
    When I click the "Mark as Resolved" button on the ticket detail page
    Then the ticket status should change to "Resolved"
    And the resolved timestamp should be set
    And an email notification should be sent to "user1@example.com" confirming the resolution

  Scenario: Trying to mark an already resolved ticket
    Given I am logged in as "user1"
    And I have a ticket with subject "Issue with Ticketing" already in status "Resolved"
    When I visit the ticket detail page
    Then I should not see the "Mark as Resolved" button
