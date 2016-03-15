% setdefault('page_title', "Henet Admin")
% setdefault('category', None)
% setdefault('page', None)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>{{page_title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />

    <!--CSS-START-->
    <link href="/resources/css/bootstrap.min.css" rel="stylesheet" />
    <link href="/resources/css/bootstrap-theme.min.css" rel="stylesheet" />
    <link href="/resources/css/style.css" rel="stylesheet" />
    <link href="/resources/css/lightbox.min.css" rel="stylesheet" />
    <link id="bsdp-css" href="/resources/css/datepicker3.css" rel="stylesheet">
    <link id="jqta-css" href="/resources/css/jquery-linedtextarea.css"
          rel="stylesheet">
    <link href="/resources/css/jquery.toastmessage.css" rel="stylesheet" />
    <!--CSS-END-->

    <!--[if lt IE 9]>
    <script src="/resources/js/html5.js"></script>
    <![endif]-->
</head>

<body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Henet Admin</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            % for cat_, data  in categories:
                % if cat_ == category:
                <li class="active"><a href="/category/{{ cat_ }}">
                        {{ data['title'] }}</a></li>
                % else:
                <li><a href="/category/{{ cat_ }}">{{ data['title'] }}</a></li>
                % end
            % end

            % for page_, data  in pages:
                % if page_ == page:
                <li class="active"><a href="/page/{{ page_ }}">
                        {{ data['title'] }}</a></li>
                % else:
                <li><a href="/page/{{ page_ }}">{{ data['title'] }}</a></li>
                % end
            % end
            % if use_comments:
              % if category != 'comments':
              <li><a href="/comments"><em><strong>{{_('Moderate')}}</strong></em></a></li>
              % else:
              <li class="active"><a href="/comments"><em><strong>{{_('Moderate')}}</strong></em></a></li>
              % end
            % end
            % if use_media:
              % if category != 'media':
              <li><a href="/media"><em><strong>{{_('Media')}}</strong></em></a></li>
              % else:
              <li class="active"><a href="/media"><em><strong>{{_('Media')}}</strong></em></a></li>
              % end
            % end

          </ul>
        <div class="navbar-right">
         % for lang, label in langs:
          <a href="/{{lang}}" alternate="{{label}}" title="{{label}}"><img src="/resources/images/{{lang}}.png"></img></a>
         % end
        </div>

        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
        <div class="row">
            <div class="span12">
                <!--JS-START-->
                <script src="/resources/js/jquery.min.js"></script>
                <script src="/resources/js/bootstrap.min.js"></script>
                <script src="/resources/js/bootstrap-datepicker.js"></script>
                <script src="/resources/js/bootstrap-datepicker.fr.min.js" charset="UTF-8"></script>
                <!--JS-END-->
                <!-- CONTENT -->
                <div class="row">
                    <div class="span12" id="contentContainer">
                        % for alert in get_alerts():
                        <div class="alert alert-success alert-dismissible" role="alert">
                          <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                          <strong>Info</strong> {{alert}}
                        </div>
                        % end
                        {{!base}}
                    </div>
                </div>
                <!-- END-CONTENT -->
            </div><!--/span-->
        </div><!--/row-->

        <hr>

        <footer>
            <p>&copy; Tarek Ziadé - 2016</p>
        </footer>
    </div><!--/.fluid-container-->
</body>
</html>