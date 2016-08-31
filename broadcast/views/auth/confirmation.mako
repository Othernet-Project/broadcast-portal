<%inherit file="/_inner.mako"/>
<%namespace name="confirmation" file="_confirmation.mako"/>

<h1>${_('Confirmation')}</h1>

<section id="confirmation-form" class="confirmation-form">
    ${confirmation.body()}
</section>
