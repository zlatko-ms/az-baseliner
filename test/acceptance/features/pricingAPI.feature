Feature: Getting offer pricing from Azure Pricing API

  Scenario: Pricing API Client gets the correct monhtly pricing for reserved instanced and savings plan
     Given the meter with ids "f1a44e37-1c48-567c-a0e0-b55263ef5ceb" and "ef8e981f-27ae-50ae-9145-a36ec129424e"
      When requesting the information on those meters via the PricingAPICient in "westeurope" region with "EUR" currency 
      Then the client returns exactly "2" pricing records
      And the record for meter "ef8e981f-27ae-50ae-9145-a36ec129424e" indicates "34.66" as the monthly price for the "RI3Y" offer 
      And the record for meter "ef8e981f-27ae-50ae-9145-a36ec129424e" indicates "53.8" as the monthly price for the "RI1Y" offer  
      And the record for meter "ef8e981f-27ae-50ae-9145-a36ec129424e" indicates "43.4" as the monthly price for the "SP3Y" offer
      And the record for meter "ef8e981f-27ae-50ae-9145-a36ec129424e" indicates "62.19" as the monthly price for the "SP1Y" offer  
      And the record for meter "f1a44e37-1c48-567c-a0e0-b55263ef5ceb" indicates "115.55" as the monthly price for the "RI3Y" offer
      And the record for meter "f1a44e37-1c48-567c-a0e0-b55263ef5ceb" indicates "179.37" as the monthly price for the "RI1Y" offer
      And the record for meter "f1a44e37-1c48-567c-a0e0-b55263ef5ceb" indicates "166.87" as the monthly price for the "SP3Y" offer
      And the record for meter "f1a44e37-1c48-567c-a0e0-b55263ef5ceb" indicates "232.43" as the monthly price for the "SP1Y" offer

