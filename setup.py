from setuptools import setup, find_packages
from henet import __version__


install_requires = ['bottle', 'python-dateutil', 'beaker',
                    'konfig', 'docutils', 'rst2rst',
                    'python-Levenshtein', 'pelican',
                    'konfig', 'bson', 'waitress',
                    'multiprocessing-logging',
                    'beautifulsoup4']


try:
    import argparse     # NOQA
except ImportError:
    install_requires.append('argparse')


with open('README.rst') as f:
    README = f.read()


classifiers = ["Programming Language :: Python",
               "License :: OSI Approved :: Apache Software License",
               "Development Status :: 1 - Planning"]


setup(name='henet',
      version=__version__,
      packages=find_packages(),
      description=("Pelican admin"),
      long_description=README,
      license='APLv2',
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      henet-server = henet.app:main
      """)
