from .common import *


class ProcessorTest(unittest.TestCase):

	def test_all_data(self):
		"""The process_dates method should process all data for the given date range"""

		class TestProcessor(pyracing.Processor):

			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)

				self.pre_processed_items = {}
				self.post_processed_items = {}
				self.processed_items = {}

				self.pre_process_date = self.pre_process_item
				self.pre_process_meet = self.pre_process_item
				self.pre_process_race = self.pre_process_item
				self.pre_process_runner = self.pre_process_item
				self.pre_process_horse = self.pre_process_item

				self.post_process_date = self.post_process_item
				self.post_process_meet = self.post_process_item
				self.post_process_race = self.post_process_item
				self.post_process_runner = self.post_process_item
				self.post_process_horse = self.post_process_item

				self.process_jockey = self.process_item
				self.process_trainer = self.process_item
				self.process_performance = self.process_item

			def pre_process_item(self, item):
				if item.__class__.__name__ not in self.pre_processed_items:
					self.pre_processed_items[item.__class__.__name__] = []
				self.pre_processed_items[item.__class__.__name__].append(item)

			def post_process_item(self, item):
				if item.__class__.__name__ not in self.post_processed_items:
					self.post_processed_items[item.__class__.__name__] = []
				self.post_processed_items[item.__class__.__name__].append(item)

			def process_item(self, item):
				if item.__class__.__name__ not in self.processed_items:
					self.processed_items[item.__class__.__name__] = []
				self.processed_items[item.__class__.__name__].append(item)

		date_from = datetime(2016, 2, 1)
		date_to = datetime(2016, 2, 2)
		processor = TestProcessor(threads=4)
		processor.process_dates(date_from, date_to)

		for cls in (datetime, pyracing.Meet, pyracing.Race, pyracing.Runner, pyracing.Horse):
			for collection in (processor.pre_processed_items, processor.post_processed_items):
				self.assertIn(cls.__name__, collection)
				self.assertGreater(len(collection[cls.__name__]), 0)

		for cls in (pyracing.Jockey, pyracing.Trainer, pyracing.Performance):
			self.assertIn(cls.__name__, processor.processed_items)
			self.assertGreater(len(processor.processed_items[cls.__name__]), 0)