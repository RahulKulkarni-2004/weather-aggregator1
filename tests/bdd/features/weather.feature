Feature: Weather aggregation

  Scenario: Fetch and save weather for a city
    Given the weather provider returns weather for "Belagavi"
    When I fetch weather for "Belagavi"
    Then the response should contain temperature "25.0"
    And the weather should be saved for "Belagavi"

  Scenario: Retrieve weather history for a city
    Given weather data exists for "Belagavi"
    When I request weather history for "Belagavi"
    Then I should receive weather readings for "Belagavi"

  Scenario: Retrieve latest weather for a city
    Given weather data exists for "Belagavi"
    When I request the latest weather for "Belagavi"
    Then the response should contain temperature "25.0"