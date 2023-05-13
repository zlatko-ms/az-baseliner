from behave import given
from behave import when
from behave import then


@given("a valid calculator")
def step_impl(context):
    pass


@when('adding "{value1}" and "{value2}" using that calculator')
def step_impl(context, value1, value2):
    pass
    # context.result = context.calculator.add(int(value1), int(value2))


@then('the calculator returns result value "{result}"')
def step_impl(context, result):
    pass
    # assert int(context.result) is int(result)
