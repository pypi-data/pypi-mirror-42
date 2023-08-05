=============================
negative-i18n
=============================

.. image:: https://badge.fury.io/py/negative-i18n.png
    :target: http://badge.fury.io/py/negative-i18n

.. image:: https://travis-ci.org/negative-space/negative-i18n.png?branch=master
    :target: https://travis-ci.org/negative-space/negative-i18n

Database-stored translation strings for Django


Features
--------

* Strore translations in database
* Download translations as po file
* Import translations from po file
* Simple admin interface for editing translations
* Instant refresh of translation strings
* negative-inline-editor integration


Installation
---------------

pip install negative-i18n

Add 'negative_i18n' to installed apps.


Configuration
------------------

settings.COLLECT_I18N_STATS
default: True
meaning: collect strings to database


Usage in templates
---------------------

{% load negative_i18n %}

<div>
    <h1>{{ 'i18n test'|_ }}</h1>
</div>


Usage in views
-------------------

from negative_i18n.trans_utils import _

_('Some text')

