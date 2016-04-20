from .common import *


class IteratorTest(unittest.TestCase):

	def test_all_data(self):
		"""The iterate method should process all data for the given date range"""

		date_from = datetime(2016, 2, 1)
		date_to = datetime(2016, 2, 2)

		pre_processed_items = {}
		def pre_process_item(item):
			if item.__class__.__name__ not in pre_processed_items:
				pre_processed_items[item.__class__.__name__] = []
			pre_processed_items[item.__class__.__name__].append(item)

		post_processed_items = {}
		def post_process_item(item):
			if item.__class__.__name__ not in post_processed_items:
				post_processed_items[item.__class__.__name__] = []
			post_processed_items[item.__class__.__name__].append(item)

		processed_items = {}
		def process_item(item):
			if item.__class__.__name__ not in processed_items:
				processed_items[item.__class__.__name__] = []
			processed_items[item.__class__.__name__].append(item)

		pyracing.iterate(
			date_from=date_from,
			date_to=date_to,
			date_pre_processor=pre_process_item,
			date_post_processor=post_process_item,
			meet_pre_processor=pre_process_item,
			meet_post_processor=post_process_item,
			race_pre_processor=pre_process_item,
			race_post_processor=post_process_item,
			runner_pre_processor=pre_process_item,
			runner_post_processor=post_process_item,
			horse_pre_processor=pre_process_item,
			horse_post_processor=post_process_item,
			jockey_processor=process_item,
			trainer_processor=process_item,
			performance_processor=process_item
			)

		for cls in (datetime, pyracing.Meet, pyracing.Race, pyracing.Runner, pyracing.Horse):
			for collection in (pre_processed_items, post_processed_items):
				self.assertIn(cls.__name__, collection)
				self.assertGreater(len(collection[cls.__name__]), 0)

		for cls in (pyracing.Jockey, pyracing.Trainer, pyracing.Performance):
			self.assertIn(cls.__name__, processed_items)
			self.assertGreater(len(processed_items[cls.__name__]), 0)