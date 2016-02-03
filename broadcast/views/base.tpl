<!doctype html>

<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title><%block name="title">Share your content</%block> - Outernet</title>
        % if redirect_url is not UNDEFINED:
        <meta http-equiv="refresh" content="5; url=${redirect_url}">
        % endif
        <link rel="stylesheet" href="${assets['css/main']}">
        % if not DEBUG:
        <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
             (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
             m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
             })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
             ga('create', 'UA-47041607-1', 'auto');
             ga('send', 'pageview');
        </script>
        % endif
        <%block name="extra_head"/>
    </head>
    <body>
        <%block name="header">
        <header class="menu">
            <div class="menu-subblock">
                <a class="logo" href="${url('main')}"><span lang="en">Outernet</span></a>
                <a class="logo-broadcast" href="${url('main')}"></span>${_('Uplink center')}</span></a>
            </div>
            <div class="menu-block-right">
                <nav id="nav" class="menu-subblock toolbar">
                    <a href="http://www.outernet.is/" class="homepage"><span class="label">${_("Home")}</span></a>
                    <a href="#" class="homepage"><span class="label">${_("Contact Us")}</span></a>
                    <a href="#" class="homepage"><span class="label">${_("Guaranteed Delivery")}</span></a>
                </nav>
                <div class="hamburger">
                    <a href="#nav">Site menu</a>
                </div>
            </div>
        </header>
        </%block>

        <div class="section body">
        <%block name="main">
            ${self.body()}
        </%block>
        </div>

        <%block name="footer">
        <footer>
            <p class="logo"><span lang="en">Outernet</span>: ${_("Humanity's Public Library")}</p>
            <p class="copyright">2014-2015 <span lang="en">Outernet Inc</span></p>
        </footer>
        </%block>

        <script type="text/template" id="menu">
            <nav class="alt-menu">
                <div class="level1" id="top">
                    % if request.user.is_authenticated:
                    <a href="${url('logout')}" class="logout"><span class="label">${_("Log out")}</span></a>
                    % else:
                    <a href="${url('login')}" class="login"><span class="label">${_("Login")}</span></a>
                    <a href="${url('register_form')}" class="register"><span class="label">${_("Register")}</span></a>
                    % endif
                </div>
            </nav>
        </script>
        <script src="${assets['js/ui']}"></script>
        <%block name="extra_scripts"/>
    </body>
</html>
