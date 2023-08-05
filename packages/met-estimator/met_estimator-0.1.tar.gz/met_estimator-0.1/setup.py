from setuptools import setup

setup(name='met_estimator',
      version='0.1',
      description='Estimate and classify activity based on accelerometer input',
      url='http://github.com/ms2300/met_estimator',
      author='ms2300',
      author_email='matt.sewall@gmail.com',
      license='MIT',
      packages=['met_estimator'],
      install_requires=[
          'numpy'
      ],
      zip_safe=False)