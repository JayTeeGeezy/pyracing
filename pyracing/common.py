from datetime import datetime

from .events import EventManager


class Entity(dict):
	"""Common functionality for racing entities"""

	database = None
	event_manager = EventManager()
	scraper = None

	@classmethod
	def create_index(cls, index):
		"""Create a database index"""

		cls.get_database_collection().create_index(index)

	@classmethod
	def delete_expired(cls, filter, expiry_date):
		"""Delete entities matching the specified filter with a scraped_at date prior to expiry_date"""

		if expiry_date is not None:
			for entity in cls.find(dict({'scraped_at': {'$lt': expiry_date}}, **filter)):
				entity.delete()

	@classmethod
	def find(cls, filter):
		"""Get a list of entities matching the specified filter from the database"""

		return [cls(values) for values in cls.get_database_collection().find(filter)]

	@classmethod
	def find_one(cls, filter):
		"""Get a single entity matching filter from the database"""

		values = cls.get_database_collection().find_one(filter)
		if values is not None:
			return cls(values)

	@classmethod
	def find_or_scrape(cls, filter, scrape, scrape_args=None, scrape_kwargs=None, expiry_date=None):
		"""Get a list of entities by finding them in the database or scraping them from the web"""

		cls.delete_expired(filter, expiry_date)
		entities = cls.find(filter)

		if len(entities) < 1:
			if scrape_args is None: scrape_args = []
			if scrape_kwargs is None: scrape_kwargs = {}
			entities = [cls(values) for values in scrape(*scrape_args, **scrape_kwargs)]
			for entity in entities:
				entity['scraped_at'] = datetime.now()
				entity.save()

		return entities

	@classmethod
	def find_or_scrape_one(cls, filter, scrape, scrape_args=None, scrape_kwargs=None, expiry_date=None):
		"""Get a single entity by finding it in the database or scraping it from the web"""

		cls.delete_expired(filter, expiry_date)
		entity = cls.find_one(filter)

		if entity is None:
			if scrape_args is None: scrape_args = []
			if scrape_kwargs is None: scrape_kwargs = {}
			values = scrape(*scrape_args, **scrape_kwargs)
			if values is not None:
				entity = cls(values)
				entity['scraped_at'] = datetime.now()
				entity.save()

		return entity

	@classmethod
	def get_database_collection(cls):
		"""Get the database collection for this specific entity type"""

		return cls.database[cls.__name__.lower() + 's']

	def delete(self):
		"""Remove the entity from the database"""

		if '_id' in self and self['_id'] is not None:
			self.event_manager.publish_event('deleting_' + self.__class__.__name__.lower(), [self])
			self.get_database_collection().delete_one({'_id': self['_id']})
			self.event_manager.publish_event('deleted_' + self.__class__.__name__.lower(), [self])

	def save(self):
		"""Save the entity to the database"""

		self.event_manager.publish_event('saving_' + self.__class__.__name__.lower(), [self])

		if '_id' in self and self['_id'] is not None:
			self.get_database_collection().replace_one({'_id': self['_id']}, self)
		else:
			self['_id'] = self.get_database_collection().insert_one(self).inserted_id

		self.event_manager.publish_event('saved_' + self.__class__.__name__.lower(), [self])