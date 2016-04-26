from datetime import timedelta

from kids.cache import cache

from .common import Entity
from .performance_list import PerformanceList


class Runner(Entity):
	"""A runner represents a combination of horse, jockey and trainer competing in a given race"""

	REST_PERIOD = timedelta(days=90)

	@classmethod
	def get_runner_by_id(cls, id):
		"""Get the single runner with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_runners_by_race(cls, race):
		"""Get a list of runners competing in the specified race"""

		runners = cls.find_or_scrape(
			filter={'race_id': race['_id']},
			scrape=cls.scraper.scrape_runners,
			scrape_args=[race],
			expiry_date=race['start_time']
			)

		for runner in runners:
			if not 'race_id' in runner:
				runner['race_id'] = race['_id']
				runner.save()

		return runners

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		def handle_deleting_race(race):
			for runner in race.runners:
				runner.delete()

		cls.event_manager.add_subscriber('deleting_race', handle_deleting_race)

		cls.create_index([('race_id', 1)])
		cls.create_index([('race_id', 1), ('scraped_at', 1)])

	def __str__(self):

		return 'runner {number} in {race}'.format(number=self['number'], race=self.race)

	@property
	@cache
	def actual_weight(self):
		"""Return the weight carried by the runner plus the average weight of a racehorse"""

		return self.carrying + Horse.AVERAGE_WEIGHT

	@property
	@cache
	def age(self):
		"""Return the horse's official age as at the time of the race"""

		if 'foaled' in self.horse:
			birthday = self.horse['foaled'].replace(month=8, day=1)
			return (self.race.meet['date'] - birthday).days // 365

	@property
	@cache
	def at_distance(self):
		"""Return a PerformanceList containing all of the horse's prior performances within 100m of the current race's distance"""

		return PerformanceList([performance for performance in self.career if self.race['distance'] - 100 <= performance['distance'] <= self.race['distance'] + 100])

	@property
	@cache
	def at_distance_on_track(self):
		"""Return a PerformanceList containing all of the horse's prior performances within 100m of the current race's distance on the current track"""

		return PerformanceList([performance for performance in self.at_distance if performance in self.on_track])

	@property
	@cache
	def career(self):
		"""Return a PerformanceList containing all of the horse's performances prior to the current race"""

		return PerformanceList([performance for performance in self.horse.performances if performance['date'] < self.race.meet['date']])

	@property
	@cache
	def carrying(self):
		"""Return the official listed weight less allowances for the runner"""

		return self['weight'] - self['jockey_claiming']

	@property
	@cache
	def current_performance(self):
		"""Return the horse's performance for the current race if available"""

		for performance in self.horse.performances:
			if performance['track'] == self.race.meet['track'] and performance['date'] == self.race.meet['date']:
				return performance

	@property
	@cache
	def firm(self):
		"""Return a PerformanceList containing all of the horse's prior performances on firm tracks"""

		return self.get_performances_by_track_condition('firm')

	@property
	@cache
	def good(self):
		"""Return a PerformanceList containing all of the horse's prior performances on good tracks"""

		return self.get_performances_by_track_condition('good')

	@property
	@cache
	def heavy(self):
		"""Return a PerformanceList containing all of the horse's prior performances on heavy tracks"""

		return self.get_performances_by_track_condition('heavy')

	@property
	@cache
	def horse(self):
		"""Return the actual horse running in the race"""

		return Horse.get_horse_by_runner(self)

	@property
	@cache
	def jockey(self):
		"""Return the actual jockey riding in the race"""

		return Jockey.get_jockey_by_runner(self)

	@property
	@cache
	def on_track(self):
		"""Return a PerformanceList containing all of the horse's prior performances on the current track"""

		return PerformanceList([performance for performance in self.career if performance['track'] == self.race.meet['track']])

	@property
	@cache
	def on_up(self):
		"""Return a PerformanceList containing all of the horse's prior performances with the same UP number"""

		performances = []
		previous_date = None
		up = 0
		for index in range(len(self.career) - 1, 0, -1):
			if previous_date is None or ((self.career[index]['date'] - previous_date) < self.REST_PERIOD):
				up += 1
			else:
				up = 1
			if up == self.up:
				performances.append(self.career[index])
			previous_date = self.career[index]['date']

		return PerformanceList(performances)

	@property
	@cache
	def race(self):
		"""Return the race in which this runner competes"""

		return Race.get_race_by_id(self['race_id'])

	@property
	@cache
	def result(self):
		"""Return the final result for this runner if available"""

		if self.current_performance is not None:
			if self.current_performance['result'] is not None:
				return self.current_performance['result']
			else:
				return self.current_performance['starters']

	@property
	@cache
	def since_rest(self):
		"""Return a PerformanceList containing the horse's prior performances since the last spell of 90 days or more"""

		performances = []
		next_date = self.race.meet['date']
		for index in range(len(self.career)):
			if (next_date - self.career[index]['date']) < self.REST_PERIOD:
				performances.append(self.career[index])
				next_date = self.career[index]['date']
			else:
				break

		return PerformanceList(performances)

	@property
	@cache
	def soft(self):
		"""Return a PerformanceList containing all of the horse's prior performances on soft tracks"""

		return self.get_performances_by_track_condition('soft')

	@property
	@cache
	def spell(self):
		"""Return the number of days since the horse's previous run"""

		if len(self.career) > 0:
			return (self.race.meet['date'] - self.career[0]['date']).days

	@property
	@cache
	def starting_price(self):
		"""Return the starting price for this runner if available"""

		if self.current_performance is not None:
			return self.current_performance['starting_price']

	@property
	@cache
	def synthetic(self):
		"""Return a PerformanceList containing all of the horse's prior performances on synthetic tracks"""

		return self.get_performances_by_track_condition('synthetic')

	@property
	@cache
	def trainer(self):
		"""Return the trainer responsible for the runner"""

		return Trainer.get_trainer_by_runner(self)

	@property
	@cache
	def up(self):
		"""Return the number of races run by the horse (including this one) since the last rest period of 90 days or more"""

		up = 1

		next_date = self.race.meet['date']
		for index in range(len(self.career)):
			if (next_date - self.career[index]['date']) < self.REST_PERIOD:
				up += 1
				next_date = self.career[index]['date']
			else:
				break

		return up

	@property
	@cache
	def with_jockey(self):
		"""Return a PerformanceList containing all of the horse's prior performances with the same jockey"""

		return PerformanceList([performance for performance in self.career if performance['jockey_url'] == self['jockey_url']])

	def calculate_expected_speed(self, performance_list):
		"""Return a tuple containing expected speeds based on the minimum, maximum and average momentums for the specified performance list"""

		performance_list = getattr(self, performance_list)
		if performance_list is not None:
			return (
				performance_list.minimum_momentum / self.actual_weight,
				performance_list.maximum_momentum / self.actual_weight,
				performance_list.average_momentum / self.actual_weight
				)

	def get_performances_by_track_condition(self, track_condition):
		"""Return a PerformanceList containing all prior performances on the specified track condition"""

		return PerformanceList([performance for performance in self.career if performance['track_condition'].upper().startswith(track_condition.upper())])


from .race import Race
from .horse import Horse
from .jockey import Jockey
from .trainer import Trainer
