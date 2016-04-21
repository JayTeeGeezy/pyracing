from datetime import timedelta
import locale

import pyracing

from .profiling import log_time
from .threaded_queues import WorkerQueue


class Iterator:

	def __init__(self, threads=1, message_prefix=None, *args, **kwargs):
		"""Initialize instance dependencies"""

		self.threads = threads
		self.worker_queue = WorkerQueue(threads)

		self.message_prefix = 'processing'
		if message_prefix is not None:
			self.message_prefix = message_prefix

		self.args = args
		self.kwargs = kwargs

	def process_dates(self, date_from, date_to):
		"""Process all racing data for the specified date range"""
		
		if self.must_process_dates:

			next_date = date_from

			while (date_from <= date_to and next_date <= date_to) or (date_from > date_to and next_date >= date_to):

				log_time(
					target=self.process_date,
					target_args=[next_date],
					message='{prefix} {date}'.format(prefix=self.message_prefix, date=next_date.strftime(locale.nl_langinfo(locale.D_FMT)))
					)

				if date_from <= date_to:
					next_date += timedelta(days=1)
				else:
					next_date -= timedelta(days=1)

	def process_date(self, date):
		"""Process all racing data for the specified date"""

		if 'date_pre_processor' in self.kwargs and self.kwargs['date_pre_processor'] is not None:
			self.kwargs['date_pre_processor'](date)

		if self.must_process_meets:

			for meet in pyracing.Meet.get_meets_by_date(date):

				self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_meet,
						'target_args': [meet],
						'message': '{prefix} {meet}'.format(prefix=self.message_prefix, meet=meet)
					}
					)

			if self.worker_queue.is_running:
				self.worker_queue.join()

			if self.worker_queue.exception is not None:
				raise self.worker_queue.exception

		if 'date_post_processor' in self.kwargs and self.kwargs['date_post_processor'] is not None:
			self.kwargs['date_post_processor'](date)

	def process_meet(self, meet):
		"""Process the specified meet"""

		if 'meet_pre_processor' in self.kwargs and self.kwargs['meet_pre_processor'] is not None:
			self.kwargs['meet_pre_processor'](meet)

		if self.must_process_races:
			for race in meet.races:
				self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_race,
						'target_args': [race],
						'message': '{prefix} {race}'.format(prefix=self.message_prefix, race=race)
					}
					)

		if 'meet_post_processor' in self.kwargs and self.kwargs['meet_post_processor'] is not None:
			self.kwargs['meet_post_processor'](meet)

	def process_race(self, race):
		"""Process the specified race"""

		if 'race_pre_processor' in self.kwargs and self.kwargs['race_pre_processor'] is not None:
			self.kwargs['race_pre_processor'](race)

		if self.must_process_runners:
			for runner in race.runners:
				self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_runner,
						'target_args': [runner],
						'message': '{prefix} {runner}'.format(prefix=self.message_prefix, runner=runner)
					}
					)

		if 'race_post_processor' in self.kwargs and self.kwargs['race_post_processor'] is not None:
			self.kwargs['race_post_processor'](race)

	def process_runner(self, runner):
		"""Process the specified runner"""

		if 'runner_pre_processor' in self.kwargs and self.kwargs['runner_pre_processor'] is not None:
			self.kwargs['runner_pre_processor'](runner)

		if self.must_process_horses and runner.horse is not None:
			self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_horse,
						'target_args': [runner.horse],
						'message': '{prefix} {horse}'.format(prefix=self.message_prefix, horse=runner.horse)
					}
					)

		if self.must_process_jockeys and runner.jockey is not None:
			self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_jockey,
						'target_args': [runner.jockey],
						'message': '{prefix} {jockey}'.format(prefix=self.message_prefix, jockey=runner.jockey)
					}
					)

		if self.must_process_trainers and runner.trainer is not None:
			self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_trainer,
						'target_args': [runner.trainer],
						'message': '{prefix} {trainer}'.format(prefix=self.message_prefix, trainer=runner.trainer)
					}
					)

		if 'runner_post_processor' in self.kwargs and self.kwargs['runner_post_processor'] is not None:
			self.kwargs['runner_post_processor'](runner)

	def process_horse(self, horse):
		"""Process the specified horse"""

		if 'horse_pre_processor' in self.kwargs and self.kwargs['horse_pre_processor'] is not None:
			self.kwargs['horse_pre_processor'](horse)

		if self.must_process_performances:
			for performance in horse.performances:
				self.worker_queue.add_item(
					target=log_time,
					target_kwargs={
						'target': self.process_performance,
						'target_args': [performance],
						'message': '{prefix} {performance}'.format(prefix=self.message_prefix, performance=performance)
					}
					)

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
		return 'race_pre_processor' in self.kwargs or 'race_post_processor' in self.kwargs or self.must_process_performances

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