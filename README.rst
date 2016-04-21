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

Alternatively, a list of races occurring at a given meet can be obtained by accessing the meet's races property as follows:

	>>> races = meet.races

The get_races_by_meet method will return a list of Race objects. The Race class itself is derived from Python's built-in dict type, so a race's details can be accessed as follows:

	>>> number = races[index]['number']

To get the meet at which a given race occurs, access the race's meet property as follows:

	>>> meet = races[index].meet


Runners
~~~~~~~

A runner represents a combination of horse, jockey and trainer competing in a given race.

To get a list of runners competing in a given race, call the Runner.get_runners_by_race method as follows:

	>>> runners = pyracing.Runner.get_runners_by_race(race)

Alternatively, a list of runners competing in a given race can be obtained by accessing the race's runners property as follows:

	>>> runners = race.runners

The get_runners_by_race method will return a list of Runner objects. The Runner class itself is derived from Python's built-in dict type, so a runner's details can be accessed as follows:

	>>> number = runners[index]['number']

To get the race in which a given runner competes, access the runner's race property as follows:

	>>> race = runner[index].race

Runner objects also expose the following calculated values as properties that can be accessed using dot-notation:

+------------+---------------------------------------------------------------------------------------------------+
| Property   | Description                                                                                       |
+============+===================================================================================================+
| runner.age | The horse's official age as at the date of the race (calculated according to Australia standards) |
+------------+---------------------------------------------------------------------------------------------------+

The following properties (also accessible using dot-notation) return PerformanceList objects containing a filtered list of the horse's prior performances:

+-----------------------------+----------------------------------------------------------------------------------------+
| Property                    | Description                                                                            |
+=============================+========================================================================================+
| runner.at_distance          | All prior performances at a distance within 100m of the current race                   |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.at_distance_on_track | All prior performances at a distance within 100m of the current race on the same track |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.career               | All performances prior to the current race                                             |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.firm                 | All prior performances on FIRM tracks                                                  |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.good                 | All prior performances on GOOD tracks                                                  |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.heavy                | All prior performances on HEAVY tracks                                                 |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.on_track             | All prior performances on the current track                                            |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.soft                 | All prior performances on SOFT tracks                                                  |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.synthetic            | All prior performances on SYNTHETIC tracks                                             |
+-----------------------------+----------------------------------------------------------------------------------------+


Horses
~~~~~~

A horse represents the equine component of a given runner.

To get the horse for a given runner, call the Horse.get_horse_by_runner method as follows:

	>>> horse = pyracing.Horse.get_horse_by_runner(runner)

Alternatively, the horse for a given runner can be obtained by accessing the runner's horse property as follows:

	>>> horse = runner.horse

The get_horse_by_runner method will return a single Horse object. The Horse class itself is derived from Python's built-in dict type, so a horse's details can be accessed as follows:

	>>> name = horse['name']


Jockeys
~~~~~~~

A jockey represents the human riding a runner.

To get the jockey for a given runner, call the Jockey.get_jockey_by_runner method as follows:

	>>> jockey = pyracing.Jockey.get_jockey_by_runner(runner)

Alternatively, the jockey for a given runner can be obtained by accessing the runner's jockey property as follows:

	>>> jockey = runner.jockey

The get_jockey_by_runner method will return a single Jockey object. The Jockey class itself is derived from Python's built-in dict type, so a jockey's details can be accessed as follows:

	>>> name = jockey['name']


Trainers
~~~~~~~~

A trainer represents the people responsible for a horse.

To get the trainer for a given runner, call the Trainer.get_trainer_by_runner method as follows:

	>>> trainer = pyracing.Trainer.get_trainer_by_runner(runner)

Alternatively, the trainer for a given runner can be obtained by accessing the runner's trainer property as follows:

	>>> trainer = runner.trainer

The get_trainer_by_runner method will return a single Trainer object. The Trainer class itself is derived from Python's built-in dict type, so a trainer's details can be accessed as follows:

	>>> name = trainer['name']


Performances
~~~~~~~~~~~~

A performance represents the result of a completed run by a horse and jockey.

