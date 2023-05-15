from behave import given
from behave import when
from behave import then

from azbaseliner.pricing.pricer import PricingAPIClient, MonthlyPlanPricing


def getPriceMeterId(items: list, meterId: str, region: str, currency: str) -> MonthlyPlanPricing:
    for i in items:
        if i.meterId == meterId:
            return i
    return None


def getOfferPriceFromItem(item: MonthlyPlanPricing, offerCode: str) -> float:
    if offerCode == "RI3Y":
        return item.ri3y
    if offerCode == "RI1Y":
        return item.ri1y
    if offerCode == "SP3Y":
        return item.sp3y
    if offerCode == "SP1Y":
        return item.sp1y
    return None


def assertOfferPricingValue(offer: str, item: MonthlyPlanPricing, expectedRegion: str, expectedCurrency: str, expectedPrice: str) -> None:
    foundPriceValue: float = getOfferPriceFromItem(item, offer)
    expectedPriceValue: float = float(expectedPrice)
    assert float(expectedPriceValue) == foundPriceValue, f"invalid price value for offer {offer}, expected={expectedPriceValue} got={foundPriceValue}"
    assert item.regionName == expectedRegion, f"invalid region name, expected={expectedRegion} got={item.regionName}"
    assert item.currency == expectedCurrency, f"invalid currency code, expected={expectedCurrency} got={item.currency}"


@given('the meter with ids "{meterIdA}" and "{meterIdB}"')
def step_impl(context, meterIdA, meterIdB):
    context.meterIds = [meterIdA, meterIdB]


@when('requesting the information on those meters via the PricingAPICient in "{region}" region with "{currency}" currency')
def step_impl(context, region, currency):
    context.currency = currency
    context.region = region
    context.results = PricingAPIClient.getOfferMonthlyPriceForMeterIdList(region, context.meterIds, currency)


@then('the client returns exactly "{itemCount}" pricing records')
def step_impl(context, itemCount):
    itemsCount: int = len(context.results)
    expectedCount: int = int(itemCount)
    assert itemsCount == expectedCount, f"client did not return the exepected number of records, expecting={expectedCount} got={itemsCount}"


@then('the record for meter "{meterId}" indicates "{price}" as the monthly price for the "{offer}" offer')
def step_impl(context, meterId, price, offer):
    # get pricing from retuned results
    pricingItem: MonthlyPlanPricing = getPriceMeterId(context.results, meterId, context.region, context.currency)
    # assert all values match
    assertOfferPricingValue(offer, pricingItem, context.region, context.currency, price)


# @then('the client returns "{price}" as the 1Y reserved monthly price for meter "{meterId}"')
# def step_impl(context, price, meterId):
#     pricingItem: MonthlyPlanPricing = getPriceMeterId(context.results, meterId, context.region, context.currency)
#     assert pricingItem.ri1y is float(price)


# @then('the client returns "{price}" as the 3Y savings plan monthly price for meter "{meterId}"')
# def step_impl(context, price, meterId):
#     pricingItem: MonthlyPlanPricing = getPriceMeterId(context.results, meterId, context.region, context.currency)
#     assert pricingItem.sp3y is float(price)


# @then('the client returns "{price}" as the 1Y savings plan monthly price for meter "{meterId}"')
# def step_impl(context, price, meterId):
#     pricingItem: MonthlyPlanPricing = getPriceMeterId(context.results, meterId, context.region, context.currency)
#     assert pricingItem.sp1y is float(price)
