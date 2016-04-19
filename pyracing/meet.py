from datetime import datetime


class Meet(dict):
	"""A meet represents a collection of races occurring at a given track on a given date"""

	database = None
	scraper = None

	@classmethod
	def delete_expired(cls, filter, expiry_date):
		"""Delete meets matching the specified filter with a scraped_at date prior to expiry_date"""

		for meet in cls.find(dict({'scraped_at': {'$lt': expiry_date}}, **filter)):
			meet.delete()

	@classmethod
	def find(cls, filter):
		"""Get a list of meets matching the specified filter from the database"""

		return [cls(values) for values in cls.database['meets'].find(filter)]

	@classmethod
	def get_meets_by_date(cls, date):
		"""Get a list of meets occurring on the specified date"""

		filter = {'date': date}
		cls.delete_expired(filter, date)
		meets = cls.find(filter)

		if len(meets) < 1:
			meets = [cls(values) for values in cls.scraper.scrape_meets(date)]
			for meet in meets:
				meet['scraped_at'] = datetime.now()
				meet.save()

		return meets

	@classmethod
	def get_meet_by_id(cls, id):
		"""Get the single meet with the specified database ID"""

		values = cls.database['meets'].find_one({'_id': id})
		if values is not None:
			return cls(values)

	def delete(self):
		"""Remove the meet from the database"""

		if '_id' in self and self['_id'] is not None:
			self.database['meets'].delete_one({'_id': self['_id']})

	def save(self):
		"""Save the meet to the database"""

		if '_id' in self and self['_id'] is not None:
			self.database['meets'].replace_one({'_id': self['_id']}, self)
		else:
			self['_id'] = self.database['meets'].insert_one(self).inserted_id