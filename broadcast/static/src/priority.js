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
        check = window.check,
        pubKey = $('#id_stripe_public_key').val(),
        paymentForm = $('#payment-form'),
        checkCard,
        checkCvc,
        checkExpiry,
        cardField = $('#id_card_number'),
        yearField = $('#id_exp_year'),
        monthField = $('#id_exp_month'),
        cvcField = $('#id_cvc');

    $.fn.markNegative = function () {
        var el = $(this);
        el.removeClass('positive').addClass('negative');
        return el;
    };

    $.fn.markPositive = function () {
        var el = $(this);
        
        el.addClass('positive').removeClass('negative');
        return el;
    };

    $.fn.togglePositive = function (val) {
        var el = $(this);

        if (val) {
            el.markPositive();
        } else {
            el.markNegative();
        }
        return el;
    };

    $.fn.removeMarks = function () {
        return $(this).removeClass('positive').removeClass('negative');
    };

    checkCard = function () {
        var el = $(this).removeMarks(),
            parent = el.parent('p'),
            isCardValid,
            card = check.extractDigits(el.val());
        parent.clearErrors();
        if (card.length < 16) {
            return;
        }
        isCardValid = check.mod10check(card);
        el.togglePositive(isCardValid);
        if (!isCardValid) {
            parent.markError(window.messages.cardError);
        }
    };

    checkCvc = function () {
        var el = $(this).removeMarks(),
            parent = el.parent('p'),
            card = check.extractDigits(cardField.val()),
            cvc = check.extractDigits(el.val()),
            isCvcValid;
        parent.clearErrors();
        if (!cvc.length) {
            return;
        }
        if (card) {
            isCvcValid = check.cvcCheck(card, cvc);
        } else {
            isCvcValid = cvc.length === 3 || cvc.length === 4;
        }
        el.togglePositive(isCvcValid);
        if (!isCvcValid) {
            parent.markError(window.messages.cvcError);
        }
    };

    checkExpiry = function () {
        var month = monthField.removeMarks().val(),
            year = yearField.removeMarks().val(),
            parent = monthField.parent('p'),
            expiryOK;

        parent.clearErrors();

        if (!month.toString().length || year.toString().length < 2) {
            return;
        }

        month = parseInt(month, 10);
        year = parseInt(year, 10);

        if (isNaN(month) || isNaN(year)) {
            monthField.markNegative();
            yearField.markNegative();
            parent.markError(window.messages.dateError);
            return;
        }

        if (month < 0 || month > 12) {
            monthField.markNegative();
            yearField.markNegative();
            parent.markError(window.messages.monthRangeError);
            return;
        }

        expiryOK = check.expiry(month, year);

        monthField.togglePositive(expiryOK);
        yearField.togglePositive(expiryOK);

        if (!expiryOK) {
            parent.markError(window.messages.expError);
        }
    };

    cardField.input(checkCard);
    cvcField.input(checkCvc);
    monthField.input(checkExpiry);
    yearField.input(checkExpiry);

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
            formErrors.show();
            self.attachHandler();
        } else {
            tokenEl = $('<input type="hidden" name="stripe_token" />').val(response.id);
            paymentForm.append(tokenEl);
            paymentForm.find("[data-stripe=number]").remove();
            paymentForm.find("[data-stripe=cvc]").remove();
            paymentForm.find("[data-stripe=exp-year]").remove();
            paymentForm.find("[data-stripe=exp-month]").remove();
            paymentForm.submit();
        }
    };

    self.submitPayment = function (e) {
        e.preventDefault();
        self.detachHandler();
        Stripe.card.createToken(paymentForm, self.stripeResponseHandler);
    };

    self.attachHandler = function () {
        paymentForm.on('submit', self.submitPayment);
    };

    self.detachHandler = function () {
        paymentForm.off('submit', self.submitPayment);
    };

    self.attachHandler();
}(this, this.jQuery, this.Stripe));
