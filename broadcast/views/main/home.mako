<%inherit file="/_base.mako"/>

<%block name="page_title">${_('Filecaster by Outernet')}</%block>
<%block name="body_class">home</%block>

<%block name="top">
    <nav id="main-nav" class="main-nav">
        <a class="feedback-link" href="${url('feedback:submit')}">
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

<section id="hero" class="hero">
<h1 class="title">${_('Filecaster')}</h1>
<p class="subtitle">
    ${_('by Outernet')} 
    <a href="https://outernet.is/" rel="nofollow" target="_blank">
        <span class="text-label">${_('Outernet homepage')}</span>
        <span class="icon icon-arrow-right"></span>
    </a>
</p>

%if request.user.is_guest:
    <div id="register-form" class="register-form" data-roca-trap-submit="yes">
        <h2>${_('Join the filecaster community')}</h2>
        <p>${_('Join now to partitipate in shaping the future of the Outernet '
            'L-band service.')}</p>
        <p>
            <a href="${url('auth:register')}" data-roca-target="register-form">
                ${'Join'}
            </a>
        </p>
    </div>
%else:
    <div id="upload" class="upload" data-roca-trap-submit="yes">
        <h2>${_('Upload a file')}</h2>
        <p>
            <a href="${url('files:upload')}" data-roca-target="upload">
                ${'Add a new file to the review list'}
            </a>
        </p>
    </div>
%endif
</section>

<section id="stats" class="stats" data-roca-refresh-on="state-update">
<h2>${_('Daily filecast status')}</h2>
<p>
    <a href="${url('queue:status', widget=1)}" data-roca-target="stats">
        ${_('See the daily filecast status')}
    </a>
</p>
</section>
