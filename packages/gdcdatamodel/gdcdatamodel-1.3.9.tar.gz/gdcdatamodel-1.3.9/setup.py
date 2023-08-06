from setuptools import setup, find_packages

setup(
    name='gdcdatamodel',
    version='1.3.9',
    packages=find_packages(),
    install_requires=[
        'pytz>=2016.4',
        'graphviz>=0.4.2',
        'jsonschema>=2.5.1',
        'psqlgraph',
        'dictionaryutils>=1.2.0,<3.0.0',
        'cdisutils',
        'python-dateutil>=2.4.2',
    ],
    package_data={
        "gdcdatamodel": [
            "xml_mappings/*.yaml",
        ]
    },
    entry_points={
        'console_scripts': [
            'gdc_postgres_admin=gdcdatamodel.gdc_postgres_admin:main'
        ]
    },
)
