import unittest
from azbaseliner.pricing.pricer import PricingAPIClient, MonthlyPlanPricing


class TestPricing(unittest.TestCase):
    def test_00_query_filter(self) -> None:
        regionName = "westeurope"
        meterIdList = ["A", "B"]
        queryFilter: str = PricingAPIClient._buildQueryFilter(regionName, meterIdList)
        self.assertEqual(queryFilter, "armRegionName eq '" + regionName + "' and meterId eq 'A' or meterId eq 'B'")

    def test_01_query_url(self) -> None:
        currencyCode = "EUR"
        queryUrl: str = PricingAPIClient._buildQueryUrl(currencyCode)
        self.assertEqual("https://prices.azure.com/api/retail/prices??api-version=2023-01-01-preview&currencyCode=EUR", queryUrl)

    def test_02_call_pricing_api(self) -> None:
        regionName = "westeurope"
        currencyCode = "EUR"
        meterIdList = ["f1a44e37-1c48-567c-a0e0-b55263ef5ceb", "ef8e981f-27ae-50ae-9145-a36ec129424e"]
        prices: list = PricingAPIClient.getOfferMonthlyPriceForMeterIdList(regionName, meterIdList, currencyCode)
        self.assertEqual(len(prices), len(meterIdList))
        for i in range(len(meterIdList)):
            price: MonthlyPlanPricing = prices[i]
            self.assertNotEqual(price.ri1y, float("NaN"))
            self.assertNotEqual(price.ri3y, float("NaN"))
            self.assertNotEqual(price.sp1y, float("NaN"))
            self.assertNotEqual(price.sp3y, float("NaN"))
            self.assertEqual(price.currency, currencyCode)
            self.assertEqual(price.regionName, regionName)
            self.assertTrue(price.meterId in meterIdList)
