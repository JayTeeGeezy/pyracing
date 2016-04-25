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

	def test_actual_weight(self):
		"""The actual_weight property should return the weight of the horse plus the weight carried"""

		self.assertEqual(self.runner.carrying + pyracing.Horse.AVERAGE_WEIGHT, self.runner.actual_weight)

	def test_age(self):
		"""The age property should return the official age of the horse as at the time of the race"""

		self.assertEqual(4, self.runner.age)

	def test_at_distance(self):
		"""The at_distance property should return a PerformanceList containing all prior performances within 100m of the current race distance"""

		self.check_performance_list(self.runner.at_distance, 4)

	def test_at_distance_on_track(self):
		"""The at_distance_on_track property should return a PerformanceList containing all prior performances within 100m of the current race distance on the current track"""

		self.check_performance_list(self.runner.at_distance_on_track, 0)

	def test_calculate_expected_speed(self):
		"""The calculate_expected_speed method should return a tuple containing minimum, maximum and average expected speeds for the runner based on the specified performance list"""

		expected_result = (
			self.runner.career.minimum_momentum / self.runner.actual_weight,
			self.runner.career.maximum_momentum / self.runner.actual_weight,
			self.runner.career.average_momentum / self.runner.actual_weight
			)

		self.assertEqual(expected_result, self.runner.calculate_expected_speed('career'))

	def test_career(self):
		"""The career property should return a PerformanceList containing all of the horse's performances prior to the current race"""

		self.check_performance_list(self.runner.career, 6)

	def test_carrying(self):
		"""The carrying property should return the listed weight less allowances for the runner"""

		self.assertEqual(self.runner['weight'] - self.runner['jockey_claiming'], self.runner.carrying)

	def test_firm(self):
		"""The firm property should return a PerformanceList containing all prior performances on FIRM tracks"""

		self.check_performance_list(self.runner.firm, 0)

	def test_good(self):
		"""The good property should return a PerformanceList containing all prior performances on GOOD tracks"""

		self.check_performance_list(self.runner.good, 4)

	def test_heavy(self):
		"""The heavy property should return a PerformanceList containing all prior performances on HEAVY tracks"""

		self.check_performance_list(self.runner.heavy, 1)

	def test_horse(self):
		"""The horse property should return the actual horse running in the race"""
		
		self.assertEqual(pyracing.Horse.get_horse_by_runner(self.runner), self.runner.horse)

	def test_jockey(self):
		"""The jockey property should return the actual jockey riding in the race"""
		
		self.assertEqual(pyracing.Jockey.get_jockey_by_runner(self.runner), self.runner.jockey)

	def test_on_track(self):
		"""The on_track property should return a PerformanceList containing all prior performances on the current track"""

		self.check_performance_list(self.runner.on_track, 0)

	def test_on_up(self):
		"""The on_up property should return a PerformanceList containing all prior performances with the same UP number"""

		self.check_performance_list(self.runner.on_up, 1)

	def test_race(self):
		"""The race property should return the race in which the runner is competing"""

		self.assertEqual(pyracing.Race.get_race_by_id(self.runner['race_id']), self.runner.race)

	def test_since_rest(self):
		"""The since_rest property should return a PerformanceList contain all prior performances since the horse's last spell of 90 days or more"""

		self.check_performance_list(self.runner.since_rest, 2)

	def test_soft(self):
		"""The soft property should return a PerformanceList containing all prior performances on SOFT tracks"""

		self.check_performance_list(self.runner.soft, 1)

	def test_spell(self):
		"""The spell property should return the number of days since the horse's previous run"""

		self.assertEqual(11, self.runner.spell)

	def test_synthetic(self):
		"""The synthetic property should return a PerformanceList containing all prior performances on SYNTHETIC tracks"""

		self.check_performance_list(self.runner.synthetic, 0)

	def test_trainer(self):
		"""The trainer property should return the actual trainer riding in the race"""
		
		self.assertEqual(pyracing.Trainer.get_trainer_by_runner(self.runner), self.runner.trainer)

	def test_up(self):
		"""The up property should return the number of races run by the horse (including the current race) since the last rest period of 90 days or more"""

		self.assertEqual(3, self.runner.up)

	def test_with_jockey(self):
		"""The with_jockey property should return a PerformanceList containing all prior performances with the same jockey"""

		self.check_performance_list(self.runner.with_jockey, 1)

	def check_performance_list(self, performance_list, expected_length):
		"""Check that the specified performance list has the expected length"""

		self.assertIsInstance(performance_list, pyracing.PerformanceList)
		self.assertEqual(expected_length, len(performance_list))