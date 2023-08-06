from distutils.core import setup
from setuptools import find_packages

setup(name='mllog',
      version='0.0.4',
      description='mllog',
      long_description='mllog',
      author='mllog',
      author_email='mllog@mllog.com',
      url='https://mllog.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'kafka>=1.3.5',
      ]
      )
