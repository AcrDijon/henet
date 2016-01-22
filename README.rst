henet
=====

**DO NOT USE - IT'S NOT READY**

Web Admin for a Pelican blog with the following features:

- edition, addition & deletion of articles
- cleanup of the reSTructuredText
- live preview
- commenting system with static rendering via a Pelican plugin
  and moderation queue. (comments are files like articles)
- ablity to add new comments via a Javascript snippet

Limitations:

- only works with reStructuredText for now.
- completely unsafe at this point


See https://github.com/AcrDijon/henet/issues for planned features
and ongoing work.

Run it
------

Tweak a config file as described in the next section, then::

    $ pip install https://github.com/AcrDijon/henet/archive/master.zip
    $ henet-server config.ini
    Bottle v0.12.9 server starting up (using WSGIRefServer())...
    Listening on http://localhost:8080/
    Hit Ctrl-C to quit.


Configuration
-------------

Henet uses a configuration file. Example with inline comments::

    [henet]
    # host and port to run Henet
    host = localhost
    port = 8080
    debug = True

    # cache for rst parsing and rendering
    cache_dir = /tmp/henet

    # blog categories
    # by convention, one dir == one article category
    categories = actus
                resultats
                foulees
                pages

    # urls info from pelican we need to link to the published
    # pages
    site_url = http://acr-dijon.org
    article_url = posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/

    # the location of the comments files
    comments_dir = /Users/tarek/Dev/github.com/acr-dijon.org/comments

    # each category has an id (the section name), a title and a directory
    [actus]
    title = Actualités
    path = /Users/tarek/Dev/github.com/acr-dijon.org/content/actu

    [resultats]
    title = Résultats
    path = /Users/tarek/Dev/github.com/acr-dijon.org/content/resultats

    [foulees]
    title = Foulées
    path = /Users/tarek/Dev/github.com/acr-dijon.org/content/foulees

    [pages]
    title = Pages statiques
    path = /Users/tarek/Dev/github.com/acr-dijon.org/content/pages

    # with this flag, you can't add article in that category
    can_create = False


Pelican integration
-------------------

To add the commenting system in Pelican, add the
following in your pelicanconf.py::

    HENET_SERVER = "http://localhost:8080"
    PLUGIN_PATH = '/path/to/henet/plugins'
    PLUGINS = ["henet_comments"]

Then adapt your article template to include the comments
and the form to add comments. Example::

    {% if HENET_SERVER %}
     <form id="henet_comment" action="">
       <input type="hidden" name="article_url" value="{{article.url}}">
       Name: <input type="text" name="author" id="author"/>
       Comment: <input type="text" name="text" id="text"/>
       <button type="button" onclick="post_comment('#henet_comment', {{HENET_SERVER}})">Add comment</button>
     </form>
     <script src="{{HENET_SERVER}}/resources/js/henet.js"></script>
    {% endif %}


Credits
-------

Henet is under MIT and uses some code from:

- rsted
- XXX list all pieces of code I used here and there

It leverages:

- bottle
- bootstrap
