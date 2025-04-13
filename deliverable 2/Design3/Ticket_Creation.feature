Feature: Ticket Creation
  As a registered user
  I want to create a new ticket
  So that I can request support for my club

  Scenario: Successful ticket creation
    Given I am logged in as "user1"
    And I am on the "Create Ticket" page
    When I fill in the form with a subject "Issue with Ticketing", description "I cannot purchase a ticket", select "Ticketing" as category, choose "High" priority, and select a club
    And I submit the form
    Then I should be redirected to the ticket list page
    And I should see my new ticket with the subject "Issue with Ticketing"

  Scenario: Ticket creation with missing subject
    Given I am logged in as "user1"
    And I am on the "Create Ticket" page
    When I fill in the form without a subject and complete the other fields
    And I submit the form
    Then I should see an error message "This field is required" near the subject input
