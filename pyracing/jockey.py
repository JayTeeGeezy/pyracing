from .common import Entity


class Jockey(Entity):
	"""A jockey represents the human riding a runner"""

	@classmethod
	def get_jockey_by_id(cls, id):
		"""Get the single jockey with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_jockey_by_runner(cls, runner):
		"""Get the jockey for the specified runner"""

		if 'jockey_url' in runner and runner['jockey_url'] is not None:
			return cls.find_or_scrape_one(
				filter={'url': runner['jockey_url']},
				scrape=cls.scraper.scrape_jockey,
				scrape_args=[runner['jockey_url']],
				expiry_date=runner.race['start_time']
				)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('url', 1)])
		cls.create_index([('url', 1), ('scraped_at', 1)])