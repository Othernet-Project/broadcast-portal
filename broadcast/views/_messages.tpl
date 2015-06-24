<%def name="messages(form)">
    <script type="text/javascript">
        window.messages = {};
        window.messages._form = {};
        % for type, message in form.messages.items():
        window.messages._form.${type} = "${message.replace('"', '\\"')}";
        % endfor
        % for field, messages in form.field_messages.items():
        window.messages.${field} = {};
        % for type, message in messages.items():
        window.messages.${field}.${type} = "${message.replace('"', '\\"')}";
        % endfor
        % endfor
    </script>
</%def>
