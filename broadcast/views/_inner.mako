<%inherit file="/_base.mako"/>

<%block name="top">
    <nav id="main-nav" class="main-nav">
    <div class="logo">
        <a href="${url('main:home')}">Filecaster</a>
    </div>
    <a class="feedback-link" href="${url('feedback:submit')}" data-modal="feedback">
        <span class="icon icon-feedback"></span>
        <span class="label">${_('Feedback')}</span>
    </a>
    %if request.user.is_guest:
        <a class="login-link" href="${_(url('auth:login', next=request.fullpath))}">
            <span class="icon icon-key"></span>
            <span class="label">${_('Log in')}</span>
        </a>
    %else:
        <%
            USER_ICONS = {
                'moderator': 'user-shield',
                'superuser': 'user-star',
            }
            user_icon = USER_ICONS.get(request.user.group, 'user')
        %>
        <span class="user-profile">
            <span class="icon icon-${user_icon}"></span>
            <span class="label">${request.user.username}</span>
        </span>
        <a href="${url('auth:logout')}">
            <span class="icon icon-exit"></span>
            <span class="label">${_('Log out')}</span>
        </a>
    %endif
    </nav>
</%block>

<%block name="footer">
    <footer id="footer" class="footer">
    <nav id="smallprint">
    <a href="${url('main:terms')}">${_('Terms and Conditions, and Privacy Policy')}</a>
    <a href="https://outernet.is/content-guidelines" target="_blank">Outernet Content Guidelines</a>
    </nav>
    <p id="copyright">
        &copy;2016, Outernet Inc. All rights reserved.
    </p>
    </footer>
</%block>
