import locale

from kids.cache import cache

from .common import Entity


class Performance(Entity):
	"""A performance represents a the result of a past run for a horse and jockey"""

	METRES_PER_LENGTH = 2.4

	@classmethod
	def get_performance_by_id(cls, id):
		"""Get the single performance with the specified database ID"""

		return cls.find_one({'_id': id})

	@classmethod
	def get_performances_by_horse(cls, horse):
		"""Get a list of performances for the specified horse"""

		return cls.find_or_scrape(
			filter={'horse_url': horse['url']},
			scrape=cls.scraper.scrape_performances,
			scrape_args=[horse['url']]
			)

	@classmethod
	def initialize(cls):
		"""Initialize class dependencies"""

		def handle_deleting_horse(horse):
			for performance in horse.performances:
				performance.delete()

		cls.event_manager.add_subscriber('deleting_horse', handle_deleting_horse)

		cls.create_index([('horse_url', 1)])
		cls.create_index([('horse_url', 1), ('scraped_at', 1)])

	def __str__(self):

		return 'performance for {horse} at {track} on {date}'.format(horse=self.horse, track=self['track'], date=self['date'].strftime(locale.nl_langinfo(locale.D_FMT)))

	@property
	@cache
	def actual_distance(self):
		"""Return the actual distance run by the horse in the winning time"""

		if 'distance' in self and self['distance'] is not None and 'lengths' in self and self['lengths'] is not None:
			return self['distance'] - (self['lengths'] * self.METRES_PER_LENGTH)

	@property
	@cache
	def actual_weight(self):
		"""Return the weight carried by the horse plus the average weight of a racehorse"""

		if 'carried' in self and self['carried'] is not None:
			return self['carried'] + Horse.AVERAGE_WEIGHT

	@property
	@cache
	def horse(self):
		"""Return the actual horse involved in this performance"""

		return Horse.get_horse_by_performance(self)

	@property
	@cache
	def jockey(self):
		"""Return the actual jockey involved in this performance"""

		return Jockey.get_jockey_by_performance(self)

	@property
	@cache
	def momentum(self):
		"""Return the average momentum achieved by the horse during this performance"""

		if self.actual_weight is not None and self.speed is not None:
			return self.actual_weight * self.speed

	@property
	@cache
	def speed(self):
		"""Return the average speed run by the horse during this performance"""

		if self.actual_distance is not None and 'winning_time' in self and self['winning_time'] is not None:
			return self.actual_distance / self['winning_time']


from .horse import Horse
from .jockey import Jockey
