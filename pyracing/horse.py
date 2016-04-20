from .common import Entity


class Horse(Entity):
	"""A horse represents the equine component of a runner"""

	@classmethod
	def get_horse_by_id(cls, id):
		"""Get the single horse with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_horse_by_runner(cls, runner):
		"""Get the horse for the specified runner"""

		if 'horse_url' in runner and runner['horse_url'] is not None:
			return cls.find_or_scrape_one(
				filter={'url': runner['horse_url']},
				scrape=cls.scraper.scrape_horse,
				scrape_args=[runner['horse_url']],
				expiry_date=runner.race['start_time']
				)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('url', 1)])
		cls.create_index([('url', 1), ('scraped_at', 1)])

	@property
	def performances(self):
		"""Return a list of performances involving this horse"""

		return Performance.get_performances_by_horse(self)


from .performance import Performance