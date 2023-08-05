# language: en
@kms
Feature: Amazon Key Management Service

  Scenario: Making a request
    When I call the "ListAliases" API
    Then the value at "Aliases" should be a list

  Scenario: Handling errors
    When I attempt to call the "GetKeyPolicy" API with:
    | KeyId      | 12345678-1234-1234-1234-123456789012 |
    | PolicyName | fake-policy                          |
    Then I expect the response error code to be "NotFoundException"
    And I expect the response error to contain a message
