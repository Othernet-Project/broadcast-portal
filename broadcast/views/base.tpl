<!doctype html>

<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title><%block name="title">Broadcast your content</%block> - Outernet</title>
        % if redirect is not UNDEFINED:
        <meta http-equiv="refresh" content="5; url=${redirect}">
        % endif
        <link rel="stylesheet" href="${assets['css/main']}">
        <%block name="extra_head"/>
    </head>
    <body>
        <%block name="header">
        <header class="menu">
            <div class="menu-subblock">
                <a class="logo" href="${url('main')}"><span lang="en">Outernet</span></a>
            </div>
            <div class="menu-block-right">
                <nav id="nav" class="menu-subblock toolbar">
                    % if request.user.is_authenticated:
                    <a href="${url('logout')}" class="logout"><span class="label">${_("Log out")}</span></a>
                    % else:
                    <a href="${url('login')}" class="login"><span class="label">${_("Login")}</span></a>
                    <a href="${url('register_form')}" class="register"><span class="label">${_("Register")}</span></a>
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
            <p class="logo"><span lang="en">Outernet</span>: ${_("Humanity's public library")}</p>
            <p class="copyright">2014-2015 <span lang="en">Outernet Inc</span></p>
        </footer>
        </%block>

        <script src="${assets['js/ui']}"></script>
        <%block name="extra_scripts"/>
    </body>
</html>
