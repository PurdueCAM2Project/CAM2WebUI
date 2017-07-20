# Email
## 1. User Email Confirmation

Email user to confirm registration and notify administrator after user registered.

### Approach

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
  
### Related Templates

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

## 2.Contact Us

### Goal
Under email_system app, creating a page for user to contact our website.

### Approach
Using a form that requires user to input "Name, email, subject and message" and the content into an email template. And then email admin. 
In `forms.py`:
```
class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
```
2 new urls needed to be linked: one for contact us, and one for notifying user the email has been sent.
In `urls.py`, add:
```
url(r'^contact/$', views.contact, name='contact'),
url(r'^email_sent/$', views.email_sent, name='email_sent'),
```
2 new views corresponding to the two urls are added.
The one that tells user email has been seet only needs a template:
```
def email_sent(request):
    return render(request, 'email_system/email_sent.html')
```
The second one is the view for contact us page:
First we get everything user input and add them into our email template. And then we email our website host.
```
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #get info from form
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            #add info to email template
            content = render_to_string('email_system/contact_email_template.html', {
                'name': name,
                'from_email': from_email,
                'message': message,
            })
            try:
                 send_mail(subject, content, from_email, [EMAIL_HOST_USER])#email admin
            except:
                messages.error(request, 'Email sent failed.')  # error message

            return redirect('email_sent')
    else:
        form = ContactForm()
    return render(request, "email_system/contact.html", {'form': form})
```

## Template
Email template:
`contact_email_template.html`
```
Contact Name:
{{ name }}

Email:
{{ from_email }}

Content:
{{ message }}
```

## 3. Administrator Emailing
### Goal
Allow admin to send email to specific users.
procedure:
Log in as admin, and in the main page, go to `Users`， click the checkbox to choose recipient and select `Email Users`, then click `Go` to go to a web page that admin can type in subject and message.

### decorator
To make sure only admin can use this view, we need to add a django decorator `@staff_member_required` before our function.

### Admin action
We will add a new action to User admin called `email user` to redirect the page to our `admin_send_email` page, and pass the email of selected user to the email input in `admin_send_email` page.
  
In `app/admin.py`
First we write the action. An admin action takes 3 parameters, self, request and queryset.
The queryset contains every user object we selected under User admin page. 
```
def email_users(self, request, queryset):
    list = queryset.values_list('email')
    email_selected = []
    for l in list:
        email_selected.append(l)
```
Since we want to automatically put the email of selected users to the input of admin_send_email page, we want to make it look pretty so that the email field in admin_send_email page can read the email.
 
Therefore we get the email and append them into a list, make it a string and remove the redundant brackets and empty value. 

```
email_selected = str(email_selected)
# remove empty email
email_selected = email_selected.replace('(\'\',),', '')
# remove redundant char
email_selected = email_selected.replace('[', '').replace(']', '').replace('(\'', '').replace('\',)', '')

```
At last we will use a `session` to pass the `email_selected`. And then, redirect admin to admin_send_email page
```
#open a session and render the email_selected to admin_send_email view
request.session['email_selected'] = email_selected
return redirect('admin_send_email')
```

After completing the action, We need to redefine a `UserAdmin` to add the action. In list_display, we choose the field we want to see in admin page.
And add the action to `actions` :
```
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'date_joined',
    )
    actions = [email_users]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
```
At last we need to unregister the User model because it is registered by default, and then reregister it with our`UserAdmin` class.

### Send Email Page
we use a form to obtain the subject, message and email:

In `forms.py':
```
    from django import forms
    from django.core.validators import validate_email
    
    class MailForm(forms.Form):
        email = MultiEmailField(required=False, help_text='Split email by " ,  " or " ; ", or copy paste a list from below')
        email_all_users = forms.BooleanField(required=False)
        subject = forms.CharField(max_length=255)
        message = forms.CharField(widget=forms.Textarea)
```

Since we want to send email to more than one address, we need to define a field that accepts multiple email addresses.
  
Before `Mailform`, add:
```
    class MultiEmailField(forms.Field):
        def to_python(self, value):
            if not value:
                return []
            #Modify the input so that email can be split by , and ;
            value = value.replace(' ', '') 
            value = value.replace(';', ',')
            while value.endswith(',') or value.endswith(';'):
                value = value[:-1] #remove the last ',' or ';'

            return value.split(',')

        def validate(self, value):
            """Check if value consists only of valid emails."""
            # Use the parent's handling of required fields, etc.
            super(MultiEmailField, self).validate(value)
            for email in value:
                validate_email(email)
```
The MultiEmailField will accept a list of email addresses that is split by `,` or `;` aas well as a list copy and paste from the user info table that we will create later.
  
Now go to `views.py`:

```
@staff_member_required
def admin_send_email(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            #email specific users
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            email_all_users = form.cleaned_data['email_all_users'] #option for email all users

            try:
                if email_all_users: #if ture, send email to all users
                    current_site = get_current_site(request)#will be used in templates
                    all_users = User.objects.all() #For iteration of email all users
                    mass_email = []
                    #iterations that add users info to each email and attach to mass_email list
                    for user in all_users: 
                        username = user.username
                        template = render_to_string('email_system/admin_send_email_template.html', {
                            'username': username,
                            'message': message,
                            'domain': current_site.domain,
                        })
                        mass_email.append((
                            subject,
                            template,
                            EMAIL_HOST_USER,
                            [user.email],
                        ))

                    send_mass_mail(mass_email)
                else: #if email_all_users is not true, send email to address that the admin typed in
                    send_mail(subject,message,EMAIL_HOST_USER,email)

                messages.success(request, 'Email successfully sent.')#success message
            except:
                messages.error(request, 'Email sent failed.')#error message

            return redirect('admin_send_email')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form': form})
 ```
 
There are two ways of sending email: send_mail and send_mass_mail. send_mass_mail will not close the channel of sending email after each email es sent, so it is slightly faster when sending a lot of email.

We also used a template here for email_all_users since it is nice to have signiture for an official email:

```
Hi {{ username }},
{{ message }}



Sincerely,
CAM2
http://{{ domain }}
```
For the convenience of administrator, it is good to have a table of all users' info.
To obtain them, we will use `objects.values` and `objects.values_list`. The `objects.values` will collect the names of each aspact of info, however, `objects.values_list` will only contain the info itself.
  
Right after `def admin_send_email(request):` and before `if request.method == 'POST':`, add the following to get user info:
  
    email_table = (User.objects.values('email')) #Obtaining a list of users' emails outside users info table for easy copying and pasting.
    users = User.objects.values_list('username', 'first_name', 'last_name', 'date_joined') #Obtaining a list of info required from user
    
and add this two list in `return render()` in the end:
    return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': users, 'email_table': email_table})


