from .common import Entity


class Trainer(Entity):
	"""A trainer represents the people responsible for maintaining a horse"""

	@classmethod
	def get_trainer_by_id(cls, id):
		"""Get the single trainer with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_trainer_by_runner(cls, runner):
		"""Get the trainer for the specified runner"""

		if 'trainer_url' in runner and runner['trainer_url'] is not None:
			return cls.find_or_scrape_one(
				filter={'url': runner['trainer_url']},
				scrape=cls.scraper.scrape_trainer,
				scrape_args=[runner['trainer_url']],
				expiry_date=runner.race['start_time']
				)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('url', 1)])
		cls.create_index([('url', 1), ('scraped_at', 1)])