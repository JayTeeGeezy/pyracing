from .common import *


class GetHistoricalMeetsByDateTest(EntityTest):

	@classmethod
	def setUpClass(cls):

		cls.meets = pyracing.Meet.get_meets_by_date(historical_date)

	def test_types(self):
		"""The get_meets_by_date method should return a list of Meet objects"""

		self.check_types(self.meets, list, pyracing.Meet)

	def test_ids(self):
		"""All Meet objects returned by get_meets_by_date should have a database ID"""
		
		self.check_ids(self.meets)

	def test_scraped_at_dates(self):
		"""All Meet objects returned by get_meets_by_date should have a scraped_at date"""
		
		self.check_scraped_at_dates(self.meets)

	def test_no_rescrape(self):
		"""Subsequent calls to get_meets_by_date for the same historical date should retrieve data from the database"""

		self.check_no_rescrape(pyracing.Meet.get_meets_by_date, historical_date)


class GetFutureMeetsByDateTest(EntityTest):

	def test_rescrape(self):
		"""Subsequent calls to get_meets_by_date for the same future date should replace data in the database"""

		self.check_rescrape(pyracing.Meet.get_meet_by_id, pyracing.Meet.get_meets_by_date, future_date)


class MeetPropertiesTest(EntityTest):

	def test_races(self):
		"""The races property should return a list of races occuring at the meet"""

		meet = pyracing.Meet.get_meets_by_date(historical_date)[0]

		self.assertEqual(pyracing.Race.get_races_by_meet(meet), meet.races)


class DeleteMeetTest(EntityTest):

	def test_deletes_races(self):
		"""Deleting a meet should also delete any races occurring at that meet"""

		meet = pyracing.Meet.get_meets_by_date(historical_date)[0]
		old_ids = [race['_id'] for race in meet.races]

		meet.delete()

		for old_id in old_ids:
			self.assertIsNone(pyracing.Race.get_race_by_id(old_id))