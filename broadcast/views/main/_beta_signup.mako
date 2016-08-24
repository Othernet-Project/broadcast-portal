<%namespace name="forms" file="/_forms.mako"/>

<h2>${_('Sign up for closed beta')}</h2>

<p>
    ${_('By submitting your email, you will be added to the closed beta '
    'mailing list. When there are new openings for the closed beta, you '
    'will receive an invitation. IndieGoGo backers and Outernet product '
    'owners will be invited first, so please be patient.')}
</p>

<form action="${url('main:beta_signup')}" method="POST">
    ${forms.csrf_token()}
    ${forms.field(form.email)}
    <button class="submit" type="submit">${_('Sign up')}</button>
</form>
