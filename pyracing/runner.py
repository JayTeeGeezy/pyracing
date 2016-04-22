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
	def age(self):
		"""Return the horse's official age as at the time of the race"""

		if 'foaled' in self.horse:
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

		return Horse.get_horse_by_runner(self)

	@property
	def jockey(self):
		"""Return the actual jockey riding in the race"""

		return Jockey.get_jockey_by_runner(self)

	@property
	def on_track(self):
		"""Return a PerformanceList containing all of the horse's prior performances on the current track"""

		return PerformanceList([performance for performance in self.career if performance['track'] == self.race.meet['track']])

	@property
	def race(self):
		"""Return the race in which this runner competes"""

		return Race.get_race_by_id(self['race_id'])

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
	def synthetic(self):
		"""Return a PerformanceList containing all of the horse's prior performances on synthetic tracks"""

		return self.get_performances_by_track_condition('synthetic')

	@property
	def trainer(self):
		"""Return the trainer responsible for the runner"""

		return Trainer.get_trainer_by_runner(self)

	@property
	def with_jockey(self):
		"""Return a PerformanceList containing all of the horse's prior performances with the same jockey"""

		return PerformanceList([performance for performance in self.career if performance['jockey_url'] == self['jockey_url']])

	def get_performances_by_track_condition(self, track_condition):
		"""Return a PerformanceList containing all prior performances on the specified track condition"""

		return PerformanceList([performance for performance in self.career if performance['track_condition'].upper().startswith(track_condition.upper())])


from .race import Race
from .horse import Horse
from .jockey import Jockey
from .trainer import Trainer
