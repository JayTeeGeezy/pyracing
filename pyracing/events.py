class EventManager:
	"""Implement a publisher/subscriber model event manager"""

	def __init__(self):
		"""Initialize instance dependencies"""

		self.subscribers = {}

	def add_subscriber(self, event, subscriber):
		"""Add subscriber to the specified event"""

		if not event in self.subscribers:
			self.subscribers[event] = []

		if not subscriber in self.subscribers[event]:
			self.subscribers[event].append(subscriber)

	def publish_event(self, event, args=None, kwargs=None):
		"""Publish an event to subscribers"""

		if event in self.subscribers:

			if args is None: args = []
			if kwargs is None: kwargs = {}

			for subscriber in self.subscribers[event]:
				subscriber(*args, **kwargs)