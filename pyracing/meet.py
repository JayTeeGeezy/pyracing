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

		return cls.find_or_scrape(
			filter={'date': date},
			scrape=cls.scraper.scrape_meets,
			scrape_args=[date],
			expiry_date=date
			)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		cls.create_index([('date', 1)])
		cls.create_index([('date', 1), ('scraped_at', 1)])

	@property
	def races(self):
		"""Return a list of races occurring at this meet"""

		return Race.get_races_by_meet(self)


from .race import Race
