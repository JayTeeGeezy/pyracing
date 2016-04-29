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

In addition, race objects expose an 'importance' property that returns the product of the starting prices of all runners in the race that finished in the first four, or 1.0 if such data is not yet available. The importance property is accessible using dot-notation as follows:

	>>> importance = races[index].importance


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

+----------------------------+-------------------------------------------------------------------------------------------------------+
| Property                   | Description                                                                                           |
+============================+=======================================================================================================+
| runner.actual_weight       | The weight carried by the runner plus the average weight of a racehorse (in kg)                       |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runner.age                 | The horse's official age as at the date of the race (calculated according to Australia standards)     |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runner.carrying            | The official listed weight for the runner less allowances (in kg)                                     |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runner.current_performance | The horse's performance for the current race if available (None if not)                               |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runner.result              | The final result achieved by this runner if available (None if not)                                   |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runners.spell              | The number of days since the horse's previous run (None if this is the horse's first run)             |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runners.starting_price     | The starting price for this runner if available (None if not)                                         |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| runner.up                  | The number of races run by the horse (including the this one) since the last spell of 90 days or more |
+----------------------------+-------------------------------------------------------------------------------------------------------+

The following properties (also accessible using dot-notation) return PerformanceList objects (see below) containing a filtered list of the horse's prior performances:

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
| runner.on_up                | All prior performances with the same UP number as the horse's current run              |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.since_rest           | All performances since the horse's last spell of 90 days or more                       |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.soft                 | All prior performances on SOFT tracks                                                  |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.synthetic            | All prior performances on SYNTHETIC tracks                                             |
+-----------------------------+----------------------------------------------------------------------------------------+
| runner.with_jockey          | All prior performances for the horse with the same jockey                              |
+-----------------------------+----------------------------------------------------------------------------------------+

The following properties (also accessible using dot-notation) return PerformanceList objects (see below) containing a filtered list of the jockey's prior performances:

+------------------------------------+----------------------------------------------------------------------------------------+
| Property                           | Description                                                                            |
+====================================+========================================================================================+
| runner.jockey_at_distance          | All prior performances at a distance within 100m of the current race                   |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_at_distance_on_track | All prior performances at a distance within 100m of the current race on the same track |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_career               | All performances prior to the current race                                             |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_firm                 | All prior performances on FIRM tracks                                                  |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_good                 | All prior performances on GOOD tracks                                                  |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_heavy                | All prior performances on HEAVY tracks                                                 |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_on_track             | All prior performances on the current track                                            |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_soft                 | All prior performances on SOFT tracks                                                  |
+------------------------------------+----------------------------------------------------------------------------------------+
| runner.jockey_synthetic            | All prior performances on SYNTHETIC tracks                                             |
+------------------------------------+----------------------------------------------------------------------------------------+

The PerformanceList objects returned by the properties described above expose the following properties:

+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| Property               | Description                                                                                                             |
+========================+=========================================================================================================================+
| average_momentum       | The average momentum per start in the performance list (None if no starts)                                              |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| average_prize_money    | The average prize money earned per start in the performance list (None if no starts)                                    |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| average_starting_price | The average starting price per start in the performance list (None if no starts)                                        |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| fourths                | The number of fourth placing performances included in the performance list                                              |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| fourth_pct             | The number of fourths as a percentage of the number of starts (None if no starts)                                       |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| maximum_momentum       | The maximum momentum achieved for any performance in the performance list                                               |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| minimum_momentum       | The minimum momentum achieved for any performance in the performance list                                               |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| places                 | The number of placing (1st, 2nd and 3rd) performances included in the performance list                                  |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| place_pct              | The number of places as a percentage of the number of starts (None if no starts)                                        |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| roi                    | The total starting price for wins less the number of starts as a percentage of the number of starts (None if no starts) |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| seconds                | The number of second placing performances included in the performance list                                              |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| second_pct             | The number of seconds as a percentage of the number of starts (None if no starts)                                       |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| starts                 | The total number of starts included in the performance list                                                             |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| thirds                 | The number of third placing performances included in the performance list                                               |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| third_pct              | The number of thirds as a percentage of the number of starts (None if no starts)                                        |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| total_prize_money      | The total prize money earned in the performance list                                                                    |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| wins                   | The number of winning performances included in the performance list                                                     |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+
| win_pct                | The number of wins as a percentage of the number of starts (None if no starts)                                          |
+------------------------+-------------------------------------------------------------------------------------------------------------------------+

