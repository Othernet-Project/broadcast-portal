<!doctype html>

<html lang="en">
    <head>
        <meta chaset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; chaset=utf-8">
        <meta name="viewport" content="initial-scale=1">
        <link rel="stylesheet" href="">
        <title><%block name="title">Filecast center</%block></title>
        <%block name="extra_head"/>
    </head>
    <body class="<%block name="body_class">default</%block>">
        ${self.body()}

        <footer id="footer" class="footer"></footer>

        <%block name="pre_script"/>
        <script src=""></script>
        <%block name="post_script"/>
    </body>
</html>
