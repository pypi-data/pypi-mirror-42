============
ECAS B2SHARE
============


Python module to interact with B2SHARE HTTP REST API!

.. note:: This module is not a B2SHARE client and is related to the ECAS use case.


How to install
==============

Using pip
::

   pip install ecasb2share


How to use
==========

Create a client
::

   from ecasb2share.ecasb2shareclient import EcasShare as Client
   client = Client()


Create a draft record
::

   client.create_draft_record(community_id, title, dataset_id)

Docs
====

Build the doc
::

    python setup.py build_sphinx
============
Contributors
============

* Sofiane Bendoukha <bendoukha@dkrz.de>

=========
Changelog
=========


Version 0.0.1b6 2019-02-19
==========================
- Fix default token path

Version 0.0.1b5 2019-02-14
==========================

- Update README
- Fix uploading token
- Fix creating new drafts records (filebucketid)

Version 0.0.1b4 2019-02-12
==========================

- Fixed bug in adding files to records

Version 0.0.1-a0
================

- Added first basic methods



