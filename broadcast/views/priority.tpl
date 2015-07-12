<%inherit file='base.tpl'/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

<%block name="title">
    ${_("Payment")}
</%block>

<%block name="main">
<div class="h-bar">
    <h2>${_('Complete the payment')}</h2>
    % if item.type == 'twitter':
        <p class="priority-help">${_("After completing the payment, your feed will be reviewed by Outernet staff and start broadcasting during Outernet's working hours (week days between 11am and 7pm Chicago time). You can always unsubscribe by emailing us at {email}.").format(email='<a href="mailto:hello@outernet.is">hello@outernet.is</a>')}</p>
    % else:
        <p class="priority-help">${_("After completing the payment, your content will be reviewed by Outernet staff and broadcast during Outernet's working hours (week days between 11am and 7pm Chicago time)")}</p>
    % endif
</div>

<div class="full-page-form">
    % if item.type == 'content':
        <p class="subtotal">
        <strong>
            ${_('''Your card will be charged {amount} after content is
            broadcast.''').format(amount=item.priority_price)}
        </strong>
        </p>
    % elif item.type == 'twitter':
        <p class="subtotal">
        <strong>
            ${_('''Your card will be charged {amount} {period} until
            unsubscribed.''').format(amount=item.plan_price,
            period=item.plan_period)}
        </strong>
        </p>
    % endif
    <div class="priority">
        ${h.form('post', _id='payment-form', action=url('broadcast_priority', item_type=item.type, item_id=item.id))}
            % if form.error:
            ${form.error}
            % elif charge_error:
            ${charge_error}
            % else:
            <ul class="form-errors">
            </ul>
            % endif
            ${csrf_tag()}
            ${form.stripe_public_key}
            <p class="field">
                ${form.email.label}
                ${form.email}
                % if form.email.error:
                ${form.email.error}
                % endif
            </p>
            <p class="field form-input-required">
                ${form.card_number.label}
                ${form.card_number}
                % if form.card_number.error:
                ${form.card_number.error}
                % endif
            </p>
            <div class="inline-fields">
                <p class="field form-input-required cvc">
                    ${form.cvc.label}
                    ${form.cvc}
                    % if form.cvc.error:
                    ${form.cvc.error}
                    % endif
                </p>
                <p class="field form-input-required expiration">
                    ${form.exp_month.label}
                    ${form.exp_month}
                    ${form.exp_year}
                    % if form.exp_month.error:
                    ${form.exp_month.error}
                    % elif form.exp_year.error:
                    ${form.exp_year.error}
                    % endif
                </p>
                <p class="field-help">
                ${_('''CVC number is a 3-digit security code and normally
                appears on the back of the card towards the right edge of the
                signature field, or 4-digit code just above the card number on
                the right.''')}
                </p>
            </div>
            <p class="buttons">
                <button class="primary">${_('Broadcast')}</button>
            </p>
        </form>
    </div>
</div>
</%block>

<%block name="extra_scripts">
    <script type="text/javascript" src="https://js.stripe.com/v2/"></script>
    <script type="text/javascript">
    'use strict';
    window.messages = {
        cardError: "${_('Check the card number')}",
        cvcError: "${_('Check the CVC number')}",
        monthRangeError: "${_('Number entered for month is too small or too big')}",
        dateError: "${_('Enter only numbers for expiry date')}",
        expError: "${_('Check the expiration date on your card')}"
    };
    </script>
    <script src="${assets['js/priority']}"></script>
</%block>
