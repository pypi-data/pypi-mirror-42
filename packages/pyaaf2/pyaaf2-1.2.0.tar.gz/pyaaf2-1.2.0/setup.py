import sys
import os
from setuptools import setup
import setuptools.command.build_py

PROJECT_METADATA = {
    "version": "1.2.0",
    "author": 'Mark Reid',
    "author_email": 'mindmark@gmail.com',
    "license": 'MIT',
}

METADATA_TEMPLATE = """
__version__ = "{version}"
__author__ = "{author}"
__author_email__ = "{author_email}"
__license__ = "{license}"
"""


class AddMetadata(setuptools.command.build_py.build_py):
    """Stamps PROJECT_METADATA into __init__ files."""

    def run(self):
        setuptools.command.build_py.build_py.run(self)

        if self.dry_run:
            return

        target_file = os.path.join(self.build_lib, 'aaf2', "__init__.py")
        source_file = os.path.join(os.path.dirname(__file__), 'aaf2', "__init__.py")

        # get the base data from the original file
        with open(source_file, 'r') as fi:
            src_data = fi.read()

        # write that + the suffix to the target file
        with open(target_file, 'w') as fo:
            fo.write(src_data)
            fo.write(METADATA_TEMPLATE.format(**PROJECT_METADATA))

setup(
    name='pyaaf2',
    description='A python module for reading and writing advanced authoring format files',
    url='https://github.com/markreidvfx/pyaaf2',
    project_urls={
        'Source':
            'https://github.com/markreidvfx/pyaaf2',
        'Documentation':
            'http://pyaaf.readthedocs.io',
        'Issues':
            'https://github.com/markreidvfx/pyaaf2/issues',
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    keywords='film tv editing editorial edit non-linear edl time',

    platforms='any',

    packages=[
        'aaf2',
        'aaf2.model',
        'aaf2.model.ext',
    ],

    cmdclass={'build_py': AddMetadata},

    **PROJECT_METADATA
)
