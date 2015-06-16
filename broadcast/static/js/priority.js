/**
 * priority.js: priority form code
 *
 * Copyright 2015, Outernet Inc.
 * Some rights reserved.
 *
 * This software is free software licensed under the terms of GPLv3. See
 * COPYING file that comes with the source code, or
 * http://www.gnu.org/licenses/gpl.txt.
 */

(function (window, $, Stripe) {
    'use strict';
    var self = {},
        pubKey = $('#id_stripe_public_key').val(),
        paymentForm = $('#payment-form'),
        paymentButton = paymentForm.find('a.button');

    Stripe.setPublishableKey(pubKey);

    self.stripeResponseHandler = function (status, response) {
        var formErrors,
            tokenEl;
        if (response.error) {
            formErrors = paymentForm.find('.form-errors');

            if (formErrors.length === 0) {
                formErrors = $('<ul class="form-errors"></ul>');
                paymentForm.prepend(formErrors);
            }
            formErrors.append($('<li></li>').text(response.error.message));
            self.attachHandler();
        } else {
            tokenEl = $('<input type="hidden" name="stripe_token" />').val(response.id);
            paymentForm.append(tokenEl);
            paymentForm.find("[data-stripe=number]").remove();
            paymentForm.find("[data-stripe=cvc]").remove();
            paymentForm.find("[data-stripe=exp-year]").remove();
            paymentForm.find("[data-stripe=exp-month]").remove();
            paymentForm.get(0).submit();
        }
    };

    self.submitPayment = function () {
        self.detachHandler();
        Stripe.card.createToken(paymentForm, self.stripeResponseHandler);
    };

    self.attachHandler = function () {
        paymentButton.on('click', self.submitPayment);
    };

    self.detachHandler = function () {
        paymentButton.off('click', self.submitPayment);
    };

    self.attachHandler();
}(this, this.jQuery, this.Stripe));
