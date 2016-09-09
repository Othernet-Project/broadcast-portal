<!doctype html>

<%namespace name="client_templates" file="_client_templates.mako"/>

<html lang="en">
    <head>
        <meta chaset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; chaset=utf-8">
        <meta name="viewport" content="initial-scale=1">
        <link rel="stylesheet" href="${assets['css/main']}">
        <title><%block name="page_title">Filecaster</%block></title>
        <%block name="extra_head"/>
    </head>
    <body id="top" class="<%block name="body_class">default</%block>" data-last-update="${last_update['timestamp']}" data-update-url="${url('queue:last_update')}">
        <%block name="top"/>
        ${self.body()}
        <%block name="footer"/>
        <%block name="pre_script"/>
        ${client_templates.body()}
        <script src="${assets['js/main']}"></script>
        <%block name="post_script"/>
    </body>
</html>
