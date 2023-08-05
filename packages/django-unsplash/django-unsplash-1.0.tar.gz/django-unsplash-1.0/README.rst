=====
unsplash
=====

Unsplash is a simple Django app to manage Unsplash photos and use it in your project.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "unsplash" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'unsplash',
    ]

2. Run `python manage.py migrate` to create the unsplash models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an Unsplash Photo (you'll need the Admin app enabled).