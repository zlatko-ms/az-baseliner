from behave import given
from behave import when
from behave import then
from azbaseliner.calculator import Calculator


@given('a valid calculator')
def step_impl(context):
    context.calculator = Calculator()


@when('adding "{value1}" and "{value2}" using that calculator')
def step_impl(context, value1, value2):
    context.result = context.calculator.add(int(value1), int(value2))


@then('the calculator returns result value "{result}"')
def step_impl(context, result):
    assert int(context.result) is int(result)
