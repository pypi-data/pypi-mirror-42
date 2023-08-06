PyBD
****

.. image:: https://travis-ci.org/daytum/PyBD.svg?branch=master
    :target: https://travis-ci.org/daytum/PyBD
.. image:: https://coveralls.io/repos/github/daytum/PyBD/badge.svg?branch=master
   :target: https://coveralls.io/github/daytum/PyBD?branch=master
.. image:: https://readthedocs.org/projects/py-bd/badge/?version=latest
   :target: https://py-bd.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://badge.fury.io/py/pybd.svg
   :target: https://badge.fury.io/py/pybd

A Python API to access the Bazean Postgres database

Example Usage
=============

A simple Python script that gets the production data from 10 wells from the state of Texas operated by XOM:

.. code-block:: python

    from pybd import PyBD

    db = PyBD(user='bazean_postgres_username', password='bazean_postgres_password')
    db.set_fetch_size(10)
    latitude, longitude, apis = db.get_well_locations_by_ticker_and_state('XOM', 'TX')

    oil_production = []
    for i in range(10):
       dates, oil, gas, water = db.get_production_from_api(apis[i])
       oil_production += [oil]
