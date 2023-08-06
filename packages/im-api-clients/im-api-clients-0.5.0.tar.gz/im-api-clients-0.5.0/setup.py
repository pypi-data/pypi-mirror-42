import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='im-api-clients',
    version='0.5.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple client for Inmediate REST API.',
    long_description=README,
    url='https://github.com/ej2015/im_rest_client_python',
    author='Edgar Ji',
    author_email='edgar.ji@insurancemarket.sg',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
