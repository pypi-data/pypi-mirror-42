==================================
DjangoCMS plugin for django-formed
==================================

A DjangoCMS plugin which allows you to add a form created with django-formed to your page.

Installation
============

`pip install django-formed django-formed-cmsplugin`

Then add `'formed'` and `'cmsplugin_formed_form'` to your `INSTALLED_APPS` setting.

Configuration
=============

To make the form plugin available in a placeholder add it to the `'plugins'` item of the placeholder
in the `CMS_PLACEHOLDER_CONF` setting.

For example:

::

    CMS_PLACEHOLDER_CONF = {
        'content': {
            'plugins': [
                'FormPlugin'
            ]
        }
    }
