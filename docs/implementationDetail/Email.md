# Email
## 1. User Email Confirmation

Email user to confirm registration and notify administrator after user registered.

### Approach

Useful [tutorial](https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html)

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
  
### Related Templates
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

## 3. Send Email from Admin
See [here](https://purduecam2project.github.io/CAM2WebUI/implementationDetail/Admin.html#admin-action-of-send-email-from-admin)
for admin action of "send email from admin" that direct admin to this view.
### Goal
Receive a list of user id from previous page, and allow admin to input subject and message to send email to users in the list.
The admin can also add other recipient by adding email addresses into the "additional email" box.

### decorator
To make sure only admin can use this view, we need to add a django decorator `@staff_member_required` before our function.

### Send Email Page
we use a form to obtain the subject, message and additional email:
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
See [Django Documentation: Form field default cleaning](https://docs.djangoproject.com/en/1.11/ref/forms/validation/#form-field-default-cleaning)
  
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
  
Now go to `views.py`. We will use `request.session` to pass the user id list from another web page.
  
And we want to show the info of selected user at the bottom of the view for admin's convenience.
  
Therefore, we will first get the `User` object from user id, and form a list containing the information we need.
```
@staff_member_required
def admin_send_email(request):
    #obtain user id list from session, or none
    user_selected = request.session.get('user_id_selected', None)
    #get a list of User objects
    user_info=[]
    if user_selected is not None:
        for i in user_selected:
            obj=User.objects.get(id=i)
            obj_info=[obj.is_staff, obj.username, obj.email, obj.first_name, obj.last_name, obj.date_joined]
            user_info.append(obj_info)

```

To retrieve input from admin:
```
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            #get admin input
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
```
There are two ways of sending email: send_mail and send_mass_mail. send_mass_mail will not close the channel of sending email after each email es sent, so it is slightly faster when sending a lot of email. 
  
send_mass_mail accepts the email in the format: `(subject, message, from_email, recipient_list)`. See [Django Documentation: send_mass_mail()](https://docs.djangoproject.com/en/1.11/topics/email/#send-mass-mail).
    
It is better to send the email one by one, that is, we only put one email at a time in the `recipienct_list`, because all the email in `recipienct_list` is visible to others in the same `recipienct_list`.
  
To send the email one by one, we need to create a list to put all of our email, and then iterate through the user list to get their username and email. The username will be used for greeting in the email template. 
```
                    
            current_site = get_current_site(request)  # will be used in templates
            mass_email = []
            #for user id list
            for i in user_selected:
                obj = User.objects.get(id=i)
                if obj.email is not '':
                    username = obj.username  # will be used in template
                    template = render_to_string('email_system/admin_send_email_template.html', {
                        'username': username,
                        'message': message,
                        'domain': current_site.domain,
                    })
                    mass_email.append((
                        subject,
                        template,
                        EMAIL_HOST_USER,
                        [obj.email],
                    ))
            send_mass_mail(mass_email, fail_silently=False)
```
To email additional recipient is easy, just do another for loop iterating the email list: `for e in email:`.
  
Assign each email address as username for greeting in template. `username = e`
  
And change the recipient_list to `[e]`. All the other code can be reused directly.
  
At last, finish the function, the else matches the `if request.method == 'POST':`:
```
    else:
        form = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': user_info})
```

### Template
Email template:
```
Hi {{ username }},
{{ message }}



Sincerely,
CAM2
http://{{ domain }}
```

View template:
```
{% block content %}
<div class="top-content">
  <div class="inner-bg">
    <div class="container">
      <div class="row">
          <a style="color: blue" href="/admin/auth/user/">Go back to User administration</a>
        <h3>Email Users</h3>
      </div>
        {% if messages %}
        <ul style="color: red" class="messages">
            {% for message in messages %}
            <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
      <div class="form-bottom">
      <form method="post">
        {% csrf_token %}
        {% for field in form %}
            {% if field is form.email %}
                {{ field.label_tag }}<br>
                <input type="text" style="width: 100%" name="{{ form.email.name }}"/>
            {% else %}
                {{ field.label_tag }}<br>
                {{ field }}<br>
            {% endif %}
            {% if field.help_text %}
                <p style="color: grey">{{ field.help_text }}</p>
            {% endif %}
            {% for error in field.errors %}
                <p id="emailerror" style="color: red">{{ error }}</p>
            {% endfor %}

        {% endfor %}
        <button type="submit" name="sendemail" class="btn">Send</button>

        <br>
        <br>
        <div class="infoTable">
            <table style="width:100%; float: left">
            <h3>Selected Users</h3>
            <tr>
                <th>Staff Status</th>
                <th>Username</th>
                <th>Email</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Date Joined</th>
            </tr>

            {% for user in users %}
                <tr>
                {% for field in user %}
                    <td>{{ field }}</td>
                {% endfor %}
                </tr>
            {% endfor %}

            </table>

        </div>
      </form>
    </div>
  </div>
</div>
</div>
{% endblock %}
```
