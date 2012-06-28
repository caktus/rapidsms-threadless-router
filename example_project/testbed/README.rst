testbed
=======

Skeleton project to test threadless router.

Installation
------------

Follow these steps::

    ~/rapidsms-threadless-router/example_project/testbed$ mkvirtualenv --distribute testbed
    ~/rapidsms-threadless-router/example_project/testbed$ pip install -U -r requirements.txt
    ~/rapidsms-threadless-router/$ python setup.py develop
    ~/rapidsms-threadless-router/example_project/testbed$ cp localsettings.py.example localsettings.py
    ~/rapidsms-threadless-router/example_project/testbed$ ./manage.py syncdb
    ~/rapidsms-threadless-router/example_project/testbed$ ./manage.py runserver

