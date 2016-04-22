class PerformanceList(list):
	"""A PerformanceList represents a filtered list of performances decorated with statistical calculations"""

	def __init__(self, *args, **kwargs):
		"""Create PerformanceList and ensure it is sorted by date in descending order"""
		super().__init__(*args, **kwargs)

		self.sort(key=lambda performance: performance['date'], reverse=True)

	@property
	def fourths(self):
		"""Return the number of fourth placing performances included in this performance list"""

		return self.count_results(4)

	@property
	def seconds(self):
		"""Return the number of second placing performances included in this performance list"""

		return self.count_results(2)

	@property
	def starts(self):
		"""Return the number of starts included in this performance list"""

		return len(self)

	@property
	def thirds(self):
		"""Return the number of third placing performances included in this performance list"""

		return self.count_results(3)

	@property
	def wins(self):
		"""Return the number of winning performances included in this performance list"""

		return self.count_results(1)

	def count_results(self, result):
		"""Return the number of performances in this list with the specified result"""

		return len([performance for performance in self if performance['result'] == result])