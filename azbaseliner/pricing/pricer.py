import logging
from logging import Logger
from dataclasses import dataclass
import requests
import os
import json


@dataclass
class MonthlyPlanPricing:
    """Holds pricing information retured by the pricing API"""

    meterId: str
    regionName: str
    currency: str
    ri3y: float = float("NaN")
    ri1y: float = float("NaN")
    sp3y: float = float("NaN")
    sp1y: float = float("NaN")


class PricingAPIConstants(object):
    """'Holds constants for usage of the pricing API"""

    API_ENDPOINT: str = "https://prices.azure.com/api/retail/prices"
    API_VERSION: str = "api-version=2023-01-01-preview"
    API_CALL_HEADERS: dict = {"Content-Type": "application/json"}

    KEY_TERM: str = "term"
    VALUE_TERM_3YEARS: str = "3 Years"
    VALUE_TERM_1YEAR: str = "1 Year"

    KEY_RESERVATION_TERM: str = "reservationTerm"
    KEY_METER_ID: str = "meterId"
    KEY_SAVINGS_PLAN: str = "savingsPlan"
    KEY_UNIT_PRICE: str = "unitPrice"
    KEY_ITEMS: str = "Items"

    QUERY_PARAM_CURRENCY_CODE: str = "currencyCode"
    QUERY_PARAM_CURRENCY_VALUE_EUR: str = "EUR"
    QUERY_FILTER: str = "$filter"
    QUERY_PARAM_REGION: str = "armRegionName"
    QUERY_PARAM_CURRENCY_CODE: str = "currencyCode"

    HOURS_IN_MONTH: int = 730


class PricingAPIClient(object):
    """Handles the pricing lookup via the Azure pricing API"""

    logger: Logger = logging.getLogger("PricingAPIClient")

    @classmethod
    def _buildQueryFilter(ctx, regionName: str, meterIds: list) -> str:
        """builds the OOD query filter for a given region and a set of meter ids"""
        oodFilterString: str = PricingAPIConstants.QUERY_PARAM_REGION + " eq '" + regionName + "' and "
        doAppend: bool = False
        for meterId in meterIds:
            if doAppend:
                oodFilterString = oodFilterString + " or "
            oodFilterString = oodFilterString + PricingAPIConstants.KEY_METER_ID + " eq '" + meterId + "'"
            doAppend = True

        ctx.logger.debug(f"query filter : {oodFilterString}")
        return oodFilterString

    @classmethod
    def _buildQueryUrl(ctx, currencyCode=PricingAPIConstants.QUERY_PARAM_CURRENCY_VALUE_EUR) -> str:
        """builds the query url for a given currency code"""
        url: str = PricingAPIConstants.API_ENDPOINT + "?" + PricingAPIConstants.API_VERSION + "&" + PricingAPIConstants.QUERY_PARAM_CURRENCY_CODE + "=" + currencyCode
        ctx.logger.debug(f"query url : {url}")
        return url

    @classmethod
    def __dumpResponseForDebug(ctx, data: dict) -> None:
        if os.getenv("AZB_DUMP_REST_PAYLOADS") is not None:
            with open("capture.json", "w") as f:
                json.dump(data, f)

    @classmethod
    def _execAPICall(ctx, queryUrl: str, queryFilters: str) -> dict:
        """executes the REST call to the Azure Pricing API and returns the payload"""
        ctx.logger.info(f"invoking azure pricing api on url {queryUrl}&$filter={queryFilters}")
        url = f"{queryUrl}&{PricingAPIConstants.QUERY_FILTER}={queryFilters}"
        response = requests.get(url, headers=PricingAPIConstants.API_CALL_HEADERS)
        if response.ok:
            ctx.logger.info(f"request ok, status code is {response.status_code}")
            data = response.json()
            ctx.__dumpResponseForDebug(data)
            return data
        else:
            ctx.logger.error(f"request failed with status code {response.status_code}")
            return dict()

    @classmethod
    def _parseItemsForMeterId(ctx, meterId: str, regionName: str, currencyCode: str, items: list) -> MonthlyPlanPricing:
        """parses the pricing api response for a given meter id, returns the corresponsing MonthlyPlanPricing record"""
        monthlyPricing: MonthlyPlanPricing = MonthlyPlanPricing(meterId=meterId, regionName=regionName, currency=currencyCode)
        for item in items:
            if PricingAPIConstants.KEY_RESERVATION_TERM in item.keys():
                if item[PricingAPIConstants.KEY_RESERVATION_TERM] == PricingAPIConstants.VALUE_TERM_3YEARS:
                    monthlyPricing.ri3y = round(float(item[PricingAPIConstants.KEY_UNIT_PRICE]) / 3 / 12, 2)
                if item[PricingAPIConstants.KEY_RESERVATION_TERM] == PricingAPIConstants.VALUE_TERM_1YEAR:
                    monthlyPricing.ri1y = round(float(item[PricingAPIConstants.KEY_UNIT_PRICE]) / 12, 2)
            if PricingAPIConstants.KEY_SAVINGS_PLAN in item.keys():
                itemsSP = item[PricingAPIConstants.KEY_SAVINGS_PLAN]
                for itemSP in itemsSP:
                    if PricingAPIConstants.KEY_TERM in itemSP.keys():
                        if itemSP[PricingAPIConstants.KEY_TERM] == PricingAPIConstants.VALUE_TERM_3YEARS:
                            monthlyPricing.sp3y = round(float(itemSP[PricingAPIConstants.KEY_UNIT_PRICE]) * PricingAPIConstants.HOURS_IN_MONTH, 2)
                        if itemSP[PricingAPIConstants.KEY_TERM] == PricingAPIConstants.VALUE_TERM_1YEAR:
                            monthlyPricing.sp1y = round(float(itemSP[PricingAPIConstants.KEY_UNIT_PRICE]) * PricingAPIConstants.HOURS_IN_MONTH, 2)

        return monthlyPricing

    @classmethod
    def _groupRecordsByMeterId(ctx, items: list) -> dict:
        """groups all records by meterId in a given dict"""
        mapPerMeterId: dict = dict()
        for item in items:
            meterId: str = item[PricingAPIConstants.KEY_METER_ID]
            if meterId not in mapPerMeterId.keys():
                mapPerMeterId[meterId] = list()
            mapPerMeterId[meterId].append(item)
        return mapPerMeterId

    @classmethod
    def _getPricingRecords(ctx, regionName: str, currencyCode: str, mapRecordsPerMeterId: dict) -> list:
        """parses records for each and every meterId and returns the corresponing plan pricing record"""
        pricingItems: list = list()
        for meterId in mapRecordsPerMeterId.keys():
            meterIdItems = mapRecordsPerMeterId[meterId]
            pricingItems.append(ctx._parseItemsForMeterId(meterId, regionName, currencyCode, meterIdItems))
        return pricingItems

    @classmethod
    def getOfferMonthlyPriceForMeterIdList(ctx, regionName: str, meterIds: list, currencyCode=PricingAPIConstants.QUERY_PARAM_CURRENCY_VALUE_EUR) -> list:
        """Queries the pricing offers for a list of meter Ids. Returns a list of MonthlyPlanPricing records, one by requested meter Id"""
        responseData: dict = ctx._execAPICall(ctx._buildQueryUrl(currencyCode), ctx._buildQueryFilter(regionName, meterIds))
        mapRecordsPerMeterId: dict = ctx._groupRecordsByMeterId(responseData[PricingAPIConstants.KEY_ITEMS])
        return ctx._getPricingRecords(regionName, currencyCode, mapRecordsPerMeterId)
