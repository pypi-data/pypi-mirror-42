from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='netpy',
      version='0.0.0.1',
      author="nethub",
      author_email="nethub@yandex.ru",
      description="Library for ML",
      long_description=long_description,
      install_requires=['numpy>=1.9.1',
                        'scipy>=0.14',
                        'h5py'],
      packages=find_packages())
