<%inherit file="/_base.mako"/>

<%block name="page_title">${_('Filecast center by Outernet')}</%block>
<%block name="body_class">home</%block>

<%block name="top">
    <nav id="main-nav" class="main-nav">
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
<h1 class="title">${_('Filecast center')}</h1>
<p class="subtitle">
    ${_('by Outernet')} 
    <a href="https://outernet.is/" rel="nofollow" target="_blank">
        <span class="text-label">${_('Outernet homepage')}</span>
        <span class="icon icon-arrow-right"></span>
    </a>
</p>

<div id="beta-signup" class="beta-signup" data-roca-trap-submit="yes">
    <h2>${_('Join the closed beta')}</h2>
    <p>${_('Filecast center is now in closed beta. We are accepting '
        'sign-ups for closed beta testers.')}</p>
    <p>
        <a href="${url('main:beta_signup')}" data-roca-target="beta-signup">
            ${'Join'}
        </a>
    </p>
</div>
</section>

<section id="stats" class="stats" data-roca-refresh-on="state-update">
<h2>${_('Daily filecast status')}</h2>
<p>
    <a href="${url('queue:status', widget=1)}" data-roca-target="stats">
        ${_('See the daily filecast status')}
    </a>
</p>
</section>
