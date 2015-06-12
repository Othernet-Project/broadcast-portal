<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row auth">
            <div class="col confirm">
                ${h.form('post', action=url('broadcast'), enctype="multipart/form-data")}
                    % if form.error:
                    ${form.error}
                    % endif
                    ${csrf_tag()}
                    <p class="field form-input-file">
                        ${form.content.label}
                        ${form.content}
                        % if form.content.error:
                        ${form.content.error}
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
