# -*- coding: utf-8 -*-

# Copyright (c) 2016-2018 by University of Kassel and Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.



from setuptools import setup, find_packages

with open('README.rst', 'rb') as f:
    install = f.read().decode('utf-8')
with open('CHANGELOG.rst', 'rb') as f:
    changelog = f.read().decode('utf-8')

long_description = '\n\n'.join((install, changelog))

setup(
    name='pandapower',
    version='1.6.1',
    author='Leon Thurner, Alexander Scheidler',
    author_email='leon.thurner@uni-kassel.de, alexander.scheidler@iee.fraunhofer.de',
    description='Convenient Power System Modelling and Analysis based on PYPOWER and pandas',
    long_description=long_description,
    url='http://www.pandapower.org',
    license='BSD',
    install_requires=["pypower>=5.0.1",
                      "pandas>=0.17.0",
                      "networkx",
                      "numpy",
                      "scipy"],
    extras_require = {":python_version<'3.0'": ["future"]},
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
)
