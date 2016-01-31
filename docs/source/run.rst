Run it
======


Henet is a web app running under Bottle, to install everything required,
it's encouraged to use a virtualenv::

    $ virtualenv .
    $ bin/pip install https://github.com/AcrDijon/henet/archive/master.zip

Once it's installed, the web admin can be run using **henet-server**::

    $ bin/henet-server
    Bottle v0.12.9 server starting up (using WaitressServer())...
    Listening on http://localhost:8080/
    Hit Ctrl-C to quit.

Before running it, make sure you configure everything properly by tweaking
the configuration file.
