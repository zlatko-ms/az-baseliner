Feature: example acceptance test

  Scenario: ensure the integer additions are correctly computed by the calculator
     Given a valid calculator
      When adding "12" and "30" using that calculator
      Then the calculator returns result value "42"



