from setuptools import setup

setup(
    name='astpretty',
    description='Pretty print the output of python stdlib `ast.parse`.',
    url='https://github.com/asottile/astpretty',
    version='1.5.0',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    py_modules=['astpretty'],
    entry_points={'console_scripts': ['astpretty = astpretty:main']},
    extras_require={'typed': ['typed-ast']},
)
