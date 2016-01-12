<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>{{title}} // Henet Admin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />

    <!--CSS-START-->
    <link href="/resources/css/bootstrap.css" rel="stylesheet" />
    <link href="/resources/css/bootstrap-responsive.css" rel="stylesheet" />
    <link href="/resources/css/style.css" rel="stylesheet" />
    <link id="bsdp-css" href="/resources/css/datepicker3.css" rel="stylesheet">
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
                <a class="brand" href="#">Henet Admin</a>
                <div class="nav-collapse collapse">
                    <p class="navbar-text pull-right">
                        Logged in as <a href="#" class="navbar-link">Username</a>
                    </p>
                    <ul class="nav">
                        <li class="active"><a href="#">Home</a></li>
                        <li><a href="#about">About</a></li>
                        <li><a href="#contact">Contact</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="container-fluid">
        <div class="row-fluid">
            <div class="span3">
                <div class="well sidebar-nav">
                    <ul class="nav nav-list">
                        <li class="nav-header">Actions</li>
                        <li><a href="#">Create entry</a></li>

                        <li class="nav-header">Blog categories</li>
                        % for cat in categories.keys():
                        <li><a href="/category/{{ cat }}">{{ cat }}</a></li>
                        % end
                    </ul>
                </div><!--/.well -->
            </div><!--/span-->

            <div class="span9">
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