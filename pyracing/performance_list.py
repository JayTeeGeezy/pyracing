class PerformanceList(list):
	"""A PerformanceList represents a filtered list of performances decorated with statistical calculations"""

	def __init__(self, *args, **kwargs):
		"""Create PerformanceList and ensure it is sorted by date in descending order"""
		super().__init__(*args, **kwargs)

		self.sort(key=lambda performance: performance['date'], reverse=True)

	@property
	def starts(self):
		"""Return the number of starts included in this performance list"""

		return len(self)

	@property
	def wins(self):
		"""Return the number of wins included in this performance list"""

		return len([performance for performance in self if performance['result'] == 1])