from datetime import datetime
import unittest

import pyracing


class PerformanceListTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):

		cls.performances = [
			{
				'result':				10,
				'starters':				13,
				'track':				'Wangaratta',
				'date':					datetime(2016, 4, 21),
				'distance':				1170,
				'track_condition':		'Good 4',
				'runner_prize_money':	500.00,
				'race_prize_money':		20000.00,
				'barrier':				16,
				'winning_time':			68.66,
				'starting_price':		6.50,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Dylan-Dunn_7917/',
				'weight':				60.5,
				'carried':				60.5,
				'lengths':				4.15
			},
			{
				'result':				3,
				'starters':				12,
				'track':				'Echuca',
				'date':					datetime(2016, 4, 10),
				'distance':				1209,
				'track_condition':		'Good 4',
				'runner_prize_money':	1600.00,
				'race_prize_money':		20000.00,
				'barrier':				15,
				'winning_time':			73.2,
				'starting_price':		6.50,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Mark-Pegus_980/',
				'weight':				60.5,
				'carried':				60.5,
				'lengths':				0.30
			},
			{
				'result':				3,
				'starters':				4,
				'track':				'Yarra Valley',
				'date':					datetime(2016, 3, 20),
				'distance':				1200,
				'track_condition':		'Heavy 9',
				'runner_prize_money':	2000.00,
				'race_prize_money':		25000.00,
				'barrier':				4,
				'winning_time':			76.55,
				'starting_price':		2.10,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Ben-Allen_9146/',
				'weight':				60.5,
				'carried':				59.0,
				'lengths':				2.95
			},
			{
				'result':				6,
				'starters':				11,
				'track':				'Sandown Hillside',
				'date':					datetime(2016, 2, 17),
				'distance':				1300,
				'track_condition':		'Soft 5',
				'runner_prize_money':	700.00,
				'race_prize_money':		35000.00,
				'barrier':				4,
				'winning_time':			79.18,
				'starting_price':		9.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Harry-Coffey_3109/',
				'weight':				61.0,
				'carried':				59.5,
				'lengths':				4.35
			},
			{
				'result':				2,
				'starters':				8,
				'track':				'Kilmore',
				'date':					datetime(2016, 2, 1),
				'distance':				1100,
				'track_condition':		'Good 4',
				'runner_prize_money':	3400.00,
				'race_prize_money':		20000.00,
				'barrier':				2,
				'winning_time':			63.6,
				'starting_price':		4.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Ben-E-Thompson_2143/',
				'weight':				61.0,
				'carried':				59.5,
				'lengths':				0.10
			},
			{
				'result':				9,
				'starters':				12,
				'track':				'Wangaratta',
				'date':					datetime(2016, 1, 21),
				'distance':				1300,
				'track_condition':		'Good 4',
				'runner_prize_money':	500.00,
				'race_prize_money':		20000.00,
				'barrier':				12,
				'winning_time':			77.55,
				'starting_price':		8.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Mitchell-Aitken_9402/',
				'weight':				61.0,
				'carried':				58.0,
				'lengths':				5.25
			},
			{
				'result':				1,
				'starters':				14,
				'track':				'Wangaratta',
				'date':					datetime(2016, 1, 4),
				'distance':				1170,
				'track_condition':		'Soft 5',
				'runner_prize_money':	11000.00,
				'race_prize_money':		20000.00,
				'barrier':				5,
				'winning_time':			68.51,
				'starting_price':		10.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Ben-E-Thompson_2143/',
				'weight':				60.0,
				'carried':				58.5,
				'lengths':				0.00
			},
			{
				'result':				5,
				'starters':				11,
				'track':				'Echuca',
				'date':					datetime(2015, 9, 25),
				'distance':				1100,
				'track_condition':		'Good 4',
				'runner_prize_money':	600.00,
				'race_prize_money':		20000.00,
				'barrier':				1,
				'winning_time':			64.42,
				'starting_price':		7.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Jason-Collins_2265/',
				'weight':				59.0,
				'carried':				57.0,
				'lengths':				2.80
			},
			{
				'result':				1,
				'starters':				13,
				'track':				'Echuca',
				'date':					datetime(2015, 9, 5),
				'distance':				1200,
				'track_condition':		'Good 4',
				'runner_prize_money':	13000.00,
				'race_prize_money':		20000.00,
				'barrier':				12,
				'winning_time':			72.04,
				'starting_price':		19.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Jason-Collins_2265/',
				'weight':				58.5,
				'carried':				56.5,
				'lengths':				0.00
			},
			{
				'result':				4,
				'starters':				14,
				'track':				'Echuca',
				'date':					datetime(2015, 8, 17),
				'distance':				1400,
				'track_condition':		'Good 4',
				'runner_prize_money':	900.00,
				'race_prize_money':		20000.00,
				'barrier':				6,
				'winning_time':			85.74,
				'starting_price':		5.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Jason-Benbow_690/',
				'weight':				58.5,
				'carried':				58.5,
				'lengths':				5.25
			},
			{
				'result':				3,
				'starters':				11,
				'track':				'Wodonga',
				'date':					datetime(2015, 7, 29),
				'distance':				1100,
				'track_condition':		'Heavy 9',
				'runner_prize_money':	1200.00,
				'race_prize_money':		15000.00,
				'barrier':				15,
				'winning_time':			67.96,
				'starting_price':		21.00,
				'horse_url':			'/horses/Tycoon-Tony_395471/',
				'jockey_url':			'/jockeys/Jason-Benbow_690/',
				'weight':				58.5,
				'carried':				58.5,
				'lengths':				4.50
			}
		]

		cls.performance_list = pyracing.PerformanceList(cls.performances)

	def test_average_prize_money(self):
		"""The average_prize_money property should return the average prize money per start in the list"""

		self.assertEqual(self.performance_list.total_prize_money / self.performance_list.starts, self.performance_list.average_prize_money)

	def test_average_starting_price(self):
		"""The average_starting_price property should return the average starting price per start in the list"""

		self.assertEqual(sum([performance['starting_price'] for performance in self.performances]) / len(self.performances), self.performance_list.average_starting_price)

	def test_fourths(self):
		"""The fourths property should return the number of fourth placing performances in the list"""

		self.check_result_count(self.performance_list.fourths, 4)

	def test_fourth_pct(self):
		"""The fourth_pct property should return the number of fourths as a percentage of the number of starts"""

		self.check_percentage(self.performance_list.fourths, self.performance_list.fourth_pct)

	def test_places(self):
		"""The places property should return the number of placing (1st, 2nd, 3rd) performances in the list"""

		self.assertEqual(len([performance for performance in self.performances if 1 <= performance['result'] <= 3]), self.performance_list.places)

	def test_place_pct(self):
		"""The place_pct property should return the number of places as a percentage of the number of starts"""

		self.check_percentage(self.performance_list.places, self.performance_list.place_pct)

	def test_roi(self):
		"""The roi property should return the total winning starting prices less the number of starts in the list, as a percentage of the number of starts"""

		self.assertEqual((sum([performance['starting_price'] for performance in self.performances if performance['result'] == 1]) - len(self.performances)) / len(self.performances), self.performance_list.roi)

	def test_seconds(self):
		"""The seconds property should return the number of second placing performances in the list"""

		self.check_result_count(self.performance_list.seconds, 2)

	def test_second_pct(self):
		"""The second_pct property should return the number of seconds as a percentage of the number of starts"""

		self.check_percentage(self.performance_list.seconds, self.performance_list.second_pct)

	def test_starts(self):
		"""The starts property should return the number of performances in the list"""

		self.assertEqual(len(self.performances), self.performance_list.starts)

	def test_thirds(self):
		"""The thirds property should return the number of third placing performances in the list"""

		self.check_result_count(self.performance_list.thirds, 3)

	def test_third_pct(self):
		"""The third_pct property should return the number of thirds as a percentage of the number of starts"""

		self.check_percentage(self.performance_list.thirds, self.performance_list.third_pct)

	def test_total_prize_money(self):
		"""The total_prize_money property should return the total prize money earned in the list"""

		self.assertEqual(sum([performance['runner_prize_money'] for performance in self.performances]), self.performance_list.total_prize_money)

	def test_wins(self):
		"""The wins property should return the number of wins in the list"""

		self.check_result_count(self.performance_list.wins, 1)

	def test_win_pct(self):
		"""The win_pct property should return the number of wins as a percentage of the number of starts"""

		self.check_percentage(self.performance_list.wins, self.performance_list.win_pct)

	def check_percentage(self, input, output):
		"""Check that output returns input expressed as a percentage of the number of starts"""

		self.assertEqual(input / self.performance_list.starts, output)

	def check_result_count(self, property, result):
		"""Check that the specified property returns the count of the performances with the specified result"""

		self.assertEqual(len([performance for performance in self.performances if performance['result'] == result]), property)