import unittest
import math
from azbaseliner.pricing.pricer import PricingAPIClient, MonthlyPlanPricing


class TestPricingServiceIntegration(unittest.TestCase):
    def assertPriceInRange(self, lower: float, upper: float, collected: float, counterName: str):
        self.assertGreaterEqual(collected, lower, f"expecting {counterName} to be >= then {upper} but found value {collected}")
        self.assertLessEqual(collected, upper, f"expecting {counterName} to be <= then {lower} but found value {collected}")

    def test_001_call_pricing_api_service(self) -> None:
        # given a region, currency code and two meter ids
        regionName = "westeurope"
        currencyCode = "EUR"
        meterA = "f1a44e37-1c48-567c-a0e0-b55263ef5ceb"
        meterB = "ef8e981f-27ae-50ae-9145-a36ec129424e"
        meterIdList = [meterA, meterB]
        # when requesting the offer pricing for the above specified region, currency and meter id list
        prices: list = PricingAPIClient.getOfferMonthlyPriceForMeterIdList(regionName, meterIdList, currencyCode)
        # then we get one record per meter id
        self.assertEqual(len(prices), len(meterIdList))
        for i in range(len(meterIdList)):
            price: MonthlyPlanPricing = prices[i]
            # and all pricing fields have been returned, i.e no NaNs
            self.assertFalse(math.isnan(price.ri1y))
            self.assertFalse(math.isnan(price.ri3y))
            self.assertFalse(math.isnan(price.sp1y))
            self.assertFalse(math.isnan(price.sp3y))
            # and all global fields (currency, region ) are correctly set up
            self.assertEqual(price.currency, currencyCode)
            self.assertEqual(price.regionName, regionName)
            # and there is no records unrelated to our list have been provided
            self.assertTrue(price.meterId in meterIdList)
            # and the pricings are correct for each of the meters
            # note : as the pricing fluctuates over time,  better asses a range then exact value
            if price.meterId == meterA:
                self.assertPriceInRange(118.0, 120.0, price.ri3y, "price.ri3y")
                self.assertPriceInRange(184.0, 186.0, price.ri1y, "price.ri1y")
                self.assertPriceInRange(172.0, 174.0, price.sp3y, "price.sp3y")
                self.assertPriceInRange(238.0, 240.0, price.sp1y, "price.sp1y")
            if price.meterId == meterB:
                self.assertPriceInRange(34.0, 36.0, price.ri3y, "price.ri3y")
                self.assertPriceInRange(55.0, 57.0, price.ri1y, "price.ri1y")
                self.assertPriceInRange(44.0, 46.0, price.sp3y, "price.ri3y")
                self.assertPriceInRange(63.0, 65.0, price.sp1y, "price.sp1y")

    def test_002_multipage_response(self) -> None:
        # gather all pricing for all meterNames starting with DS
        url = "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&currencyCode=EUR&$filter=armRegionName eq 'westeurope' and startswith(meterName,'DS')"
        items: list = PricingAPIClient._execCallAndReturnItems(url)
        # we expect 292 items obtained via 3 pages ( 2x100 items and 1x92 items)
        self.assertEqual(len(items), 292)
