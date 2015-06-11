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
        <header>
            <p class="logo">
                Outernet
            </p>
        </header>
        <%block name="main"/>
        <script src="${assets['js/ui']}"></script>
        <%block name="extra_scripts"/>
    </body>
</html>
