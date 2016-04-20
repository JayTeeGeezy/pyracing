from datetime import timedelta

import pyracing


def iterate(date_from, date_to, **kwargs):
	"""Iterate through all racing data for the given date range"""
	
	next_date = date_from

	while (date_from < date_to and next_date <= date_to) or (date_from > date_to and next_date >= date_to):

		if 'date_pre_processor' in kwargs and kwargs['date_pre_processor'] is not None:
			kwargs['date_pre_processor'](next_date)

		for meet in pyracing.Meet.get_meets_by_date(next_date):

			if 'meet_pre_processor' in kwargs and kwargs['meet_pre_processor'] is not None:
				kwargs['meet_pre_processor'](meet)

			for race in meet.races:

				if 'race_pre_processor' in kwargs and kwargs['race_pre_processor'] is not None:
					kwargs['race_pre_processor'](race)

				for runner in race.runners:

					if 'runner_pre_processor' in kwargs and kwargs['runner_pre_processor'] is not None:
						kwargs['runner_pre_processor'](runner)

					if 'horse_pre_processor' in kwargs and kwargs['horse_pre_processor'] is not None:
						kwargs['horse_pre_processor'](runner.horse)

					for performance in runner.horse.performances:

						if 'performance_processor' in kwargs and kwargs['performance_processor'] is not None:
							kwargs['performance_processor'](performance)

					if 'horse_post_processor' in kwargs and kwargs['horse_post_processor'] is not None:
						kwargs['horse_post_processor'](runner.horse)

					if 'jockey_processor' in kwargs and kwargs['jockey_processor'] is not None:
						kwargs['jockey_processor'](runner.jockey)

					if 'trainer_processor' in kwargs and kwargs['trainer_processor'] is not None:
						kwargs['trainer_processor'](runner.trainer)

					if 'runner_post_processor' in kwargs and kwargs['runner_post_processor'] is not None:
						kwargs['runner_post_processor'](runner)

				if 'race_post_processor' in kwargs and kwargs['race_post_processor'] is not None:
					kwargs['race_post_processor'](race)

			if 'meet_post_processor' in kwargs and kwargs['meet_post_processor'] is not None:
				kwargs['meet_post_processor'](meet)

		if 'date_post_processor' in kwargs and kwargs['date_post_processor'] is not None:
			kwargs['date_post_processor'](next_date)

		if date_from < date_to:
			next_date += timedelta(days=1)
		else:
			next_date -= timedelta(days=1)