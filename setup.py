from setuptools import setup, find_packages


setup(
    name='rapidsms-threadless-router',
    version=__import__('threadless_router').__version__,
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
    zip_safe=False,
)