To get a list of performances for a given horse, call the Horse.get_performances_by_horse method as follows:

	>>> performances = pyracing.Performance.get_performances_by_horse(horse)

Alternatively, a list of performances for a given horse can be obtained by accessing the horse's performances property as follows:

	>>> performances = horse.performances

The get_performances_by_horse method will return a list of Performance objects. The Performance class itself is derived from Python's built-in dict type, so a performance's details can be accessed as follows:

	>>> result = performances[index]['result']


Batch Processing
~~~~~~~~~~~~~~~~

The pyracing package includes an Iterator class to facilitate the batch processing of ALL racing data for a specified date range.

To implement batch processing, create an instance of the Iterator class and call its process_dates method as follows:

	>>> iterator = pyracing.Iterator(threads=1, message_prefix='processing', {keyword arguments})
	>>> iterator.process_dates(date_from, date_to)

Alternatively, to process ALL racing data for a single date instead, call the process_date method as follows:

	>>> iterator.process_date(date)

The threads and message_prefix arguments to the Iterator constructor are both optional.

The threads argument specifies the number of threads to use for processing entities (all threads will be joined after processing a single date's data, just prior to executing the date_post_processor method if specified - see below). The default value for threads is 1.

The message_prefix argument specifies a text string to be prepended to a description of each entity being processed in the messages logged by the iterator. The default value for message_prefix is 'processing'.

Any combination of the following keyword arguments may also be passed to the Iterator constructor, with each specifying a callable that will be called at a specific time during the processing of entities:

+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| Keyword               | Calls                              | When                                                                             |
+=======================+====================================+==================================================================================+
| date_pre_processor    | date_pre_processor(date)           | BEFORE meets occurring on date are processed                                     |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| date_post_processor   | date_post_processor(date)          | AFTER meets occurring on date have been processed (and threads have been joined) |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| meet_pre_processor    | meet_pre_processor(meet)           | BEFORE races occurring at meet are processed                                     |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| meet_post_processor   | meet_post_processor(mmet)          | AFTER races occurring at meet have been processed                                |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| race_pre_processor    | race_pre_processor(race)           | BEFORE runners competing in race are processed                                   |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| race_post_processor   | race_post_processor(race)          | AFTER runners competing in race have been processed                              |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| runner_pre_processor  | runner_pre_processor(runner)       | BEFORE the runner's horse, jockey and trainer are processed                      |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| runner_post_processor | runner_post_processor(runner)      | AFTER the runner's horse, jockey and trainer have been processed                 |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| horse_pre_processor   | horse_pre_processor(horse)         | BEFORE the horse's performances are processed                                    |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| horse_post_processor  | horse_post_processor(horse)        | AFTER the horse's performances have been processed                               |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| jockey_processor      | jockey_processor(jockey)           | ONCE for each run by a jockey                                                    |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| trainer_processor     | trainer_processor(trainer)         | ONCE for each run by a trainer                                                   |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| performance_processor | performance_processor(performance) | ONCE for each performance by a horse                                             |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+


Event Hooks
~~~~~~~~~~~

The pyracing package implements a publisher/subscriber style event model. To subscribe to an event, call the pyracing.add_subscriber method as follows:

	>>> pyracing.add_subscriber('event_name', handler)

handler must be a function that conforms to the handler signature as specified in the following table:

+----------------------+----------------------+------------------------------------------------------+
| Event Name           | Calls                | When                                                 |
+======================+======================+======================================================+
| deleting_meet        | handler(meet)        | BEFORE meet is deleted from the database             |
+----------------------+----------------------+------------------------------------------------------+
| deleted_meet         | handler(meet)        | AFTER meet has been deleted from the database        |
+----------------------+----------------------+------------------------------------------------------+
| saving_meet          | handler(meet)        | BEFORE meet is saved to the database                 |
+----------------------+----------------------+------------------------------------------------------+
| saved_meet           | handler(meet)        | AFTER meet has been saved to the database            |
+----------------------+----------------------+------------------------------------------------------+
| deleting_race        | handler(race)        | BEFORE race is deleted from the database             |
+----------------------+----------------------+------------------------------------------------------+
| deleted_race         | handler(race)        | AFTER race has been deleted from the database        |
+----------------------+----------------------+------------------------------------------------------+
| saving_race          | handler(race)        | BEFORE race is saved to the database                 |
+----------------------+----------------------+------------------------------------------------------+
| saved_race           | handler(race)        | AFTER race has been saved to the database            |
+----------------------+----------------------+------------------------------------------------------+
| deleting_runner      | handler(runner)      | BEFORE runner is deleted from the database           |
+----------------------+----------------------+------------------------------------------------------+
| deleted_runner       | handler(runner)      | AFTER runner has been deleted from the database      |
+----------------------+----------------------+------------------------------------------------------+
| saving_runner        | handler(runner)      | BEFORE runner is saved to the database               |
+----------------------+----------------------+------------------------------------------------------+
| saved_runner         | handler(runner)      | AFTER runner has been saved to the database          |
+----------------------+----------------------+------------------------------------------------------+
| deleting_horse       | handler(horse)       | BEFORE horse is deleted from the database            |
+----------------------+----------------------+------------------------------------------------------+
| deleted_horse        | handler(horse)       | AFTER horse has been deleted from the database       |
+----------------------+----------------------+------------------------------------------------------+
| saving_horse         | handler(horse)       | BEFORE horse is saved to the database                |
+----------------------+----------------------+------------------------------------------------------+
| saved_horse          | handler(horse)       | AFTER horse has been saved to the database           |
+----------------------+----------------------+------------------------------------------------------+
| deleting_jockey      | handler(jockey)      | BEFORE jockey is deleted from the database           |
+----------------------+----------------------+------------------------------------------------------+
| deleted_jockey       | handler(jockey)      | AFTER jockey has been deleted from the database      |
+----------------------+----------------------+------------------------------------------------------+
| saving_jockey        | handler(jockey)      | BEFORE jockey is saved to the database               |
+----------------------+----------------------+------------------------------------------------------+
| saved_jockey         | handler(jockey)      | AFTER jockey has been saved to the database          |
+----------------------+----------------------+------------------------------------------------------+
| deleting_trainer     | handler(trainer)     | BEFORE trainer is deleted from the database          |
+----------------------+----------------------+------------------------------------------------------+
| deleted_trainer      | handler(trainer)     | AFTER trainer has been deleted from the database     |
+----------------------+----------------------+------------------------------------------------------+
| saving_trainer       | handler(trainer)     | BEFORE trainer is saved to the database              |
+----------------------+----------------------+------------------------------------------------------+
| saved_trainer        | handler(trainer)     | AFTER trainer has been saved to the database         |
+----------------------+----------------------+------------------------------------------------------+
| deleting_performance | handler(performance) | BEFORE performance is deleted from the database      |
+----------------------+----------------------+------------------------------------------------------+
| deleted_performance  | handler(performance) | AFTER performance has been deleted from the database |
+----------------------+----------------------+------------------------------------------------------+
| saving_performance   | handler(performance) | BEFORE performance is saved to the database          |
+----------------------+----------------------+------------------------------------------------------+
| saved_performance    | handler(performance) | AFTER performance has been saved to the database     |
+----------------------+----------------------+------------------------------------------------------+


Testing
-------

To run the included test suite, execute the following command from the root directory of the pyracing repository::

	python setup.py test

The above command will ensure all test dependencies are installed in your current Python environment. For more concise output during subsequent test runs, the following command can be executed from the root directory of the pyracing repository instead::

	nosetests

Alternatively, individual components of pyracing can be tested by executing any of the following commands from the root directory of the pyracing repository::

	nosetests pyracing.test.meets
	nosetests pyracing.test.races
	nosetests pyracing.test.runners
	nosetests pyracing.test.horses
	nosetests pyracing.test.jockeys
	nosetests pyracing.test.trainers
	nosetests pyracing.test.performances
	nosetests pyracing.test.iterator


Version History
---------------

0.1.0 (21 April 2016)
	Interim release to facilitate database pre-population
