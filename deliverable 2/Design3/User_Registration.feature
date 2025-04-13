Feature: User Registration
  As a new user
  I want to register an account
  So that I can access the Fan Support system

  Scenario: Successful registration
    Given I am on the registration page
    When I enter a valid username "user1", email "user1@example.com", password "password", and confirm "password"
    And I submit the registration form
    Then I should be redirected to the home page
    And I should see a welcome message
    And a welcome email is sent to "user1@example.com"

  Scenario: Registration with missing email
    Given I am on the registration page
    When I enter a valid username "user2", leave the email field blank, enter password "password", and confirm "password"
    And I submit the registration form
    Then I should remain on the registration page
    And I should see an error message "This field is required" next to the email field
