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


