from setuptools import setup, find_packages

setup(
    name='datamodelutils',
    version='0.4.2',
    packages=find_packages(),
    install_requires=[
        'cdisutils',
        'psqlgraph>=1.2.0',
        'dictionaryutils>=1.2.0',
        'gdcdictionary>=0.1.1',
        'gdcdatamodel>=1.1.0',
    ],
    entry_points={
        'console_scripts': [
            'datamodel_postgres_admin=datamodelutils.postgres_admin:main',
            'datamodel_repl=datamodelutils.repl:main'
        ]
    },
)
