(function (window, $, _, messages, pwlen) {
    var userField = $('#id_username'),
        emailField = $('#id_email'),
        passwordField = $('#id_password1'),
        confirmField = $('#id_password2'),
        registerForm = $('#register-form'),
        checkUrl = registerForm.data('url'),
        okClass = 'positive',
        emailRe = /^[^@]+@[^@]+$/,
        toggleError,
        checkUserEmail,
        checkUser,
        copyUsername,
        checkEmail,
        checkPassword,
        checkConfirm;

    toggleError = function(result, field, message) {
        var parent = field.parent('p');
        parent.clearErrors();
        if (result) {
            parent.markError(message);
        } else {
            parent.clearErrors();
            field.addClass(okClass);
        }
    };

    checkUserEmail = function () {
        var field = $(this),
            fieldName = field.attr('name');
        $.getJSON(checkUrl, {'account': field.val()}, function (data) {
            var message = messages[fieldName][fieldName + '_taken'];
            toggleError(data.result, field, message);
        });
    };
    
    checkUserEmail = _.debounce(checkUserEmail, 500);

    checkUser = function () {
        var field = $(this),
            parent = field.parent('p'),
            username = field.val();
        field.removeClass(okClass);
        parent.clearErrors();
        if (!username.length) {
            return;
        }
        checkUserEmail.call(this);
    };

    copyUsername = function () {
        if (!emailField.val()) {
            emailField.val(userField.val() + '@');
        }
    };

    checkEmail = function () {
        var field = $(this),
            parent = field.parent('p'),
            email = field.val();
        field.removeClass(okClass);
        parent.clearErrors();
        if (!email.length) {
            return;
        }
        if (emailRe.exec(email) === null) {
            parent.markError(messages.email.email_invalid);
        } else {
            checkUserEmail.call(this);
        }
    };

    checkPassword = function () {
        var field = $(this),
            parent = field.parent('p'),
            password = field.val();
        field.removeClass(okClass);
        parent.clearErrors();
        if (!password.length) {
            parent.markError(messages.password1.required);
        } else if (password.length < pwlen) {
            parent.markError(messages.password1.password_length.
                replace('{length}', pwlen));
        } else {
            field.addClass(okClass);
        }
    };

    checkConfirm = function () {
        var field = $(this),
            parent = field.parent('p'),
            password = passwordField.val(),
            confirm = field.val();
        field.removeClass(okClass);
        parent.clearErrors();
        if (!confirm.length) {
            parent.markError(messages.password2.reuqired);
            return;
        }
        if (password !== confirm) {
            parent.markError(messages._form.pwmatch);
            return;
        } else {
            field.addClass(okClass);
        }
    };

    userField.input(checkUser);
    userField.change(copyUsername);
    emailField.input(checkEmail);
    passwordField.input(checkPassword);
    confirmField.input(checkConfirm);
}(this, this.jQuery, this._, this.messages, this.pwlen));
