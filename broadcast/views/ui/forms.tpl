## Conditionally render placeholder
##

<%def name="pholder_attr(text=None)">${u' placeholder="{}"'.format(esc(text)) if text else ''}</%def>

## Render all optional attributes
##

<%def name="opt_attrs(**kwargs)">${u' '.join([u'{}={}'.format(k, v) for (k, v) in kwargs.items()]) | h}</%def>

## Select list option
##

<%def name="option(value, label, selected=False)">
    <option value="${value | h}"${ ' selected' if selected else ''}>${label | h}</option>
</%def>

## Select list
##

<%def name="select(name, choices=[], empty_value=None, value=None, id=None)">
    <%
        choices = choices or context.get(name + '_choices', [])
        # Make a copy to work around caching issues
        choices = [c for c in choices]
        if empty_value:
            choices.insert(0, ('', empty_value))
        current_value = value or request.params.get(name, '')
    %>
    <select name="${name | h}" id="${id or name | h}">
    % for val, label in choices:
        <% selected = val == current_value %>
        ${option(val, label, selected)}
    % endfor
    </select>
</%def>


## Generic input
##

<%def name="input(name, type='text', placeholder=None, value=None, id=None, has_error=False, **kwargs)">
    <% current_value = h.to_unicode(value or request.params.get(name, '')) %>
    <input type="${type | h}" name="${name | h}" id="${id or name | h}" value="${current_value | h}"${self.pholder_attr(placeholder)}${self.opt_attrs(**kwargs)}>
</%def>

## Hidden input
##

<%def name="hidden(name, value, id=None, **kwargs)">
    ${self.input(name, 'hidden', value=value, id=id or name)}
</%def>

## Text input
##

<%def name="text(name, placeholder=None, value=None, id=None, **kwargs)">
    ${self.input(name, 'text', placeholder=placeholder, value=value, id=id)}
</%def>

## Checkbox
##

<%def name="checkbox(name, value, is_checked=None, label=None, id=None)">
    <%
    current_value = request.params.getall(name)
    is_checked = value in current_value if is_checked is None else is_checked
    %>
    <input type="checkbox" id="${id or name | h}" name="${name | h}" value="${value | h}"${' checked' if is_checked else ''}>
    % if label:
        ${self.label(label, inline=True)}
    % endif
</%def>

## Textarea
##

<%def name="textarea(name, placeholder=None, value=None, id=None)">
    <%
    current_value = value or request.params.getall(name)
    %>
    <textarea name="${name | h}" id="${id or name | h}"${self.pholder_attr(placeholder)}>${current_value}</textarea>
</%def>


## Label
##

<%def name="label(label, inline=False, id=None)">
    <label${' for="{}"'.format(id) if id else '' | h} class="field-label${' field-label-inline' if inline else ''}">${label}</label>
</%def>

## Field supplemental information
##

<%def name="field_help(message)">
    <span class="field-help-message">
        ${message | h}
    </span>
</%def>

<%def name="field_error(message)">
    <span class="field-error-message">
        ${message | h}
    </span>
</%def>

<%def name="field_extras(fld)">
    % if fld.options.get('help_text'):
        ${self.field_help(fld.options.get('help_text'))}
    % endif
    % if fld.error:
        ${self.field_error(fld.error)}
    % endif
</%def>

## Field
##
## This def renders a bottle-utils Field instance.
##

<%def name="field(fld, id=None, help=None, required=False)">
    <%
        if help:
            fld.options['help_text'] = help
    %>
    <p class="field${' field-error' if fld.error else ''}${' required' if required else ''}" id="field-${id or fld.name | h}">
        ## Label
        % if fld.type not in ('checkbox', 'radio', 'hidden'):
            <% label = fld.label + ':' if not fld.label.endswith(':') else fld.label %>
            ${self.label(label, id=id or fld.name)}
        % endif

        ## Help text for textarea is rendered above the field but below label
        % if fld.type in ('textarea',):
            ${self.field_extras(fld)}
        % endif

        ## Field
        <span class="field-input">
            % if fld.type in ['text', 'email', 'date', 'password', 'file']:
                ${self.input(fld.name, type=fld.type, value=fld.value, id=id, **fld.options)}
            % elif fld.type == 'hidden':
                ${self.hidden(fld.name, value=fld.value, id=id, **fld.options)}
            % elif fld.type in ['checkbox', 'radio']:
                ${self.checkbox(fld.name, value=fld.expected_value, is_checked=fld.value, id=id)}
            % elif fld.type == 'textarea':
                ${self.textarea(fld.name, placeholder=fld.options.get('placeholder'), value=fld.value, id=id)}
            % elif fld.type == 'select':
                ${self.select(fld.name, fld.choices, value=fld.value, id=id)}
            % endif
        </span>

        ## Help text for non-textarea fields is rendered below the field
        % if fld.type not in ('textarea',):
            ${self.field_extras(fld)}
        % endif
    </p>
</%def>

## Form errors and messages
##

<%def name="form_errors(errors)">
    <%
    if not errors:
        return ''
    %>
    <ul class="o-form-errors">
        % for error in errors:
            <li class="o-form-error">
            ${error | h}
            </li>
        % endfor
    </ul>
</%def>

<%def name="form_message(message)">
    <%
    if not message:
        return ''
    %>
    <p class="o-form-message">
        ${message | h}
    </p>
</%def>
