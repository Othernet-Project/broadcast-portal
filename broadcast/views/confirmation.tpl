<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row auth">
            <div class="col confirm">
                ${h.form('post', action=url('send_confirmation'))}
                    % if form.error:
                    ${form.error}
                    % endif
                    ${csrf_tag()}
                    <p>
                        ${form.email.label}
                        ${form.email}
                        % if form.email.error:
                        ${form.email.error}
                        % endif
                    </p>
                    <p>
                        <button type="submit"><span class="icon"></span> ${_('Send confirmation')}</button>
                    </p>
                </form>
            </div>
        </div>
    </div>
</div>
</%block>
