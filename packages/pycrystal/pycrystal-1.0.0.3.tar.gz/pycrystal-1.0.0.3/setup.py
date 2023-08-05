from setuptools import setup

setup(
    name='pycrystal',
    version='1.0.0.3',
    author='Evgeny Blokhin, Maxim Losev, Andrey Sobolev',
    author_email='support@tilde.pro',
    description='Utilities for ab initio modeling suite CRYSTAL',
    long_description='The pycrystal Python utilities are good for quick CRYSTAL logs parsing, getting the maximum information, and presenting it in a systematic machine-readable way, as well as preparing and handling the Gaussian LCAO basis sets.',
    url='https://github.com/tilde-lab/pycrystal',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='materials informatics crystal structures crystal-structure crystallography CRYSTAL ab-initio ab-initio-simulations first-principles materials-science',
    packages=['pycrystal'],
    install_requires=['ase==3.16.2', 'pyparsing']
)
