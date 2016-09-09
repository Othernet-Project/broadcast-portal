<p>${_('''Yes, that's right. Congratulations! You have been chosen as a
moderator. As a moderator you have the ability to oversee user uploads, and
vote on them to decide whether they should be filecast on the Outernet's L-band
service. Together with other moderators, you now have the ability to influence
and decide on the future of the Outernet's L-band service.
''')}</p>

<p>${_('''We have defined a 
<a href="https://outernet.is/content-guidelines" target="_blank">general 
guidelines</a> that will help you make your decision, but for anything outside
of those guidelines, you are calling the shots.
''') | n,unicode}</p>

<p>${_("Welcome to the Filecaster. Let's make the future together!")}</p>

<p>
    <a class="button" href="${url('queue:status')}">${_('Get started')}</a>
</p>
