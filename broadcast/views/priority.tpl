<%inherit file='base.tpl'/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

<%block name="main">
% if item.has_free_mode:
${priority_switch.body()}
% endif

<div class="grid">
    <div class="grid-container">
        <div class="grid-row priority">
            <div class="col">
                <h2>${_("Please provide your creditcard details")}</h2>

                ${h.form('post', _id='payment-form', action=url('broadcast_priority', item_type=item.type, item_id=item.id))}
                    % if form.error:
                    ${form.error}
                    % endif
                    ${csrf_tag()}
                    ${form.stripe_public_key}
                    <p class="field form-input-required">
                        ${form.card_number.label}
                        ${form.card_number}
                        % if form.card_number.error:
                        ${form.card_number.error}
                        % endif
                    </p>
                    <div class="inline-fields">
                        <p class="field form-input-required">
                            ${form.cvc.label}
                            ${form.cvc}
                            % if form.cvc.error:
                            ${form.cvc.error}
                            % endif
                        </p>
                        <p class="field form-input-required">
                            ${form.exp_month.label}
                            ${form.exp_month}
                            ${form.exp_year}
                            % if form.exp_month.error:
                            ${form.exp_month.error}
                            % elif form.exp_year.error:
                            ${form.exp_year.error}
                            % endif
                        </p>
                    </div>
                    <p>
                        <a class="button primary">${_('Charge me %s') % item.priority_price}</a>
                    </p>
                </form>
            </div>
        </div>
    </div>
</div>
</%block>

<%block name="extra_scripts">
    <script type="text/javascript" src="https://js.stripe.com/v2/"></script>
    <script src="${assets['js/priority']}"></script>
</%block>

