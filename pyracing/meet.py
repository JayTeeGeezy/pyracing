import locale

from .common import Entity


class Meet(Entity):
	"""A meet represents a collection of races occurring at a given track on a given date"""

	@classmethod
	def get_meet_by_id(cls, id):
		"""Get the single meet with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_meets_by_date(cls, date):
		"""Get a list of meets occurring on the specified date"""

		return sorted(cls.find_or_scrape(
			filter={'date': date},
			scrape=cls.scraper.scrape_meets,
			scrape_args=[date],
			expiry_date=date
			), key=lambda meet: meet['track'])

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('date', 1)])
		cls.create_index([('date', 1), ('scraped_at', 1)])

	def __str__(self):

		return '{track} on {date}'.format(track=self['track'], date=self['date'].strftime(locale.nl_langinfo(locale.D_FMT)))

	@property
	def races(self):
		"""Return a list of races occurring at this meet"""

		if 'races' not in self.cache:
			self.cache['races'] = Race.get_races_by_meet(self)
		return self.cache['races']


from .race import Race
