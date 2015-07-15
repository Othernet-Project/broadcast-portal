<!doctype html>

<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title><%block name="title">Share your content</%block> - Outernet</title>
        <link rel="stylesheet" href="${assets['css/main']}">
    </head>
    <body>
        <div class="section body">
        <%block name="main">
            ${self.body()}
        </%block>
        </div>
    </body>
</html>
