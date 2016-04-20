from .common import *


class GetHistoricalTrainerByRunnerTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		cls.race = cls.meet.races[0]
		cls.runner = cls.race.runners[0]
		cls.trainer = pyracing.Trainer.get_trainer_by_runner(cls.runner)

	def test_type(self):
		"""The get_trainer_by_runner method should return a single Trainer object"""

		self.assertIsInstance(self.trainer, pyracing.Trainer)

	def test_id(self):
		"""The Trainer object returned by get_trainer_by_runner should have a database ID"""
		
		self.check_ids([self.trainer])

	def test_scraped_at_date(self):
		"""The Trainer object returned by get_trainer_by_runner should have a scraped_at date"""
		
		self.check_scraped_at_dates([self.trainer])

	def test_no_rescrape(self):
		"""Subsequent calls to get_trainer_by_runner for the same historical runner should retrieve data from the database"""

		new_trainer = pyracing.Trainer.get_trainer_by_runner(self.runner)

		self.assertEqual(self.trainer['_id'], new_trainer['_id'])


class GetFutureTrainerByRunnerTest(EntityTest):

	def test_rescrape(self):
		"""Subsequent calls to get_trainer_by_runner for the same future runner should replace data in the database"""

		meet = pyracing.Meet.get_meets_by_date(future_date)[0]
		race = meet.races[0]
		runner = race.runners[0]
		old_trainer = pyracing.Trainer.get_trainer_by_runner(runner)

		new_trainer = pyracing.Trainer.get_trainer_by_runner(runner)

		self.assertNotEqual(old_trainer['_id'], new_trainer['_id'])