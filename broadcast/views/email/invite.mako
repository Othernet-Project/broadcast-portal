<%namespace name="signature" file="_signature.mako"/>

Dear user,

This is an invitation to join the closed beta community at the Outernet's 
Filecast Center.

This invitation has been sent out because you (or someone else using your 
email) signed up for Filecast center closed beta program. To complete the 
signup process, please follow this link:

${host_url}${url('auth:accept_invitation', key=key)}

${signature.body()}