from setuptools import setup, find_packages


setup(
    name='threadless_router',
    version='0.0.1',
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.sql', '*.pyc'],
    },
    url='https://github.com/caktus/rapidsms-threadless-router',
    license='LICENSE.txt',
    description='Threadless router implementation for RapidSMS',
    long_description=open('README.rst').read(),
)
