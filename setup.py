from setuptools import setup, find_packages


setup(
    name='routerq',
    version='0.0.1',
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.sql', '*.pyc'],
    },
    url='http://github.com/caktus/rapidsms-routerq/',
    license='LICENSE.txt',
    description='RapidSMS routerq',
    long_description=open('README.rst').read(),
)
