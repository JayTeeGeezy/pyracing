from .common import Entity


class Horse(Entity):
	"""A horse represents the equine component of a runner"""

	AVERAGE_WEIGHT = 453.592

	@classmethod
	def get_horse_by_id(cls, id):
		"""Get the single horse with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_horse_by_performance(cls, performance):
		"""Get the actual horse involved in the specified performance"""

		if 'horse_url' in performance and performance['horse_url'] is not None:
			return cls.get_horse_by_url(url=performance['horse_url'])

	@classmethod
	def get_horse_by_runner(cls, runner):
		"""Get the actual horse for the specified runner"""

		if 'horse_url' in runner and runner['horse_url'] is not None:
			return cls.get_horse_by_url(url=runner['horse_url'], expiry_date=runner.race['start_time'])

	@classmethod
	def get_horse_by_url(cls, url, expiry_date=None):
		"""Get the horse with the specified profile URL"""

		return cls.find_or_scrape_one(
			filter={'url': url},
			scrape=cls.scraper.scrape_horse,
			scrape_args=[url],
			expiry_date=expiry_date
			)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('url', 1)])
		cls.create_index([('url', 1), ('scraped_at', 1)])

	def __str__(self):

		return 'horse {name}'.format(name=self['name'])

	@property
	def performances(self):
		"""Return a list of performances involving this horse"""

		return Performance.get_performances_by_horse(self)


from .performance import Performance