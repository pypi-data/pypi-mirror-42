# pylint: disable=missing-docstring
from setuptools import setup
from setuptools import find_packages

setup(name='fritz',
      version='1.0.0-beta.1',
      description='Fritz Machine Learning Library.',
      url='https://github.com/fritzlabs/fritz-python',
      author='Fritz Engineering',
      author_email='engineering@fritz.ai',
      license='MIT',
      zip_safe=False,
      packages=find_packages(),
      install_requires=[
          'requests',
      ],
      extras_require={
          'keras': ['keras', 'tensorflow'],
      })
