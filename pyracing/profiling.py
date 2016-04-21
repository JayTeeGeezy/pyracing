from datetime import datetime
import logging


def log_time(target, message, log_method=None, target_args=None, target_kwargs=None):
	"""Execute target and log the start/elapsed time before and after execution"""

	logger = logging.info
	if log_method is not None:
		logger = log_method

	start_time = datetime.now()
	logger('Started {message} at {start_time}'.format(message=message, start_time=start_time))

	if target_args is None: target_args=[]
	if target_kwargs is None: target_kwargs={}
	output = target(*target_args, **target_kwargs)

	logger('Finished {message} in {elapsed_time}'.format(message=message, elapsed_time=datetime.now() - start_time))
	return output