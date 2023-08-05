from setuptools import setup, find_packages


def readme():
	with open('./README.md') as f:
		return f.read()


setup(
	name='atlantis',
	version='0.1',
	license='MIT',

	url='https://github.com/idin/atlantis',
	author='Idin',
	author_email='py@idin.ca',

	description='Python library for natural language processingpython setup.py sdist bdist_wheel',
	long_description=readme(),
	long_description_content_type='text/markdown',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],

	packages=find_packages(exclude=["jupyter_tests", ".idea", ".git"]),
	install_requires=[],
	python_requires='~=3.6',
	zip_safe=False
)