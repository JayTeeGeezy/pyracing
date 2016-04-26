from .common import *


class GetHistoricalJockeyByRunnerTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		cls.race = cls.meet.races[0]
		cls.runner = cls.race.runners[0]
		cls.jockey = pyracing.Jockey.get_jockey_by_runner(cls.runner)

	def test_type(self):
		"""The get_jockey_by_runner method should return a single Jockey object"""

		self.assertIsInstance(self.jockey, pyracing.Jockey)

	def test_id(self):
		"""The Jockey object returned by get_jockey_by_runner should have a database ID"""
		
		self.check_ids([self.jockey])

	def test_scraped_at_date(self):
		"""The Jockey object returned by get_jockey_by_runner should have a scraped_at date"""
		
		self.check_scraped_at_dates([self.jockey])

	def test_no_rescrape(self):
		"""Subsequent calls to get_jockey_by_runner for the same historical runner should retrieve data from the database"""

		new_jockey = pyracing.Jockey.get_jockey_by_runner(self.runner)

		self.assertEqual(self.jockey['_id'], new_jockey['_id'])


class GetFutureJockeyByRunnerTest(EntityTest):

	def test_rescrape(self):
		"""Subsequent calls to get_jockey_by_runner for the same future runner should replace data in the database"""

		meet = pyracing.Meet.get_meets_by_date(future_date)[0]
		race = meet.races[-1]
		runner = race.runners[0]
		old_jockey = pyracing.Jockey.get_jockey_by_runner(runner)

		new_jockey = pyracing.Jockey.get_jockey_by_runner(runner)

		self.assertNotEqual(old_jockey['_id'], new_jockey['_id'])