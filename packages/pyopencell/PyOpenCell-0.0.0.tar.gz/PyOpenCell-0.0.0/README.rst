   Inspired by https://gitlab.com/rhab/PyOTRS

PyOpenCell is a Python wrapper for accessing `Open Cell <https://www.opencellsoft.com/>`_ (Version 5 or 6) using the
REST API.

You can see all the API information [here](https://api.opencellsoft.com/6.0.0)

Features
--------

Access an OpenCell instance to:

* find a Customer by ID
* create or update a Account Hierarchy
* create Subscription

Installation
============

Dependencies
------------

*Dependencies are installed automatically*

pip:

- python-requests

Python Usage
============

Quickstart
----------

Get Customer with Customer ID 1 from OpenCell over the REST API::

>>> client = Client(baseurl='http://myoc/', username='User', password='pwd')
>>> customer = client.find_customer(1)

License
=======
