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
             ga('create', 'UA-47041607-10', 'auto');
             ga('send', 'pageview');
        </script>
        % endif
        <%block name="extra_head"/>
    </head>
    <body>
        <%block name="header">
        <header>
            <h1 class="header-logo">
                <a class="logo" href="${url('main')}">${_("Outernet Uplink Center")}</a>
            </h1>
            <div class="header-links">
                <nav id="nav" class="nav">
                    <a href="http://www.outernet.is/" class="homepage"><span class="label">${_("Home")}</span></a>
                    <a href="mailto:hello+uplink@outernet.is" class="homepage"><span class="label">${_("Contact Us")}</span></a>
                    ${h.link_other(_("Rocket Service"), url('rocket_service'), request.path)}
                    % if not request.user.is_authenticated or request.user.is_anonymous:
                    <a href="${url('login_form')}" class="homepage"><span class="label">${_("Login")}</span></a>
                    <a href="${url('register_form')}" class="homepage"><span class="label">${_("Sign Up")}</span></a>
                    % endif
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
            <p class="copyright">2014-2015 <span lang="en">Outernet Inc</span></p>
        </footer>
        </%block>
        <script src="${assets['js/ui']}"></script>
        <%block name="extra_scripts"/>
    </body>
</html>
