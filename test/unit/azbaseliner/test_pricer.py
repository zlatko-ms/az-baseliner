import unittest
import json
import math
import unittest.mock
from unittest.mock import patch
from azbaseliner.pricing.pricer import PricingAPIClient, MonthlyPlanPricing, PricingAPIConstants


class TestMe(object):
    @classmethod
    def val(ctx) -> int:
        return 42

    @classmethod
    def truc(ctx) -> str:
        return f"value is {ctx.val()}"


class TestPricing(unittest.TestCase):
    currencyCode: str = "EUR"
    regionName = "westeurope"
    fixtureFilePricingResponse = "test/unit/azbaseliner/fixtures/response.pricing.001.json"
    meterIdList = ["f1a44e37-1c48-567c-a0e0-b55263ef5ceb", "ef8e981f-27ae-50ae-9145-a36ec129424e"]

    def loadJsonFile(self, path: str) -> dict:
        with open(path) as fin:
            fixture = json.load(fin)
        return fixture

    def test_001_query_filter(self) -> None:
        meterIdList = ["A", "B"]
        queryFilter: str = PricingAPIClient._buildQueryFilter(self.regionName, meterIdList)
        self.assertEqual(f"armRegionName eq '{self.regionName}' and meterId eq 'A' or meterId eq 'B'", queryFilter)

    def test_002_query_url(self) -> None:
        queryUrl: str = PricingAPIClient._buildQueryUrl(self.currencyCode)
        self.assertEqual(f"https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&currencyCode={self.currencyCode}", queryUrl)

    def test_003_group_records_by_meterid(self) -> None:
        fixture = self.loadJsonFile(self.fixtureFilePricingResponse)
        mapPerMeterId = PricingAPIClient._groupRecordsByMeterId(fixture[PricingAPIConstants.KEY_ITEMS])

        self.assertEqual(len(mapPerMeterId.keys()), 2)
        for meterId in self.meterIdList:
            self.assertTrue(meterId in mapPerMeterId.keys())
            self.assertEqual(len(mapPerMeterId[meterId]), 3)

    def test_004_parse_meterid_items(self) -> None:
        meterId = "f1a44e37-1c48-567c-a0e0-b55263ef5ceb"
        fixture = self.loadJsonFile(f"test/unit/azbaseliner/fixtures/items.meterid.{meterId}.json")
        pricingRecord: MonthlyPlanPricing = PricingAPIClient._parseItemsForMeterId(meterId, self.regionName, self.currencyCode, fixture)
        self.assertEqual(pricingRecord.ri3y, 115.55)
        self.assertEqual(pricingRecord.ri1y, 179.37)
        self.assertEqual(pricingRecord.sp3y, 166.87)
        self.assertEqual(pricingRecord.sp1y, 232.43)
        self.assertEqual(pricingRecord.meterId, meterId)
        self.assertEqual(pricingRecord.regionName, self.regionName)
        self.assertEqual(pricingRecord.currency, self.currencyCode)

    def test_005_get_offer_monthly_price_for_meter_id_list_with_http_mocked(self) -> None:
        # mock the http call return with a json fixture
        with patch.object(PricingAPIClient, "_execAPICall") as mockedMethod:
            fixture = self.loadJsonFile(self.fixtureFilePricingResponse)
            mockedMethod.return_value = fixture
            # perform the test with patched method
            prices: list = PricingAPIClient().getOfferMonthlyPriceForMeterIdList(self.regionName, self.meterIdList, self.currencyCode)
            self.assertEqual(len(prices), len(self.meterIdList))
            for i in range(len(self.meterIdList)):
                price: MonthlyPlanPricing = prices[i]
                self.assertFalse(math.isnan(price.ri1y))
                self.assertFalse(math.isnan(price.ri3y))
                self.assertFalse(math.isnan(price.sp1y))
                self.assertFalse(math.isnan(price.sp3y))
                self.assertEqual(price.currency, self.currencyCode)
                self.assertTrue(price.meterId in self.meterIdList)
                self.assertEqual(price.regionName, self.regionName)
                if price.meterId == "ef8e981f-27ae-50ae-9145-a36ec129424e":
                    self.assertEqual(price.ri3y, 34.66)
                    self.assertEqual(price.ri1y, 53.8)
                    self.assertEqual(price.sp3y, 43.4)
                    self.assertEqual(price.sp1y, 62.19)
                if price.meterId == "f1a44e37-1c48-567c-a0e0-b55263ef5ceb":
                    self.assertEqual(price.ri3y, 115.55)
                    self.assertEqual(price.ri1y, 179.37)
                    self.assertEqual(price.sp3y, 166.87)
                    self.assertEqual(price.sp1y, 232.43)

    # def test_02_call_pricing_api(self) -> None:
    #     regionName = "westeurope"
    #     currencyCode = "EUR"
    #     meterIdList = ["f1a44e37-1c48-567c-a0e0-b55263ef5ceb", "ef8e981f-27ae-50ae-9145-a36ec129424e"]
    #     prices: list = PricingAPIClient.getOfferMonthlyPriceForMeterIdList(regionName, meterIdList, currencyCode)
    #     self.assertEqual(len(prices), len(meterIdList))
    #     for i in range(len(meterIdList)):
    #         price: MonthlyPlanPricing = prices[i]
    #         self.assertFalse(math.isnan(price.ri1y))
    #         self.assertFalse(math.isnan(price.ri3y))
    #         self.assertFalse(math.isnan(price.sp1y))
    #         self.assertFalse(math.isnan(price.sp3y))
    #         self.assertEqual(price.currency, currencyCode)
    #         self.assertEqual(price.regionName, regionName)
    #         self.assertTrue(price.meterId in meterIdList)
    #         print(f"meterId={price.meterId} ri3y={price.ri3y} ri1y={price.ri1y} sp3y={price.sp3y} sp1y={price.sp1y}")
