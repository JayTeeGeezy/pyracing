from datetime import timedelta
import locale

import pyracing

from .profiling import log_time
from .threaded_queues import WorkerQueue


class Processor:

	def __init__(self, threads=1, message_prefix=None, *args, **kwargs):
		"""Initialize instance dependencies"""

		self.threads = threads
		self.worker_queue = WorkerQueue(threads)

		self.message_prefix = 'processing'
		if message_prefix is not None:
			self.message_prefix = message_prefix

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

		if hasattr(self, 'pre_process_date'):
			self.pre_process_date(date)

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

		if hasattr(self, 'post_process_date'):
			self.post_process_date(date)

	def process_meet(self, meet):
		"""Process the specified meet"""

		if hasattr(self, 'pre_process_meet'):
			self.pre_process_meet(meet)

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

		if hasattr(self, 'post_process_meet'):
			self.post_process_meet(meet)

	def process_race(self, race):
		"""Process the specified race"""

		if hasattr(self, 'pre_process_race'):
			self.pre_process_race(race)

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

		if hasattr(self, 'post_process_race'):
			self.post_process_race(race)

	def process_runner(self, runner):
		"""Process the specified runner"""

		if hasattr(self, 'pre_process_runner'):
			self.pre_process_runner(runner)

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

		if hasattr(self, 'post_process_runner'):
			self.post_process_runner(runner)

	def process_horse(self, horse):
		"""Process the specified horse"""

		if hasattr(self, 'pre_process_horse'):
			self.pre_process_horse(horse)

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

		if hasattr(self, 'post_process_horse'):
			self.post_process_horse(horse)

	@property
	def must_process_dates(self):
		return hasattr(self, 'pre_process_date') or hasattr(self, 'post_process_date') or self.must_process_meets

	@property
	def must_process_meets(self):
		return hasattr(self, 'pre_process_meet') or hasattr(self, 'post_process_meet') or self.must_process_races

	@property
	def must_process_races(self):
		return hasattr(self, 'pre_process_race') or hasattr(self, 'post_process_race') or self.must_process_runners

	@property
	def must_process_runners(self):
		return hasattr(self, 'pre_process_runner') or hasattr(self, 'post_process_runner') or self.must_process_horses or self.must_process_jockeys or self.must_process_trainers

	@property
	def must_process_horses(self):
		return hasattr(self, 'pre_process_horse') or hasattr(self, 'post_process_horse') or self.must_process_performances

	@property
	def must_process_jockeys(self):
		return hasattr(self, 'process_jockey')

	@property
	def must_process_trainers(self):
		return hasattr(self, 'process_trainer')

	@property
	def must_process_performances(self):
		return hasattr(self, 'process_performance')