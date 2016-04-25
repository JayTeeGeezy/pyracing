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


class PerformancePropertiesTest(EntityTest):

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
								cls.performance = cls.runner.horse.performances[0]
								break
						break
				break

	def test_actual_distance(self):
		"""The actual_distance property should return the actual distance run by the horse in the winning time for this performance"""

		self.assertEqual(self.performance['distance'] - (self.performance['lengths'] * self.performance.METRES_PER_LENGTH), self.performance.actual_distance)

	def test_momentum(self):
		"""The momentum property should return the average momentum achieved by the horse in this performance"""

		self.assertEqual(self.performance['carried'] * self.performance.speed, self.performance.momentum)

	def test_speed(self):
		"""The speed property should return the average speed achieved by the horse in this performance"""

		self.assertEqual(self.performance.actual_distance / self.performance['winning_time'], self.performance.speed)