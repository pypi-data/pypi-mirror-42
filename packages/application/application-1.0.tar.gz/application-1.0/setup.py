from setuptools import setup,find_packages
import os

setup(
    name='application',
    version='1.0',
    packages=['application','models','controllers','schema'],
    include_package_data=True,
    zip_safe=False,
    #packages=find_packages(),
    install_requires=[
        'flask',
        'flask-marshmallow==0.9.0',
        'Flask-Migrate==2.3.0',
        'Flask-MySQLdb==0.2.0',
        'Flask-RESTful==0.3.6',
        'Flask-SQLAlchemy==2.1',
        'marshmallow==2.13.6',
        'marshmallow-sqlalchemy==0.15.0',
        'mysqlclient==1.3.13',
        'SQLAlchemy==1.2.13'

    ],
)
