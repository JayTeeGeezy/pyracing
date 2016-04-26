from datetime import timedelta

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

		runners = sorted(cls.find_or_scrape(
			filter={'race_id': race['_id']},
			scrape=cls.scraper.scrape_runners,
			scrape_args=[race],
			expiry_date=race['start_time']
			), key=lambda runner: runner['number'])

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
	def actual_weight(self):
		"""Return the weight carried by the runner plus the average weight of a racehorse"""

		if self.carrying is not None:
			return self.carrying + Horse.AVERAGE_WEIGHT

	@property
	def age(self):
		"""Return the horse's official age as at the time of the race"""

		if 'foaled' in self.horse and self.horse['foaled'] is not None:
			birthday = self.horse['foaled'].replace(month=8, day=1)
			return (self.race.meet['date'] - birthday).days // 365

	@property
	def at_distance(self):
		"""Return a PerformanceList containing all of the horse's prior performances within 100m of the current race's distance"""

		return PerformanceList([performance for performance in self.career if self.race['distance'] - 100 <= performance['distance'] <= self.race['distance'] + 100])

	@property
	def at_distance_on_track(self):
		"""Return a PerformanceList containing all of the horse's prior performances within 100m of the current race's distance on the current track"""

		return PerformanceList([performance for performance in self.at_distance if performance in self.on_track])

	@property
	def career(self):
		"""Return a PerformanceList containing all of the horse's performances prior to the current race"""

		return PerformanceList([performance for performance in self.horse.performances if performance['date'] < self.race.meet['date']])

	@property
	def carrying(self):
		"""Return the official listed weight less allowances for the runner"""

		if 'weight' in self and self['weight'] is not None and 'jockey_claiming' in self and self['jockey_claiming'] is not None:
			return self['weight'] - self['jockey_claiming']

	@property
	def current_performance(self):
		"""Return the horse's performance for the current race if available"""

		for performance in self.horse.performances:
			if performance['track'] == self.race.meet['track'] and performance['date'] == self.race.meet['date']:
				return performance

	@property
	def firm(self):
		"""Return a PerformanceList containing all of the horse's prior performances on firm tracks"""

		return self.get_performances_by_track_condition('firm')

	@property
	def good(self):
		"""Return a PerformanceList containing all of the horse's prior performances on good tracks"""

		return self.get_performances_by_track_condition('good')

	@property
	def heavy(self):
		"""Return a PerformanceList containing all of the horse's prior performances on heavy tracks"""

		return self.get_performances_by_track_condition('heavy')

	@property
	def horse(self):
		"""Return the actual horse running in the race"""

		if not 'horse' in self.cache:
			self.cache['horse'] = Horse.get_horse_by_runner(self)
		return self.cache['horse']

	@property
	def jockey(self):
		"""Return the actual jockey riding in the race"""

		if not 'jockey' in self.cache:
			self.cache['jockey'] = Jockey.get_jockey_by_runner(self)
		return self.cache['jockey']

	@property
	def on_track(self):
		"""Return a PerformanceList containing all of the horse's prior performances on the current track"""

		return PerformanceList([performance for performance in self.career if performance['track'] == self.race.meet['track']])

	@property
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
	def race(self):
		"""Return the race in which this runner competes"""

		if not 'race' in self.cache:
			self.cache['race'] = Race.get_race_by_id(self['race_id'])
		return self.cache['race']

	@property
	def result(self):
		"""Return the final result for this runner if available"""

		if self.current_performance is not None:
			if self.current_performance['result'] is not None:
				return self.current_performance['result']
			else:
				return self.current_performance['starters']

	@property
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
	def soft(self):
		"""Return a PerformanceList containing all of the horse's prior performances on soft tracks"""

		return self.get_performances_by_track_condition('soft')

	@property
	def spell(self):
		"""Return the number of days since the horse's previous run"""

		if len(self.career) > 0:
			return (self.race.meet['date'] - self.career[0]['date']).days

	@property
	def starting_price(self):
		"""Return the starting price for this runner if available"""

		if self.current_performance is not None:
			if 'starting_price' in self.current_performance:
				return self.current_performance['starting_price']

	@property
	def synthetic(self):
		"""Return a PerformanceList containing all of the horse's prior performances on synthetic tracks"""

		return self.get_performances_by_track_condition('synthetic')

	@property
	def trainer(self):
		"""Return the trainer responsible for the runner"""

		if not 'trainer' in self.cache:
			self.cache['trainer'] = Trainer.get_trainer_by_runner(self)
		return self.cache['trainer']

	@property
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
	def with_jockey(self):
		"""Return a PerformanceList containing all of the horse's prior performances with the same jockey"""

		return PerformanceList([performance for performance in self.career if performance['jockey_url'] == self['jockey_url']])

	def calculate_expected_speed(self, performance_list):
		"""Return a tuple containing expected speeds based on the minimum, maximum and average momentums for the specified performance list"""

		performance_list = getattr(self, performance_list)
		if performance_list is not None:

			expected_speeds = [None, None, None]

			if self.actual_weight is not None:
				if performance_list.minimum_momentum is not None:
					expected_speeds[0] = performance_list.minimum_momentum / self.actual_weight
				if performance_list.maximum_momentum is not None:
					expected_speeds[1] = performance_list.maximum_momentum / self.actual_weight
				if performance_list.average_momentum is not None:
					expected_speeds[2] = performance_list.average_momentum / self.actual_weight

			return tuple(expected_speeds)

	def get_performances_by_track_condition(self, track_condition):
		"""Return a PerformanceList containing all prior performances on the specified track condition"""

		return PerformanceList([performance for performance in self.career if performance['track_condition'].upper().startswith(track_condition.upper())])


from .race import Race
from .horse import Horse
from .jockey import Jockey
from .trainer import Trainer
