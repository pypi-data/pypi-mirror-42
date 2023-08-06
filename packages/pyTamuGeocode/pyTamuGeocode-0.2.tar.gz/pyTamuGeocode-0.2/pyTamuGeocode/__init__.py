import requests
import sqlite3

__all__ = ['TamuGeocode']

class TamuGeocode:
    """
    For geocoding and caching with sqlite using Texas A&M Geoservices API
    """
    def _call_geo_api(self, addr, city, state, zipcode):
        """
        Make a geocoding API call against TAMU and return the parsed result
        """
        if self._check_api_balance() == 0:
            raise Exception('Insufficient Balance')

        api_url = 'http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?'
        api_params = {
            'apiKey': self._tamu_key,
            'version': '4.01',
            'streetAddress': addr,
            'city': city,
            'state': state,
            'zip': zipcode,
            'includeHeader': 'true',
        }
        
        r = requests.post(api_url, data=api_params)
        
        # Process the result
        init_split = r.text.split('\r\n')  # Split the headers and the values to two lines
        headers = init_split[0].split(',')[:-1]
        values = init_split[1].split(',')[:-1]
        result_dict = dict(zip(headers, values))

        latlon = (float(result_dict['Latitude']), float(result_dict['Longitude']))

        return latlon

    def _check_api_balance(self):
        """
        Check the API balance and return it
        """
        api_url = 'https://geoservices.tamu.edu/UserServices/Payments/Balance/AccountBalanceWebServiceHttp.aspx?'
        api_params = {
            'apiKey': self._tamu_key,
            'version': '1.0',
            'format': 'csv',
        }

        balance = int(requests.post(api_url, data=api_params).text.split(',')[1])
        
        return balance

    def __init__(self, dbfile, tamu_key):
        self._tamu_key = tamu_key
        self._conn = sqlite3.connect(dbfile)
        self._conn.row_factory = sqlite3.Row
        self._cur = self._conn.cursor()
        
        self._load_cache()

    def _load_cache(self):
        try:
            q = 'SELECT * FROM geocode_cache;'
            self._cur.execute(q)

            self.geocode_cache = {}
            
            for row in self._cur.fetchall():
                k = tuple([row[x] for x in row.keys()[:-2]])
                d = (row['lat'], row['lon'])
                self.geocode_cache[k] = d

        except sqlite3.OperationalError:
            # Throwing the dice, but let's assume the table doesn't exist, so create..
            q = """
            CREATE TABLE geocode_cache (
                street_address TEXT,
                city TEXT,
                state TEXT,
                zipcode TEXT,
                lat NUMERIC,
                lon NUMERIC
            );
            """
            self._cur.execute(q)
            self._conn.commit()
            
            self.geocode_cache = {}

        return None

    def _write_new_geocode(self, addr, city, state, zipcode, lat, lon):
        """
        Insert the new data into the cache DB and into the cache dict
        """
        q = 'INSERT INTO geocode_cache (street_address, city, state, zipcode, lat, lon) VALUES(?,?,?,?,?,?)'
        idata  = (addr, city, state, zipcode, lat, lon)
        self._cur.execute(q, idata)
        self._conn.commit()
        self.geocode_cache[idata[:-2]] = idata[-2:]

        return None

    def geocode(self, addr, city, state, zipcode, only_check=False):
        """
        Geocode a single address

        If only_check is True, return a boolean indicating whether or not the address is in the cache
        """
        addr = addr.lower()
        city = city.lower()
        state = state.lower()
        zipcode = zipcode.lower()

        addr_tup = (addr, city, state, zipcode)

        if not only_check:
            if addr_tup in self.geocode_cache:
                return self.geocode_cache[addr_tup]
            else:
                latlon = self._call_geo_api(*addr_tup)
                idata = addr_tup + latlon
                self._write_new_geocode(*idata)

                return latlon
        else:
            if addr_tup in self.geocode_cache:
                return True
            else:
                return False
