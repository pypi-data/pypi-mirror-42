from setuptools import setup

setup(name='prymer',
      version='1.1',
      description='Return primers for given input sequences',
      long_description='Design and return primer sequences for input DNA sequences.',
      url='https://github.com/jrjhealey/PrYmer',
      author='Joe R. J. Healey',
      author_email='jrj.healey@gmail.com',
      license='MIT',
      packages=['prymer'],
      install_requires=['biopython'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
