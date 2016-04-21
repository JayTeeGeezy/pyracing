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
		"""Subsequent calls to get_runners_by_race for the same historical race should retrieve data from the database"""

		self.check_no_rescrape(pyracing.Runner.get_runners_by_race, self.race)


class GetFutureRunnersByDateTest(EntityTest):

	def test_rescrape(self):
		"""Subsequent calls to get_runners_by_race for the same future race should replace data in the database"""

		meet = pyracing.Meet.get_meets_by_date(future_date)[0]
		race = meet.races[0]

		self.check_rescrape(pyracing.Runner.get_runner_by_id, pyracing.Runner.get_runners_by_race, race)


class RunnerPropertiesTest(EntityTest):

	@classmethod
	def setUpClass(cls):
		
		for meet in pyracing.Meet.get_meets_by_date(historical_date):
			if meet['track'] == 'Kilmore':
				cls.meet = meet
				for race in cls.meet.races:
					if race['number'] == 5:
						cls.race = race
						for runner in cls.race.runners:
							if runner['number'] == 1:
								cls.runner = runner
								break
						break
				break

	def test_age(self):
		"""The age property should return the official age of the horse as at the time of the race"""

		self.assertEqual(4, self.runner.age)

	def test_career(self):
		"""The career property should return a PerformanceList containing all of the horse's performances prior to the current race"""

		performance_list = self.runner.career

		self.assertIsInstance(performance_list, pyracing.PerformanceList)
		self.assertEqual(6, len(performance_list))

	def test_horse(self):
		"""The horse property should return the actual horse running in the race"""
		
		self.assertEqual(pyracing.Horse.get_horse_by_runner(self.runner), self.runner.horse)

	def test_jockey(self):
		"""The jockey property should return the actual jockey riding in the race"""
		
		self.assertEqual(pyracing.Jockey.get_jockey_by_runner(self.runner), self.runner.jockey)

	def test_race(self):
		"""The race property should return the race in which the runner is competing"""

		self.assertEqual(pyracing.Race.get_race_by_id(self.runner['race_id']), self.runner.race)

	def test_trainer(self):
		"""The trainer property should return the actual trainer riding in the race"""
		
		self.assertEqual(pyracing.Trainer.get_trainer_by_runner(self.runner), self.runner.trainer)