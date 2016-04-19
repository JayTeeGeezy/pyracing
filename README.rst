pyracing
=========

Python horse racing class library


Installation
------------

To install the latest release of pyracing to your current Python environment, execute the following command::

	pip install pyracing

Alternatively, to install pyracing from a source distribution, execute the following command from the root directory of the pyracing repository::

	python setup.py install

To install pyracing from a source distribution as a symlink for development purposes, execute the following command from the root directory of the pyracing repository instead::

	python setup.py develop


Usage
-----

To use pyracing, you must first import the pyracing package into your Python interpreter as follows:

	>>> import pyracing


Testing
-------

To run the included test suite, execute the following command from the root directory of the pyracing repository::

	python setup.py test

The above command will ensure all test dependencies are installed in your current Python environment. For more concise output during subsequent test runs, the following command can be executed from the root directory of the pyracing repository instead::

	nosetests
