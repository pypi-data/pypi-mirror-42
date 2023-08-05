# Specify

A [PHPSpec](https://github.com/phpspec/phpspec)-like for Python. For fun only (for now). If you're looking for a real valid PHPSpec-like, you could check [flowp](http://pawelgalazka.github.io/flowp/testing.html) (but deprecated). [mamba](https://nestorsalceda.com/mamba/) could also interest you, even if it's not exactly what you are searching.

## Install

`pip install specify`

## Usage

You can check the [examples](examples) folder.

```python
from specify import ObjectBehavior
from examples.calculator import Calculator

class CalculatorSpec(ObjectBehavior):
    def _let(self):
        self._describe(Calculator)
        self._be_constructed_with('lorem', id=32)

    def it_adds_the_numbers(self):
        self.add(2, 3)._should_be(5)
```

The command `python -m specify examples/spec/calculator_spec.py` will render a valid TAP output (hopefully).

```
TAP version 13
1..1

ok 1 - CalculatorSpec: it adds the numbers
```

To have a nice and pretty output, you can then use a TAP formatter like [faucet](https://www.npmjs.com/package/faucet).

- **All specifications must start by `it_`.**

- **All spec files must end by `_spec` for now.**

## Builtin matchers

| Matcher                     | Details                 | Alias                           |
| --------------------------- | ----------------------- | ------------------------------- |
| `_should_be`                | check with `is`         | `_should_return`                |
| `_should_be_like`           | check with `==`         | `_should_return_like`           |
| `_should_not_be`            | check with `is not`     | `_should_not_return`            |
| `_should_not_be_like`       | check with `!=`         | `_should_not_return_like`       |
| `_should_be_an_instance_of` | check with `isinstance` | `_should_return_an_instance_of` |
| `_should_have_length`       | check with `len(x)`     |                                 |

## Custom matchers

You can implement a `_matchers` function in your spec, to add custom matchers.

The key of the matcher is left trimmed by `_should_` and the first argument
passed to your function is the value itself.

If you return false, the test will fail.

Here is an example:

```python
class CalculatorSpec(ObjectBehavior):
    # ...

    def it_adds_the_numbers(self):
        self.add(2, 3)._should_be_a_number()
        self.add(2, 3)._should_be_greater_than(10)

    def _matchers(self):
        def be_a_number(value, *args):
            return isinstance(value, int)

        def be_greater_than(value, expected_value):
            return value > expected_value

        return {
            'be_a_number': be_a_number,
            'be_greater_than': be_greater_than
        }
```

## Fluent API

All matchers (builtin and custom) are chainable. Example:

`self.add(2, 3)._should_be_a_number()._should_be(5)._should_be_greater_than(3)`

## Mocks

Thanks to [prophepy](https://github.com/Einenlum/prophepy) (did you get the pun with `prophecy`? Hoho), you can
easily mock things in a [Prophecy](https://github.com/phpspec/prophecy) way.

### Collaborators

Given this `Displayer` class:

```python
from .calculator import Calculator

class Displayer:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def display_addition(self, *args) -> str:
        total = str(self.calculator.add(*args))
        args = [str(arg) for arg in args]

        return f"{' + '.join(args)} = {total}"
```

Here is the spec, mocking the `Calculator`:

```python
from specify import ObjectBehavior, mock
from examples.calculator import Calculator
from examples.displayer import Displayer

class DisplayerSpec(ObjectBehavior):

    @mock(Calculator)
    def _let(self, calculator):
        self._describe(Displayer)
        self._be_constructed_with(calculator)
        self.__calculator = calculator

    def it_displays_addition(self):
        self.__calculator.add(2, 3)._should_be_called()
        self.__calculator.add(2, 3)._will_return(5)
        self.display_addition(2, 3)._should_be_like('2 + 3 = 5')
```

Easy peasy.

### Internal calls to modules

```python
from specify import mock_internal

# ...

@mock_internal('getcwd', lambda : 'loremipsum', from_module='os')
def it_displays_addition(self):
    # ...
    # getcwd() will return 'loremipsum' and will be go back to default after
    the test
```

## TODO

- Handle attributes and not only methods
- Improve the way interal calls are mocked
- Make the tap output a stream as the spec say
- Improve the shitty way specs are loaded for now (maybe use ast like [mamba](https://github.com/nestorsalceda/mamba/blob/8ec25de42171403a3ecf3db4c162053af058f6d7/mamba/example_collector.py#L54)?)
