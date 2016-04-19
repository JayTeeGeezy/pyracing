from datetime import datetime
import unittest

import cache_requests
from lxml import html
import pymongo
import pypunters
import pyracing


class GetHistoricalMeetsByDateTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):

		database = pymongo.MongoClient()['pyracing_test']

		http_client = cache_requests.Session()
		html_parser = html.fromstring
		scraper = pypunters.Scraper(http_client, html_parser)

		pyracing.initialize(database, scraper)

		cls.date = datetime(2016, 2, 1)

		cls.meets = pyracing.Meet.get_meets_by_date(cls.date)

	def test_types(self):
		"""The get_meets_by_date method should return a list of Meet objects"""
		
		self.assertIsInstance(self.meets, list)
		self.assertGreater(len(self.meets), 0)
		for meet in self.meets:
			self.assertIsInstance(meet, pyracing.Meet)

	def test_ids(self):
		"""All Meet objects returned by get_meets_by_date should have a database ID"""
		
		for meet in self.meets:
			self.assertIn('_id', meet)
			self.assertIsNotNone(meet['_id'])

	def test_scraped_at_dates(self):
		"""All Meet objects returned by get_meets_by_date should have a scraped_at date"""
		
		for meet in self.meets:
			self.assertIn('scraped_at', meet)
			self.assertIsNotNone(meet['scraped_at'])

	def test_no_rescrape(self):
		"""Subsequent calls to get_meets_by_date for the same historical date should retrieve data from the database"""

		old_ids = [meet['_id'] for meet in self.meets]

		new_ids = [meet['_id'] for meet in pyracing.Meet.get_meets_by_date(self.date)]

		for new_id in new_ids:
			self.assertIn(new_id, old_ids)