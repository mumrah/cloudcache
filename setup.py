from setuptools import setup,find_packages

setup (
  name = 'CloudCached',
  version = '0.1',
  install_requires = {'Boto':'boto>=1.8','Nose':'nose>=0.11'},
  packages = find_packages(),
  tests_require = {'Nose':'nose>=0.1'},
  test_suite = "nose.collector",
  author = 'David Arthur',
  author_email = 'mumrah@gmail.com',
)
