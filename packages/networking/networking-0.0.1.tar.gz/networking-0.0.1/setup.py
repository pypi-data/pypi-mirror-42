from distutils.core import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='networking',
    url='https://github.com/eth2-networks/networking',
    version='0.0.1',
    license='BSD 3-clause "New" or "Revised License"',

    packages=['networking'],
    include_package_data=True,

    author="Martijn Reening",
    author_email="m.reening@eth2.nl",

    description="Low-level networking library",
    long_description=long_description,
    long_description_content_type='text/x-rst',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
      ]
)
