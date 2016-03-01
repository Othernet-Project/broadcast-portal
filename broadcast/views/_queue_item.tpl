<%namespace name="forms" file="/ui/forms.tpl"/>

% if item:
    <table class="queue queue-item">
        <tr>
            <th>${_("ID")}</th>
            <td>${item.id}</td>
        </tr>

        <tr>
            <th>${_("Created")}</th>
            <td>${item.created.strftime('%b %d, %H:%M UTC')}</td>
        </tr>

        <tr>
            <th>${_("Size")}</th>
            <td>${h.hsize(item.size)}</td>
        </tr>

        <tr>
            <th>${_("Title")}</th>
            <td>${item.title}</td>
        </tr>

        <tr>
            <th>${_("Source")}</th>
            <td>${item.url}</td>
        </tr>

        <tr>
            <th>${_("License")}</th>
            <td>${item.license}</td>
        </tr>

        <tr>
            <th>${_("Language")}</th>
            <td>${item.language}</td>
        </tr>

        <tr>
            <th>${_("Status")}</th>
            <td>${item.status}</td>
        </tr>
    </table>
% else:
    <p>${forms.form_errors([form.error]) if form.error else ''}</p>
% endif
