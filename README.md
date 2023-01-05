# Vater
[![Build Status](https://travis-ci.org/myslak71/vater.svg?branch=master)](https://travis-ci.org/myslak71/vater)
[![Coverage Status](https://coveralls.io/repos/github/myslak71/vater/badge.svg?branch=master)](https://coveralls.io/github/myslak71/vater?branch=master)
![PyPI](https://img.shields.io/pypi/v/vater?color=blue)
[![Documentation Status](https://readthedocs.org/projects/vater/badge/?version=latest)](https://vater.readthedocs.io/en/latest/?badge=latest)

Python client providing convenient way to access polish VAT payers register API (version 1.3.0).

#### Installation

`pip install vater`

#### Usage

##### Scripts

```
>>> import vater
>>> client = vater.Client(base_url='https://wl-api.mf.gov.pl')
>>> client.search_nip(nip='0000000000')
(
  Subject(
    name='Beastie Boys',
    nip='0000000000',
    status_vat='Czynny',
    regon='111111111',
    pesel=None,
    krs='0000000000',
    residence_address=None,
    working_address='Brooklyn',
    representatives=[],
    authorized_clerks=[],
    partners=[
      Company(
        company_name='Mike D',
        first_name='Michael',
        last_name='Diamond',
        nip=None,
        pesel=None
      )
    ],
    registration_legal_date=datetime.date(2001, 1, 1),
    registration_denial_basis=None,
    registration_denial_date=None,
    restoration_basis=None,
    restoration_date=None,
    removal_basis=None,
    removal_date=None,
    account_numbers=['00000000000000000000000000'],
    has_virtual_accounts=False
  ),
  'z5x71-85a8gl5'
)
```

By default, the data is fetched from today's date,
it can be changed by setting `date` argument:
```
>>> import datetime
>>> client.search_nip(nip='0000000000', date=datetime.date(2001, 1, 1))
```

String may also be passed as a `date`:
```
>>> client.search_nip(nip='0000000000', date='2001-01-01')
```

Keep in mind the API limits maximum number of requested subjects to 30.

#### Docs
Project docs may be found here:
https://vater.readthedocs.io
