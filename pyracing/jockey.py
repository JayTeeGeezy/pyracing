from .common import Entity


class Jockey(Entity):
	"""A jockey represents the human riding a runner"""

	@classmethod
	def get_jockey_by_id(cls, id):
		"""Get the single jockey with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_jockey_by_performance(cls, performance):
		"""Get the actual jockey involved in the specified performance"""

		if 'jockey_url' in performance and performance['jockey_url'] is not None:
			return cls.get_jockey_by_url(url=performance['jockey_url'])

	@classmethod
	def get_jockey_by_runner(cls, runner):
		"""Get the actual jockey riding the specified runner"""

		if 'jockey_url' in runner and runner['jockey_url'] is not None:
			return cls.get_jockey_by_url(url=runner['jockey_url'], expiry_date=runner.race['start_time'])

	@classmethod
	def get_jockey_by_url(cls, url, expiry_date=None):
		"""Get the jockey with the specified profile URL"""

		return cls.find_or_scrape_one(
			filter={'url': url},
			scrape=cls.scraper.scrape_jockey,
			scrape_args=[url],
			expiry_date=expiry_date
			)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('url', 1)])
		cls.create_index([('url', 1), ('scraped_at', 1), ('session_id', 1)])

	def __str__(self):

		return 'jockey {name}'.format(name=self['name'])

	@property
	def performances(self):
		"""Return a list of performances involving this jockey"""

		if not 'performances' in self.cache:
			self.cache['performances'] = Performance.get_performances_by_jockey(self)
		return self.cache['performances']


from .performance import Performance