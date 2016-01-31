Henet
=====

Henet is a web admin application for `Pelican <http://docs.getpelican.com>`_.


Henet has the following features:

- edition, addition & deletion of articles
- cleanup of the reSTructuredText
- live preview
- commenting system with static rendering
- internationalized interface (French & English built-in)

Limitations:

- only works with reStructuredText for now.
- no authentication

See https://github.com/AcrDijon/henet/issues for planned features
and ongoing work.


Quick Start
-----------

Make sure you have the latest Python 2.7.x and the latest virtualenv, then::

    $ virtualenv .
    $ bin/pip install https://github.com/AcrDijon/henet/archive/master.zip
    $ bin/henet-quickstart
    $ bin/henet-server

The web admin will be reachable at http://localhost:8080


More documentation:

.. toctree::
   :maxdepth: 2

   run
   configuration
   pelican
