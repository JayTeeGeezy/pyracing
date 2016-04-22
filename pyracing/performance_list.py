class PerformanceList(list):
	"""A PerformanceList represents a filtered list of performances decorated with statistical calculations"""

	def __init__(self, *args, **kwargs):
		"""Create PerformanceList and ensure it is sorted by date in descending order"""
		super().__init__(*args, **kwargs)

		self.sort(key=lambda performance: performance['date'], reverse=True)