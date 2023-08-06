FullContact.py
==============

[![PyPI version](https://badge.fury.io/py/fullcontact.py.svg)](https://pypi.python.org/pypi/FullContact.py)
[![Build Status](https://api.travis-ci.org/fullcontact/fullcontact.py.svg?branch=master)](https://travis-ci.org/fullcontact/fullcontact.py)

A Python interface for the [FullContact API](http://docs.fullcontact.com/).

Installation
------------

```
pip install fullcontact.py
```

Usage
-----


```python

from fullcontact import FullContact
import asyncio
async def get_person():
    fc = FullContact('your_api_key')

    #return a FullContactRespoonse object
    r = await fc.person(email='you@email.com')
    print(r.status_code) # 200
    print(r.rate_limit_remaining) # 59
    print(r.json_response) # {u'socialProfiles': [...], u'demographics': {...}, ... }
```

asyncio.get_event_loop().run_until_complete(test())

Supported Python Versions
-------------------------
* 3.6
* 3.7
