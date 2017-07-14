# User Email Confirmation

Email user to confirm registration and notify administrator after user registered.

## Approach

Followed this [tutorial](https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html)

After the code of register, add the following to email user and admin:
Under `model1 = form1.save(commit=False)`, add
  
    model1.is_active = False #Will be set True after users confirm their email.
      
so that the account will be inactive until users confirm their email.

And the body of email user and admin is the following:
  
We will use a template to email users, and the template will have username, a link to confirm adn activate user's account, and some content.

```
#Email user
current_site = get_current_site(request) #will be used in website signiture
subject = 'Activate Your CAM2 Account'
message = render_to_string('app/confirmation_email.html', {
    'user': model1,
    'domain': current_site.domain,
    'uid': urlsafe_base64_encode(force_bytes(model1.pk)),
    'token': account_activation_token.make_token(model1),
})
model1.email_user(subject, message)
```

We will use a Django function mail_admins to notify admin when a user is registered.

```
#Email admin
admin_subject = 'New User Registered'
admin_message = render_to_string('app/new_user_email_to_admin.html', {
    'user': model1,
    'optional': model2,
})
mail_admins(admin_subject, admin_message)
```

And redirect the page to a page that tells user the confirmation email has been sent:

```
return redirect('email_confirmation_sent')
``` 
    
The `token` in email template will be randomly generated based on user's information.
Create a new file called `tokens.py` and add the following:

```
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.registeruser.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()
```
    
In addition, we need links for confirmation and successful activation:
go to `urls.py` and add:

```
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    app_views.activate, name='activate'),
url(r'^account_activated/$', app_views.account_activated, name='account_activated'),
```

Now we will work on the activation function. In `views.py`:

```
def activate(request, uidb64, token):
    try: #Get user
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    #Activate user
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.registeruser.email_confirmed = True
        user.save()

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        return redirect('account_activated')
    else:
        return render(request, 'email_confirmation_invalid.html')
```
            
We will get the user based on the link and activate user if the user exist. The link will be invalid a short time after the user is activated.
  
## Related Templates

The web page that user is redirected to after they register:

email_confirmation_sent.html:
```
{% block content %}
    <h4 id="emailconfirm">Email confirmation sent</h4>
    <p>We have sent an account confirmation to your email. <br>
    Please confirm your email address to complete the registration. </p>
    <p style="color: red">If you don't confirm your email, you will not be able to sign in!</p>
    <p><a style="color: deepskyblue" href="/">Go back to home page</a></p>
{% endblock %}
```
    
Template for the confirmation email sent to user:

```
{% autoescape off %}
Hi {{ user.username }},

    Welcome to CAM2!
    Please click on the link below to confirm your registration:
    http://{{ domain }}{% url 'activate' uidb64=uid token=token %}

    If you did not sign up for CAM2 website, it might be somebody else that mistakenly use your email for registration.
    We are very sorry for the inconvenience!

Sincerely,
CAM2
http://{{ domain }}
{% endautoescape %}
```
The variables inside `{{ }}` must match what we defined in `render_to_string` in `views.py`.

The web page when user open the link in confirmation email:
```
{% block content %}
    <h4>Account Successfully Activated</h4>
    <p>Congratulations! your account has been successfully activated!</p>
    <p>The website will automatically go back to home page in 5 seconds.</p>
    <p><a style="color: deepskyblue" href="/">Click here if there's no response</a></p>
    <script>
        function redirect(){
            window.location.href = "/";
        }
        setTimeout(redirect, 5000);
    </script>
{% endblock %}
```
    
The function in script makes sure that the website will be redirected to the home page after 5 seconds.

