from datetime import datetime


class Meet(dict):
	"""A meet represents a collection of races occurring at a given track on a given date"""

	database = None
	scraper = None

	@classmethod
	def get_meets_by_date(cls, date):
		"""Get a list of meets occurring on the specified date"""

		meets = [cls(values) for values in cls.database['meets'].find({'date': date})]

		if len(meets) < 1:
			meets = [cls(values) for values in cls.scraper.scrape_meets(date)]
			for meet in meets:
				meet['scraped_at'] = datetime.now()
				meet.save()

		return meets

	def save(self):
		"""Save the meet to the database"""

		if '_id' in self and self['_id'] is not None:
			self.database['meets'].replace_one({'_id': self['_id']}, self)
		else:
			self['_id'] = self.database['meets'].insert_one(self).inserted_id