<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Payment")}
</%block>

<%block name="main">
    <div class="form">
        <h2>${_('Payment')}</h2>
        % if item.type == 'twitter':
            <p class="priority-help">
                ${_("{amount} will be charged {period} until you unsubscribe "
                    "from this service. Your card will not be charged until "
                    "the subscription is approved by Outernet staff.".format(
                        amount=th.hamount(th.plan_price(item, charge)),
                        period=th.plan_period(charge)
                    )
                )}
            </p>
        % else:
            <p class="priority-help">
                ${_("A one time {amount} accelerated review fee will be charged "
                    "immediately. Your submission will be reviewed within 24 "
                    "hours after we receive your payment.".format(
                        amount=th.hamount(th.plan_price(item, charge))
                    )
                )}
            </p>
        % endif

        ${h.form('post', _id='payment-form', action=url('broadcast_priority', item_type=item.type, item_id=item.id))}
            % if form.error:
            ${forms.form_errors([form.error])}
            % elif charge_error:
            ${forms.form_errors([charge_error.message])}
            % endif
            ${csrf_tag()}
            ${forms.field(form.stripe_public_key)}
            % if item.email:
            ${h.HIDDEN('email', item.email)}
            % else:
            ${forms.field(form.email, required=True)}
            % endif
            ${forms.field(form.card_number, required=True)}
            <div class="inline-fields">
                <p class="field required" id="field-cvc">
                    ${forms.label(form.cvc.label, id=form.cvc.name)}
                    ${forms.input(form.cvc.name, type=form.cvc.type, value=form.cvc.value, **form.cvc.options)}
                </p>
                <p class="field required" id="field-expiration">
                    ${forms.label(form.exp_month.label, id=form.exp_month.name)}
                    ${forms.input(form.exp_month.name, type=form.exp_month.type, value=form.exp_month.value, **form.exp_month.options)}
                    ${forms.input(form.exp_year.name, type=form.exp_year.type, value=form.exp_year.value, **form.exp_year.options)}
                    % if form.exp_month.error:
                        ${forms.field_error(form.exp_month.error)}
                    % elif form.exp_year.error:
                        ${forms.field_error(form.exp_year.error)}
                    % endif
                </p>
            </div>
            <p class="field-help-message">
                ${_('''CVC is a 3- or 4-digit security number found on the 
                back of your card, usually in the top-right corner of 
                the signature field.''')}
            </p>
            <p class="buttons">
                <button class="primary">${_('Finish')}</button>
            </p>
        </form>
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
        expError: "${_('Check the expiration date on your card')}",
        emailError: "${_('Please enter a valid email address')}"
    };
    </script>
    <script src="${assets['js/priority']}"></script>
</%block>
