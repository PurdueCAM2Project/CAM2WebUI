Django version 1.11.1
***
## Goal
Allow admin to send email to specific users.
procedure:
Log in as admin, and in the main page, go to `Users`， click the checkbox to choose recipient and select `Email Users`, then click `Go` to go to a web page that admin can type in subject and message.

## Approach
Create a new app calld `email_system`
  
Create a view for the email page. To make sure only admin can use this, we need to add a django decorator `@staff_member_required` before aour function.

### Admin action
We will add a new action to User admin called `email user` to redirect the page to our `admin_send_email` page, and pass the email of selected user to the email input in `admin_send_email` page.
  
In `app/admin.py`
First we write the action. An admin action takes 3 parameters, self, request and queryset.
The queryset contains every user object we selected under User admin page. ```
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
```
In `forms.py':
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
            #For copying and pasting email address from the list, None, () \ will be removed.
            value = value.replace(' ', '') 
            value = value.replace('None,', '') 
            value = value.replace(';', ',')
            value = value.replace('(', '')
            value = value.replace(')', '')
            value = value.replace('\'', '')
            print(value)
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
 
There are two ways of sending email: send_mail and send_mass_mail. send_mass_mail will not close the channel of sending email after each email es sent, so it is slightly faster when sending email to a lot of people.
  
And the outcome is different. If we send_mass_email by attach every email to a list and send them together, the "to" part of the email will only show one email address, but if we use send_mail with a email list, the "to" part will show all the receivers.
  
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
  
Right after `def admin_send_email(request):` and before `if request.method == 'POST':`, add:
    email_table = (User.objects.values('email')) #Obtaining a list of users' emails outside users info table for easy copying and pasting.
    users = User.objects.values_list('username', 'first_name', 'last_name', 'date_joined') #Obtaining a list of info required from user
    
and add this two list in `return render()` in the end:
     return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': users, 'email_table': email_table})
