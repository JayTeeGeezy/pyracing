import queue
import threading


class ThreadedQueue(queue.Queue):
	"""Abstract implementation of a multi-threaded queue processor

	To implement a concrete multi-threaded queue processor based on ThreadedQueue, the following methods must be implemented:
	process_item(item)
	"""

	def __init__(self, threads, *args, **kwargs):
		"""Initialize instance dependencies and start the specified number of threads"""
		super().__init__(*args, **kwargs)

		self.exception = None
		self.is_running = False

		self.start(threads)

	def start(self, threads):
		"""Start the specified number of threads"""

		if not self.is_running:
			self.is_running = True

			for thread_count in range(threads):
				thread = threading.Thread(target=self.do_work, daemon=True)
				thread.start()

	def do_work(self):
		"""Repeatedly get items and process them"""

		while self.is_running:

			item = None
			try:
				item = self.get_nowait()
			except queue.Empty:
				pass

			if item is not None:
				try:
					self.process_item(item)
				except BaseException as e:
					self.stop(e)
				finally:
					self.task_done()

	def put(self, item):
		"""Add item to the queue if the queue is running"""

		if self.is_running:
			super().put(item)

	def stop(self, exception=None):
		"""Stop all threads"""

		if self.is_running:
			self.is_running = False

		if exception is not None and self.exception is None:
			self.exception = exception
		
		self.clear()

	def clear(self):
		"""Remove all pending items from the queue without processing them"""

		while not self.empty():
			try:
				self.get_nowait()
				self.task_done()
			except queue.Empty:
				pass


class WorkerQueue(ThreadedQueue):
	"""A concrete implementation of ThreadedQueue that processes worker tasks"""

	def add_item(self, target, target_args=None, target_kwargs=None, callback=None):
		"""Add an item to the queue"""

		self.put({
			'target':			target,
			'target_args':		target_args,
			'target_kwargs':	target_kwargs,
			'callback':			callback
			})

	def process_item(self, item):
		"""Process the specified item"""

		target = item['target']
		target_args = item['target_args']
		target_kwargs = item['target_kwargs']
		callback = item['callback']

		if target_args is None: target_args=[]
		if target_kwargs is None: target_kwargs={}
		output = target(*target_args, **target_kwargs)

		if callback is not None:
			callback(output)