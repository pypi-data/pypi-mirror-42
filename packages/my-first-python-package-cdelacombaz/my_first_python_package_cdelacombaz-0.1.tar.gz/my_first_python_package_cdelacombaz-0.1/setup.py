from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='my_first_python_package_cdelacombaz',
      version='0.1',
      description='Creating my first Python package',
      long_description=readme(),
      # url='http://github.com/storborg/funniest',
      classifiers=[
          'Programming Language :: Python :: 3.6'
      ],
      author='Cedric Delacombaz',
      author_email='cdelacombaz@bluewin.ch',
      # license='MIT',
      packages=['my_first_python_package_cdelacombaz'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
