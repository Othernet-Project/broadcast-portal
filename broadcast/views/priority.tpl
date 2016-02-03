<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Payment")}
</%block>

<%block name="main">
<div class="h-bar">
    <h2>${_('Payment')}</h2>
    % if item.type == 'twitter':
        <p class="priority-help">${_("{amount} will be charged {period} until you unsubscribe from this service. Your card will not be charged until the subscription is approved by Outernet staff.".format(amount=item.plan_price, period=item.plan_period))}</p>
    % else:
        <p class="priority-help">${_("A one time {amount} accelerated review fee will be charged immediately. Your submission will be reviewed within 24 hours after we receive your payment.".format(amount=item.priority_price))}</p>
    % endif
</div>

<div class="full-page-form">
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
            <div class="inline-fields">
                <p class="o-field field form-input-required cvc">
                    ${forms.label(form.cvc.label, id=form.cvc.name)}
                    ${forms.input(form.cvc.name, type=form.cvc.type, placeholder=form.cvc.options.get('placeholder'), value=form.cvc.value)}
                </p>
                <p class="o-field field form-input-required expiration">
                    ${forms.label(form.exp_month.label, id=form.exp_month.name)}
                    ${forms.input(form.exp_month.name, type=form.exp_month.type, placeholder=form.exp_month.options.get('placeholder'), value=form.exp_month.value)}
                    ${forms.input(form.exp_year.name, type=form.exp_year.type, placeholder=form.exp_year.options.get('placeholder'), value=form.exp_year.value)}
                    % if form.exp_month.error:
                        ${forms.field_error(form.exp_month.error)}
                    % elif form.exp_year.error:
                        ${forms.field_error(form.exp_year.error)}
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
                <button class="primary">${_('Finish')}</button>
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
