from .common import *


class GetHistoricalRacesByMeetTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		cls.races = pyracing.Race.get_races_by_meet(cls.meet)

	def test_types(self):
		"""The get_races_by_meet method should return a list of Race objects"""

		self.check_types(self.races, list, pyracing.Race)

	def test_ids(self):
		"""All Race objects returned by get_races_by_meet should have a database ID"""
		
		self.check_ids(self.races)

	def test_meet_ids(self):
		"""All Race objects returned by get_races_by_meet should have a meet ID"""

		for race in self.races:
			self.assertIn('meet_id', race)
			self.assertEqual(self.meet['_id'], race['meet_id'])

	def test_scraped_at_dates(self):
		"""All Race objects returned by get_races_by_meet should have a scraped_at date"""
		
		self.check_scraped_at_dates(self.races)

	def test_no_rescrape(self):
		"""Subsequent calls to get_races_by_meet for the same historical date should retrieve data from the database"""

		self.check_no_rescrape(pyracing.Race.get_races_by_meet, self.meet)


class GetFutureRacesByDateTest(EntityTest):

	def test_rescrape(self):
		"""Subsequent calls to get_races_by_meet for the same future date should replace data in the database"""

		meet = pyracing.Meet.get_meets_by_date(future_date)[0]

		self.check_rescrape(pyracing.Race.get_race_by_id, pyracing.Race.get_races_by_meet, meet)


class RacePropertiesTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		cls.race = pyracing.Race.get_races_by_meet(cls.meet)[0]

	def test_meet(self):
		"""The meet property should return the meet at which the race occurs"""

		self.assertEqual(pyracing.Meet.get_meet_by_id(self.race['meet_id']), self.race.meet)

	def test_runners(self):
		"""The runners property should return a list of runners competing in the race"""

		self.assertEqual(pyracing.Runner.get_runners_by_race(self.race), self.race.runners)


class DeleteRaceTest(EntityTest):

	def test_deletes_runners(self):
		"""Deleting a race should also delete any runners competing in that race"""

		meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		race = meet.races[0]
		old_ids = [runner['_id'] for runner in race.runners]

		race.delete()

		for old_id in old_ids:
			self.assertIsNone(pyracing.Runner.get_runner_by_id(old_id))