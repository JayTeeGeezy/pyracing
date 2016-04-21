from .common import Entity


class Race(Entity):
	"""A race represents a collection of runners competing in a single event at a given meet"""

	@classmethod
	def get_race_by_id(cls, id):
		"""Get the single race with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_races_by_meet(cls, meet):
		"""Get a list of races occurring at the specified meet"""

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

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		def handle_deleting_meet(meet):
			for race in meet.races:
				race.delete()

		cls.event_manager.add_subscriber('deleting_meet', handle_deleting_meet)

		cls.create_index([('meet_id', 1)])
		cls.create_index([('meet_id', 1), ('scraped_at', 1)])

	def __str__(self):

		return 'race {number} at {meet}'.format(number=self['number'], meet=self.meet)

	@property
	def meet(self):
		"""Return the meet at which this race occurs"""

		return Meet.get_meet_by_id(self['meet_id'])

	@property
	def runners(self):
		"""Return a list of the runners competing in this race"""

		return Runner.get_runners_by_race(self)


from .meet import Meet
from .runner import Runner