from setuptools import setup, find_packages

setup(name='parser_speciam_avito',
      version='0.1',
      description='Parser',
      packages=find_packages(),
      install_requires=['requests','bs4','regex'],
      include_package_data=True,
      zip_safe=False)