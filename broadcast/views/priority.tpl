<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

<%block name="title">
    ${_("Payment")}
</%block>

<%block name="main">
<div class="h-bar">
    <h2>${_('Complete the payment')}</h2>
    % if item.type == 'twitter':
        <p class="priority-help">${_("After completing the payment, your feed will be reviewed by Outernet staff and uplinked during Outernet's business hours (Monday-Friday 0900-1700 PDT). You can always unsubscribe by emailing us at {email}.").format(email='<a href="mailto:hello@outernet.is">hello@outernet.is</a>')}</p>
    % else:
        <p class="priority-help">${_("After submitting payment, your content will be reviewed by Outernet staff and uplinked during business hours (Monday-Friday 0900-1700 PDT).")}</p>
    % endif
</div>

<div class="full-page-form">
    % if item.type in ('content', 'tv'):
        <p class="subtotal">
        <strong>
            ${_('''Your card will be charged {amount} after content is
            uplinked.''').format(amount=item.priority_price)}
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
            ${forms.form_errors([form.error])}
            % elif charge_error:
            ${forms.form_errors([charge_error])}
            % endif
            ${csrf_tag()}
            ${forms.field(form.stripe_public_key)}
            ${forms.field(form.email)}
            ${forms.field(form.card_number)}
            ${forms.field(form.cvc)}
            ${forms.field(form.exp_month)}
            ${forms.field(form.exp_year)}
            <p class="field-help">
                ${_('''CVC number is a 3-digit security code and normally
                appears on the back of the card towards the right edge of the
                signature field, or 4-digit code just above the card number on
                the right.''')}
            </p>
            <p class="buttons">
                <button class="primary">${_('Uplink')}</button>
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
