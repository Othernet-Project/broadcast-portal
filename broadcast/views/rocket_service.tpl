<%inherit file='base.tpl'/>

<%block name="title">
    ${_("Rocket Service")}
</%block>

<%block name="main">
    <div class="static">
        <h2>${_('Rocket Share')}</h2>
        <div class="info">
            <p>${_("Sharing files over Outernet is free. However, we have a limited amount of satellite capacity, so we can't guarantee when all of the files uploaded to our servers will be broadcast.")}</p> 
            <p>${_("Rocket Share ensures that your files receive prioritized review and guaranteed delivery in a timely manner. We can also schedule your files for broadcasting through this premium service. Contact us to learn more about Rocket Share.")}</p> 
            <a href="mailto:hello@outernet.is">hello@outernet.is</a>
        </div>
    </div>
</%block>

