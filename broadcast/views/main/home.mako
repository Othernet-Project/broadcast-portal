<%inherit file="/_base.mako"/>

<%block name="page_title">${_('Filecast center by Outernet')}</%block>

<section id="hero" class="hero">
<h1>${_('Filecast center')}</h1>
<p>${_('by Outernet')} <a href="https://outernet.is/">Outernet homepage</a></p>

<div id="beta-signup" class="beta-signup">
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

<section id="stats" class="stats">
<h2>${_('Daily filecast status')}</h2>
<p>
    <a href="${url('queue:status')}" data-roca-target="stats">
        ${_('See the daily filecast status')}
    </a>
</p>
</section>
