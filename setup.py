from setuptools import setup

setup(
    name='PyDashie',
    version='0.2dev',
    packages=['pydashie',],
    license='MIT',
    long_description=open('README.rst').read(),
    scripts=['bin/pydashie'],
    install_requires=[
        'flask',
        'CoffeeScript',
        'requests',
        'compago'
    ]
)
