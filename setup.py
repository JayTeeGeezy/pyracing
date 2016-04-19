from setuptools import setup


def read_text(filename):
	with open(filename) as f:
		return f.read()


setup(
	name='pyracing',
	version='0.0.0',
	description='Python horse racing class library',
	long_description=read_text('README.rst'),
	classifiers=[
		'Development Status :: 1 - Planning',
		'Environment :: No Input/Output (Daemon)',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.4',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	keywords='horse racing',
	url='https://github.com/JayTeeGeezy/pyracing',
	author='Jason Green',
	author_email='JayTeeGeezy@outlook.com',
	license='MIT',
	packages=[
		'pyracing'
	],
	scripts=[
	],
	entry_points={
		'console_scripts': [
		]
	},
	install_requires=[
	],
	test_suite='nose.collector',
	tests_require=[
		'nose'
	],
	dependency_links=[
	],
	include_package_data=True,
	zip_safe=False
	)