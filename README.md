# Schengen Visa Calculator

This project is intended to help calculate the length of stays for a Schengen "short stay" visa. There is no guarantee that the calculations are correct or that changes to the visa rules will be taken into account.

When in doubt, check the calculation with the calculator of the EU commission: <https://ec.europa.eu/assets/home/visa-calculator/calculator.htm>.

## Usage

You can schengen cryptography with: 

```console
$ pip install git+https://github.com/weddige/schengen.git#egg=schengen
```

The visa calculations can be done like this:

```python
>>> from datetime import date
>>> from schengen import Visa
>>> visa = Visa(date(2020, 1, 1), date(2023, 1, 1))
>>> visa.add_trip(date(2022, 1, 1), date(2022, 2, 1))
>>> visa.evaluate(date(2022, 3, 1))
datetime.timedelta(days=58)
>>>
```
