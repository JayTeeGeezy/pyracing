from .common import *


class GetPerformancesByHorseTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		cls.race = cls.meet.races[0]
		cls.runner = cls.race.runners[0]
		cls.performances = pyracing.Performance.get_performances_by_horse(cls.runner.horse)

	def test_types(self):
		"""The get_performances_by_horse method should return a list of Performance objects"""

		self.check_types(self.performances, list, pyracing.Performance)

	def test_ids(self):
		"""All Performance objects returned by get_performances_by_horse should have a database ID"""
		
		self.check_ids(self.performances)

	def test_scraped_at_dates(self):
		"""All Performance objects returned by get_performances_by_horse should have a scraped_at date"""
		
		self.check_scraped_at_dates(self.performances)

	def test_no_rescrape(self):
		"""Subsequent calls to get_performances_by_horse for the same horse should retrieve data from the database"""

		self.check_no_rescrape(pyracing.Performance.get_performances_by_horse, self.runner.horse)