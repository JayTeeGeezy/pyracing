from datetime import timedelta

import pyracing


class Iterator:

	def __init__(self, *args, **kwargs):
		"""Initialize instance dependencies"""

		self.args = args
		self.kwargs = kwargs

	def iterate(self, date_from, date_to):
		"""Iterate through all racing data for the given date range"""
		
		if self.must_process_dates:

			next_date = date_from

			while (date_from < date_to and next_date <= date_to) or (date_from > date_to and next_date >= date_to):

				self.process_date(next_date)

				if date_from < date_to:
					next_date += timedelta(days=1)
				else:
					next_date -= timedelta(days=1)

	def process_date(self, date):
		"""Process all racing data for the specified date"""

		if 'date_pre_processor' in self.kwargs and self.kwargs['date_pre_processor'] is not None:
			self.kwargs['date_pre_processor'](date)

		if self.must_process_meets:
			for meet in pyracing.Meet.get_meets_by_date(date):
				self.process_meet(meet)

		if 'date_post_processor' in self.kwargs and self.kwargs['date_post_processor'] is not None:
			self.kwargs['date_post_processor'](date)

	def process_meet(self, meet):
		"""Process the specified meet"""

		if 'meet_pre_processor' in self.kwargs and self.kwargs['meet_pre_processor'] is not None:
			self.kwargs['meet_pre_processor'](meet)

		if self.must_process_races:
			for race in meet.races:
				self.process_race(race)

		if 'meet_post_processor' in self.kwargs and self.kwargs['meet_post_processor'] is not None:
			self.kwargs['meet_post_processor'](meet)

	def process_race(self, race):
		"""Process the specified race"""

		if 'race_pre_processor' in self.kwargs and self.kwargs['race_pre_processor'] is not None:
			self.kwargs['race_pre_processor'](race)

		if self.must_process_runners:
			for runner in race.runners:
				self.process_runner(runner)

		if 'race_post_processor' in self.kwargs and self.kwargs['race_post_processor'] is not None:
			self.kwargs['race_post_processor'](race)

	def process_runner(self, runner):
		"""Process the specified runner"""

		if 'runner_pre_processor' in self.kwargs and self.kwargs['runner_pre_processor'] is not None:
			self.kwargs['runner_pre_processor'](runner)

		if self.must_process_horses:
			self.process_horse(runner.horse)

		if self.must_process_jockeys:
			self.process_jockey(runner.jockey)

		if self.must_process_trainers:
			self.process_trainer(runner.trainer)

		if 'runner_post_processor' in self.kwargs and self.kwargs['runner_post_processor'] is not None:
			self.kwargs['runner_post_processor'](runner)

	def process_horse(self, horse):
		"""Process the specified horse"""

		if 'horse_pre_processor' in self.kwargs and self.kwargs['horse_pre_processor'] is not None:
			self.kwargs['horse_pre_processor'](horse)

		if self.must_process_performances:
			for performance in horse.performances:
				self.process_performance(performance)

		if 'horse_post_processor' in self.kwargs and self.kwargs['horse_post_processor'] is not None:
			self.kwargs['horse_post_processor'](horse)

	def process_jockey(self, jockey):
		"""Process the specified jockey"""

		if 'jockey_processor' in self.kwargs and self.kwargs['jockey_processor'] is not None:
			self.kwargs['jockey_processor'](jockey)

	def process_trainer(self, trainer):
		"""Process the specified trainer"""

		if 'trainer_processor' in self.kwargs and self.kwargs['trainer_processor'] is not None:
			self.kwargs['trainer_processor'](trainer)

	def process_performance(self, performance):
		"""Process the specified performance"""

		if 'performance_processor' in self.kwargs and self.kwargs['performance_processor'] is not None:
			self.kwargs['performance_processor'](performance)

	@property
	def must_process_dates(self):
		return 'date_pre_processor' in self.kwargs or 'date_post_processor' in self.kwargs or self.must_process_meets

	@property
	def must_process_meets(self):
		return 'meet_pre_processor' in self.kwargs or 'meet_post_processor' in self.kwargs or self.must_process_races

	@property
	def must_process_races(self):
		return 'race_pre_processor' in self.kwargs or 'race_post_processor' in self.kwargs or self.must_process_runners

	@property
	def must_process_runners(self):
		return 'runner_pre_processor' in self.kwargs or 'runner_pre_processor' in self.kwargs or self.must_process_horses or self.must_process_jockeys or self.must_process_trainers

	@property
	def must_process_horses(self):
		return 'horse_pre_processor' in self.kwargs or 'horse_post_processor' in self.kwargs or self.must_process_performances

	@property
	def must_process_jockeys(self):
		return 'jockey_processor' in self.kwargs

	@property
	def must_process_trainers(self):
		return 'trainer_processor' in self.kwargs

	@property
	def must_process_performances(self):
		return 'performance_processor' in self.kwargs