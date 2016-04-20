from .common import Entity


class Performance(Entity):
	"""A performance represents a the result of a past run for a horse and jockey"""

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