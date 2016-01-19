% setdefault('page_title', "Henet Admin")
% setdefault('category', None)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>{{page_title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />

    <!--CSS-START-->
    <link href="/resources/css/bootstrap.css" rel="stylesheet" />
    <link href="/resources/css/bootstrap-responsive.css" rel="stylesheet" />
    <link href="/resources/css/style.css" rel="stylesheet" />
    <link id="bsdp-css" href="/resources/css/datepicker3.css" rel="stylesheet">
    <link id="jqta-css" href="/resources/css/jquery-linedtextarea.css"
          rel="stylesheet">

    <!--CSS-END-->

    <!--[if lt IE 9]>
    <script src="/resources/js/html5.js"></script>
    <![endif]-->
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container-fluid">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </a>
                <a class="brand" href="/">Henet Admin</a>
                <div class="nav-collapse collapse">
                    <p class="navbar-text pull-right">
                        Logged in as <a href="#" class="navbar-link">Username</a>
                    </p>
                    <ul class="nav">
                        % for cat_, __ in categories:
                          % if cat_ == category:
                          <li class="active"><a href="/category/{{ cat_ }}">
                                 {{ cat_ }}</a></li>
                          % else:
                            <li><a href="/category/{{ cat_ }}">{{ cat_ }}</a></li>
                          % end
                        % end
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="container-fluid">
        <div class="row-fluid">
            <div class="span12">
                <!--JS-START-->
                <script src="/resources/js/jquery.js"></script>
                <script src="/resources/js/bootstrap-datepicker.js"></script>
                <script src="/resources/js/bootstrap-datepicker.fr.min.js" charset="UTF-8"></script>
                <!--JS-END-->
                <!-- CONTENT -->
                <div class="row-fluid">
                    <div class="span12" id="contentContainer">
                        %include
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