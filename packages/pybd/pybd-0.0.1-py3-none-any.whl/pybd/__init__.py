#!/usr/bin/env python

#Copyright 2019 John T. Foster
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import psycopg2
import numpy as np


class PyBD(object):
    
    """Class for querying Bazean database.
    
    Args:
    
        user (str): Bazean database username
        password (str): Bazean database password
        subdomain (str): URL subdomain, default is "premium"
        schema (str): Postgres schema, default is "goliath"
    
    
    """
    
    def __init__(self, user,  password, subdomain="premium", schema="goliath"):
        
        url = "postgresql://{}.bazean.com:5432/db?ssl=true".format(subdomain)
        
        #Create connection to database
        self.__connection = psycopg2.connect(user=user, password=password, dsn=url)
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("SET search_path TO {}".format(schema))
        
        self.__default_fetch_size = 50
        
    def __del__(self):
        """Destructor to close database connection."""
        
        self.__connection.close()
        self.__cursor.close()
        
        
    def __fetch(self, raw_sql_string, number_of_records_to_fetch=None): 
        """Fetches records from database
        
        Args:
            raw_sql_string (str): SQL query string
            number_of_records_to_fetch (int or str): limits the length of returned records
            
        Returns:
            (list): A Python list with the records returned by the sql query.
        """
        
        self.__cursor.execute(raw_sql_string)
        
        if number_of_records_to_fetch is None:
            return list(map(list, self.__cursor.fetchmany(size=self.__default_fetch_size)))
        elif isinstance(number_of_records_to_fetch, int):
            return list(map(list, self.__cursor.fetchmany(size=number_of_records_to_fetch)))
        elif isinstance(number_of_records_to_fetch, str):
            if number_of_records_to_fetch == 'all':
                return list(map(list, self.__cursor.fetchall()))
            
    def __build_query_string(self, table, columns, **kwargs):
        
        if columns != '*' and len(columns) > 1:
            columns = ','.join(columns)
        else:
            columns, = columns 
        
        query_string = "SELECT {} FROM {}".format(columns, table)
            
        if kwargs is not None:
            for count, items in enumerate(kwargs.items()):
                key, value = items
                if count == 0:
                    query_string += " WHERE {}='{}'".format(key, value)
                else:
                    query_string += " AND {}='{}'".format(key, value)
            
        return query_string
    
    def set_fetch_size(self, value):
        """Sets the fetch size for database query methods i.e.\ `get_` methods
        
        Args:
            value (int or 'all'): fetch size, default is 50.
        """
        self.__default_fetch_size = value
      
            
    def get(self, table, columns, **kwargs):
        
        query_string = self.__build_query_string(table, columns, **kwargs)
        
        return self.__fetch(query_string, number_of_records_to_fetch=self.__default_fetch_size)
    
    def get_tickers_by_state(self, state):
        
        db_tickers = self.get(table='well_all', columns=('parent_ticker',), state=state)
        unique_tickers = np.unique(np.array(db_tickers, dtype=np.str))
        return unique_tickers[unique_tickers != 'None'].tolist()
    
    def get_well_locations_by_ticker_and_state(self, ticker, state):
        latitude, longitude, api = np.array(self.get(table='well_all', 
                                                     columns=('latitude_surface_hole',
                                                              'longitude_surface_hole', 'api'),
                                                     parent_ticker=ticker, state=state)).T 
        bool_array = latitude != None
        lat_clean = latitude[bool_array].astype(dtype=np.float)
        long_clean = longitude[bool_array].astype(dtype=np.float)
        api_clean = api[bool_array].astype(dtype=np.str)
        return (lat_clean, long_clean, api_clean)
    
    def get_production_from_api(self, api):
        
        default_fetch_size = self.__default_fetch_size
        self.set_fetch_size('all')
        request = np.array(self.get(table='production_all', 
                           columns=('date', 'volume_oil_formation_bbls', 'volume_gas_formation_mcf', 
                                    'volume_water_formation_bbls'), api=api)).T
        self.set_fetch_size(default_fetch_size)
        if request.size != 0:
            date, oil, gas, water = request
            return (date.astype("datetime64"), oil.astype("double"), gas.astype("double"), water.astype("double"))
        else:
            return None
        
        
