import os
from setuptools import setup


def files_in(package, directory):
    paths = []
    for root, dirs, files in os.walk(os.path.join(package, directory)):
        for f in files:
            paths.append(os.path.join(root, f)[(len(package)+1):])
    return paths


additional_files = []
additional_files.extend(files_in('pydashie', 'skeleton'))
additional_files.extend(files_in('pydashie', 'javascripts'))

setup(
    name='PyDashie',
    version='0.2dev',
    packages=['pydashie'],
    package_data={'pydashie': additional_files},
    license='MIT',
    long_description=open('README.md').read(),
    scripts=['bin/pydashie'],
    install_requires=[
        'flask',
        'CoffeeScript',
        'requests',
        'compago',
        'pyScss'
    ]
)
