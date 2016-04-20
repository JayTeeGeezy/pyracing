from .common import *


class GetHistoricalRunnersByRaceTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		cls.race = cls.meet.races[0]
		cls.runners = pyracing.Runner.get_runners_by_race(cls.race)

	def test_types(self):
		"""The get_runners_by_race method should return a list of Runner objects"""

		self.check_types(self.runners, list, pyracing.Runner)

	def test_ids(self):
		"""All Runner objects returned by get_runners_by_race should have a database ID"""
		
		self.check_ids(self.runners)

	def test_race_ids(self):
		"""All Runner objects returned by get_runners_by_race should have a race ID"""

		for runner in self.runners:
			self.assertIn('race_id', runner)
			self.assertEqual(self.race['_id'], runner['race_id'])

	def test_scraped_at_dates(self):
		"""All Runner objects returned by get_runners_by_race should have a scraped_at date"""
		
		self.check_scraped_at_dates(self.runners)

	def test_no_rescrape(self):
		"""Subsequent calls to get_runners_by_race for the same historical date should retrieve data from the database"""

		self.check_no_rescrape(pyracing.Runner.get_runners_by_race, self.race)


class GetFutureRunnersByDateTest(EntityTest):

	def test_rescrape(self):
		"""Subsequent calls to get_runners_by_race for the same future date should replace data in the database"""

		meet = pyracing.Meet.get_meets_by_date(future_date)[0]
		race = meet.races[0]

		self.check_rescrape(pyracing.Runner.get_runner_by_id, pyracing.Runner.get_runners_by_race, race)


class RunnerPropertiesTest(EntityTest):

	def test_race(self):
		"""The race property should return the race in which the runner is competing"""

		meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		race = meet.races[0]
		runner = pyracing.Runner.get_runners_by_race(race)[0]

		self.assertEqual(pyracing.Race.get_race_by_id(runner['race_id']), runner.race)