from datetime import datetime, timedelta
import unittest

import cache_requests
from lxml import html
import pymongo
import pypunters
import pyracing


database = pymongo.MongoClient()['pyracing_test']

http_client = cache_requests.Session()
html_parser = html.fromstring
scraper = pypunters.Scraper(http_client, html_parser)

pyracing.initialize(database, scraper)

historical_date = datetime(2016, 2, 1)
future_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)


class EntityTest(unittest.TestCase):

	def check_ids(self, collection):
		"""Check that all items in the collection have a database ID"""

		for item in collection:
			self.assertIn('_id', item)
			self.assertIsNotNone(item['_id'])

	def check_no_rescrape(self, get_method, *get_args, **get_kwargs):
		"""Check that subsequent calls to get_method retrieve data from the database"""

		old_ids = [item['_id'] for item in get_method(*get_args, **get_kwargs)]

		new_ids = [item['_id'] for item in get_method(*get_args, **get_kwargs)]

		for new_id in new_ids:
			self.assertIn(new_id, old_ids)

	def check_rescrape(self, get_one_method, get_method, *get_args, **get_kwargs):
		"""Check that subsequent calls to get_method replace data in the database"""

		old_ids = [item['_id'] for item in get_method(*get_args, **get_kwargs)]

		new_ids = [item['_id'] for item in get_method(*get_args, **get_kwargs)]

		for old_id in old_ids:
			self.assertIsNone(get_one_method(old_id))
			self.assertNotIn(old_id, new_ids)

	def check_scraped_at_dates(self, collection):
		"""Check that all items in the collection have scraped_at dates"""

		for item in collection:
			self.assertIn('scraped_at', item)
			self.assertIsInstance(item['scraped_at'], datetime)
	
	def check_types(self, collection, collection_type, item_type):
		"""Check that the collection and its items are objects of the correct type"""

		self.assertIsInstance(collection, collection_type)
		self.assertGreater(len(collection), 0)
		for item in collection:
			self.assertIsInstance(item, item_type)