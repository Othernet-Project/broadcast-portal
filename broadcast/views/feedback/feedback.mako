<%inherit file="/_inner.mako"/>
<%namespace name="feedback" file="_feedback.mako"/>

<h1>${_('Feedback')}</h1>

<section id="feedback" class="feedback">
${feedback.body()}
</section>