An example of accessing these statistics is given below:

	>>> good_wins = runner.good.wins

Runner objects also provide a calculate_expected_speed method that will return a tuple of minimum, maximum and average expected speeds for the runner based on the runner's actual weight and the minimum, maximum and average momentums for a specified performance list, as follows:

	>>> runner.calculate_expected_speed('career')
	(15.75, 17.25, 16.50)


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

Performance objects also expose the following calculated values as properties that can be accessed using dot-notation:

+-----------------------------+--------------------------------------------------------------------------------+
| Property                    | Description                                                                    |
+=============================+================================================================================+
| performance.actual_distance | The actual distance run by the horse in the winning time (in metres)           |
+-----------------------------+--------------------------------------------------------------------------------+
| performance.actual_weight   | The weight carried by the horse plus the average weight of a racehorse (in kg) |
+-----------------------------+--------------------------------------------------------------------------------+
| performance.momentum        | The average momentum achieved by the horse (in kg m/s)                         |
+-----------------------------+--------------------------------------------------------------------------------+
| performance.speed           | The average speed run by the horse (in m/s)                                    |
+-----------------------------+--------------------------------------------------------------------------------+


Batch Processing
~~~~~~~~~~~~~~~~

The pyracing package includes a Processor class to facilitate the batch processing of ALL racing data for a specified date range.

To implement batch processing, extend the Processor class with your own custom sub-class and call its process_dates method as follows:

	>>> custom_processor = CustomProcessor(threads=1, message_prefix='processing')
	>>> custom_processor.process_dates(date_from, date_to)

Alternatively, to process ALL racing data for a single date instead, call the process_date method as follows:

	>>> custom_processor.process_date(date)

The threads and message_prefix arguments to the Processor constructor are both optional.

The threads argument specifies the number of threads to use for processing entities (all threads will be joined after processing a single date's data, just prior to executing the post_process_date method if specified - see below). The default value for threads is 1.

The message_prefix argument specifies a text string to be prepended to a description of each entity being processed in the messages logged by the processor. The default value for message_prefix is 'processing'.

Any combination of the following instance methods may be defined in a custom Processor class, with each being called at a specific time during the processing of entities:

+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| Method                | Calls                              | When                                                                             |
+=======================+====================================+==================================================================================+
| pre_process_date      | pre_process_date(date)             | BEFORE meets occurring on date are processed                                     |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| post_process_date     | post_process_date(date)            | AFTER meets occurring on date have been processed (and threads have been joined) |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| pre_process_meet      | pre_process_meet(meet)             | BEFORE races occurring at meet are processed                                     |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| post_process_meet     | post_process_meet(meet)            | AFTER races occurring at meet have been processed                                |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| pre_process_race      | pre_process_race(race)             | BEFORE runners competing in race are processed                                   |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| post_process_race     | post_process_race(race)            | AFTER runners competing in race have been processed                              |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| pre_process_runner    | pre_process_runner(runner)         | BEFORE the runner's horse, jockey and trainer are processed                      |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| post_process_runner   | post_process_runner(runner)        | AFTER the runner's horse, jockey and trainer have been processed                 |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| pre_process_horse     | pre_process_horse(horse)           | BEFORE the horse's performances are processed                                    |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| post_process_horse    | post_process_horse(horse)          | AFTER the horse's performances have been processed                               |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| process_jockey        | process_jockey(jockey)             | ONCE for each run by a jockey                                                    |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| process_trainer       | process_trainer(trainer)           | ONCE for each run by a trainer                                                   |
+-----------------------+------------------------------------+----------------------------------------------------------------------------------+
| process_performance   | process_performance(performance)   | ONCE for each performance by a horse                                             |
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
	nosetests pyracing.test.performance_lists
	nosetests pyracing.test.processor


Version History
---------------

0.3.0 (28 April 2016)
	Interim release to facilitate initial predictions

0.2.5 (27 April 2016)
	Fix ZeroDivisionErrors

0.2.4 (27 April 2016)
	Fix ValueErrors in PerformanceList

0.2.3 (26 April 2016)
	Fix TypeError in Runner.calculate_expected_speed

0.2.2 (26 April 2016)
	Fix memory leak in cached properties

0.2.1 (26 April 2016)
	Fix TypeErrors in calculated properties

0.2.0 (26 April 2016)
	Interim release to facilitate pre-seeding query data

0.1.1 (22 April 2016)
	Fix issue with caught exceptions hanging Processor

0.1.0 (21 April 2016)
	Interim release to facilitate database pre-population
