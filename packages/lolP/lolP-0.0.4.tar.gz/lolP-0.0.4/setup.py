"""A setuptools based setup module.
See:
https://packaging.python.org/tutorials/distributing-packages/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

VERSION = '0.0.4'

SCIPY_MIN_VERSION = '0.13.3'
NUMPY_MIN_VERSION = '1.8.2'
SKLEARN_MIN_VERSION = '0.19.1'

setup(
    name='lolP',
    version=VERSION,
    description='Linear Optimal Low Rank Projection',
    url='https://github.com/neurodata/lollipop',
    author='Jaewon Chung',
    author_email='j1c@jhu.edu',
    license='Apache License 2.0',
    keywords='dimensionality reduction',
    packages=['lol'],  # Required
    setup_requires=[
        'numpy>={}'.format(NUMPY_MIN_VERSION),
    ],
    install_requires=[
        'scipy>={}'.format(SCIPY_MIN_VERSION),
        'scikit-learn>={}'.format(SKLEARN_MIN_VERSION),
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ])
