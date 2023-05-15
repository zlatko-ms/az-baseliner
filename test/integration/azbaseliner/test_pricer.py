import unittest
import math
from azbaseliner.pricing.pricer import PricingAPIClient, MonthlyPlanPricing


class TestPricingServiceIntegration(unittest.TestCase):
    def test_001_call_pricing_api_service(self) -> None:
        # given a region, currency code and two meter ids
        regionName = "westeurope"
        currencyCode = "EUR"
        meterA = "f1a44e37-1c48-567c-a0e0-b55263ef5ceb"
        meterB = "ef8e981f-27ae-50ae-9145-a36ec129424e"
        meterIdList = [meterA, meterB]
        # when requesting the offer pricing for the above specified region, currency, list of meter ids
        prices: list = PricingAPIClient.getOfferMonthlyPriceForMeterIdList(regionName, meterIdList, currencyCode)
        # then we get one record per meter id
        self.assertEqual(len(prices), len(meterIdList))
        for i in range(len(meterIdList)):
            price: MonthlyPlanPricing = prices[i]
            # ensure all pricing fields have been returned, i.e no NaNs
            self.assertFalse(math.isnan(price.ri1y))
            self.assertFalse(math.isnan(price.ri3y))
            self.assertFalse(math.isnan(price.sp1y))
            self.assertFalse(math.isnan(price.sp3y))
            # ensure global fields (currency, region ) are correctly set up
            self.assertEqual(price.currency, currencyCode)
            self.assertEqual(price.regionName, regionName)
            # ensure that no records unrelated to our list have been provided
            self.assertTrue(price.meterId in meterIdList)
            # ensure the pricing info of the 1st meter id is correct
            if price.meterId == meterA:
                self.assertEqual(price.ri3y, 115.55)
                self.assertEqual(price.ri1y, 179.37)
                self.assertEqual(price.sp3y, 166.87)
                self.assertEqual(price.sp1y, 232.43)
            if price.meterId == meterB:
                self.assertEqual(price.ri3y, 34.66)
                self.assertEqual(price.ri1y, 53.8)
                self.assertEqual(price.sp3y, 43.4)
                self.assertEqual(price.sp1y, 62.19)
