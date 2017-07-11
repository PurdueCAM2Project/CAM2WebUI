# Forgot Password (Password Reset)

## Goal
Allow users to reset their password through email.
  
The user will go to the password reset page and enter their email. When the email is inside our database, we send a confirmation
with a link to reset the password.

## approach
Django has its own password reset views. We just need to create template and link the urls.
  
add the following to `urls.py`:
  
```
url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
url(r'^password_reset_email_sent/$', auth_views.password_reset_done, name='password_reset_done'),
url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.password_reset_confirm, name='password_reset_confirm'),
url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
```

Create a new directory `registration` under templates and put our templates inside.
  
`password_reset_form.html` correspond to `password_reset`: ask user to enter their email address
  
`password_reset_done.html` correspond to `password_reset_email_sent`: tells user the confirmation email has been sent
  
`password_reset_subject.txt`: Subject of confirmation email
  
`password_reset_email.html`: Content of confirmation email
  
`password_reset_confirm.html`: ask user to set new password
  
`password_reset_complete.html`: tells user the password has been reset
  
