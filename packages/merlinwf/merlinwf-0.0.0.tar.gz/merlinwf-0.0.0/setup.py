from setuptools import setup
from setuptools import find_packages

version = "0.0.0"

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='merlinwf',
      version=version,
      description='The building blocks of workflows!',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3.7',
      ],
      keywords='machine learning workflow',
      author='Peter Robinson',
      author_email='robinson96@llnl.gov',
      license='BSD',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
