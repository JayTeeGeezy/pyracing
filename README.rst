pyracing
=========

Python horse racing class library


Installation
------------

To install the latest release of pyracing to your current Python environment, execute the following command::

	pip install pyracing

Alternatively, to install pyracing from a source distribution, execute the following command from the root directory of the pyracing repository::

	python setup.py install

To install pyracing from a source distribution as a symlink for development purposes, execute the following command from the root directory of the pyracing repository instead::

	python setup.py develop


Usage
-----

To use pyracing, you must first import the pyracing package into your Python interpreter and initialize the pyracing module dependencies. pyracing depends on a database connection and a compatible horse racing web scraper.

The database connection must conform to the pymongo API, supporting code such as the following::

	documents = database[collection_name].find(filter)

The web scraper must conform to the pypunters API, supporting code such as the following::

	meets = scraper.scrape_meets(date)

pyracing has only been tested using pymongo and pypunters. To implement these dependencies using the same packages, execute the following code:

	>>> import pymongo
	>>> database = pymongo.MongoClient()[database_name]

	>>> import cache_requests
	>>> http_client = cache_requests.Session()
	>>> from lxml import html
	>>> html_parser = html.fromstring
	>>> import pypunters
	>>> scraper = pypunters.Scraper(http_client, html_parser)

With these dependencies in place, the pyracing package can be imported and initialized as follows:

	>>> import pyracing
	>>> pyracing.initialize(database, scraper)


Meets
~~~~~

A meet represents a collection of races occurring at a given track on a given date.

To get a list of meets occurring on a given date, call the Meet.get_meets_by_date method as follows:

	>>> from datetime import datetime
	>>> date = datetime(2016, 2, 1)
	>>> meets = pyracing.Meet.get_meets_by_date(date)

The get_meets_by_date method will return a list of Meet objects. The Meet class itself is derived from Python's built-in dict type, so a meet's details can be accessed as follows:

	>>> track = meets[index]['track']


Races
~~~~~

A race represents a collection of runners competing in a single event at a given meet.

To get a list of races occurring at a given meet, call the Race.get_races_by_meet method as follows:

	>>> races = pyracing.Race.get_races_by_meet(meet)

The get_races_by_meet method will return a list of Race objects. The Race class itself is derived from Python's built-in dict type, so a race's details can be accessed as follows:

	>>> number = races[index]['number']

To get the meet at which a given race occurs, access the race's meet property as follows:

	>>> meet = races[index].meet


Testing
-------

To run the included test suite, execute the following command from the root directory of the pyracing repository::

	python setup.py test

The above command will ensure all test dependencies are installed in your current Python environment. For more concise output during subsequent test runs, the following command can be executed from the root directory of the pyracing repository instead::

	nosetests

Alternatively, individual components of pyracing can be tested by executing any of the following commands from the root directory of the pyracing repository::

	nosetests pyracing.test.meets
	nosetests pyracing.test.races
