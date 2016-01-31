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


