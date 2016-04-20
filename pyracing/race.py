from .common import Entity


class Race(Entity):
	"""A race represents a collection of runners competing in a single event at a given meet"""

	@classmethod
	def get_race_by_id(cls, id):
		"""Get the single race with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_races_by_meet(cls, meet):
		"""Get a list of races occurring on the specified date"""

		races = cls.find_or_scrape(
			filter={'meet_id': meet['_id']},
			scrape=cls.scraper.scrape_races,
			scrape_args=[meet],
			expiry_date=meet['date']
			)

		for race in races:
			if not 'meet_id' in race:
				race['meet_id'] = meet['_id']
				race.save()

		return races

	@property
	def meet(self):
		"""Return the meet at which this race occurs"""

		return Meet.get_meet_by_id(self['meet_id'])


from .meet import Meet