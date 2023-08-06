=====
zappa-call-later
=====

zappa-call-later is a simple Django app to queue task using zappa.

Quick start
-----------

1. Add "zappa_call_later" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'zappa_call_later',
    ]

2. Run `python manage.py migrate` to create the call-later models.

