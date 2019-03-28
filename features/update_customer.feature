Feature: Update customer

  Scenario: An existing customer is updaded
    Given customer "Gene Forsgren" with ID "12345" exists
    When I update the name of customer with an id of "12345" to "Gene Jones"
    Then I should be able to fetch customer details for "Gene Jones"
