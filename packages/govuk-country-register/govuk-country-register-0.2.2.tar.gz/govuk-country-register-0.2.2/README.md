# govuk-country-register

Jijna2 filter that uses GOV.UK Registers to look up country codes.

The register data is included in the package so no external requests are required.
This package will be updated when new register data is released.

## Usage

```
import jinja2

from govuk_country_register import to_country

to_country("UK")  # "United Kingdom"

jinja_env = jinja2.Environment()
jinja_env.filters["to_country"] = to_country
```

## Version History

2019-02-12 version 0.2.2

- Fix PyPI readme

2019-02-12 version 0.2.1

- Initial release
