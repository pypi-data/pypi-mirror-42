Django QDQMedia Translations
====================

Installs Django commands to manages translations.

Installation
------------

    pip install --extra-index-url http://pypi.qdqmedia.com:8888/simple djqdqtranslations

Configure
---------

- Add ``djqdqtranslations`` to the INSTALLED_APPS.
- Define the variable THEMES_REPOS in your project settings.


Development
---------------

Install `requirements-dev.txt` into a virtualenv.

Using _virtualenvwrapper_:

    mkvirtualenv djqdqtranslations
    workon djqdqtranslations
    pip install -r requirements-dev.txt


Run tests:

    python -m djqdqtranslations.tests
