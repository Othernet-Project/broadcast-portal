<!doctype html>

<%namespace name="client_templates" file="_client_templates.mako"/>

<html lang="en">
    <head>
        <meta chaset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; chaset=utf-8">
        <meta name="viewport" content="initial-scale=1">
        <link rel="stylesheet" href="${assets['css/main']}">
        <title><%block name="page_title">Filecast center</%block></title>
        <%block name="extra_head"/>
    </head>
    <body id="top" class="<%block name="body_class">default</%block>">
        ${self.body()}

        <footer id="footer" class="footer">
        <%block name="footer"/>
        </footer>

        <%block name="pre_script"/>
        ${client_templates.body()}
        <script src="${assets['js/main']}"></script>
        <%block name="post_script"/>
    </body>
</html>
