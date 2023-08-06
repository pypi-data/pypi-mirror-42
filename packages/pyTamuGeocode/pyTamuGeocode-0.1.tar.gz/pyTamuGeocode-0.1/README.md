pyTamuGeocode
=============

A python library to perform simple queries against Texas A&M's [geocoding service](https://geoservices.tamu.edu/Services/Geocode/), and cache results in a sqlite database.

## Installation

`pip install pyTamuGeocode`

Easy

## Usage

To start, you need to register and get an API key (fairly simple process).

Once that's done, life is easy.

```
from pyTamuGeocode import TamuGeocode

tamu_api_key = 'api key here'
cache_db_file = 'geocode_cache.db'

tg = TamuGeocode(cache_db_file, tamu_api_key)

# street address, city, state, zip
tg_res = tg.geocode('2703 Ena Dr.', 'Lansing', 'Michigan', '48917')

print(tg_res)
```

```
(42.7053756, -84.6660981)
```

Additionally, once you geocode an address, it caches it by way of a tuple of the address, city, state, and zipcode.

Don't worry about capitalization, as it `lower()`'s all the address components.