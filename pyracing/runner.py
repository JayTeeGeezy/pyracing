from .common import Entity


class Runner(Entity):
	"""A runner represents a combination of horse, jockey and trainer competing in a given race"""

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

	@property
	def horse(self):
		"""Return the actual horse running in the race"""

		return Horse.get_horse_by_runner(self)

	@property
	def jockey(self):
		"""Return the actual jockey riding in the race"""

		return Jockey.get_jockey_by_runner(self)

	@property
	def race(self):
		"""Return the race in which this runner competes"""

		return Race.get_race_by_id(self['race_id'])

	@property
	def trainer(self):
		"""Return the trainer responsible for the runner"""

		return Trainer.get_trainer_by_runner(self)


from .race import Race
from .horse import Horse
from .jockey import Jockey
from .trainer import Trainer
