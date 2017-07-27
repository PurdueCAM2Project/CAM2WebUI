# Admin
## 1. Admin action of Send Email from Admin
### Goal
Allow admin to send email to specific users. 
procedure: 1.Log in as admin, and in the main page, go to Users. 
  
           2.Using checkbox to choose recipient
             
           3.Select "Email Users" in action
             
           4.Click Go to go to a web page that admin      input in subject and message.

### Approach
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
At last we will use a `session` to pass the `email_selected`. And then, redirect admin to `admin_send_email page`
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

## 2. Export User Data to CSV
### Goal
To create an admin action that download a CSV file containing info of selected user(s).
  
### UserAdmin class and Admin action
[Django Documentation on "Outputting CSV with Django"](https://docs.djangoproject.com/en/1.11/howto/outputting-csv/) 
  
To see how to add actions to Model and how to modify`UserAdmin`,
see [here](https://purduecam2project.github.io/CAM2WebUI/implementationDetail/Email.html#admin-action).
  
### Action Function
Go to `app/admin.py`, find `actions` in class `UserAdmin`, add the new function `export_csv`.
  
And create the function **before** class `UserAdmin`:
```
def export_csv(modeladmin, request, queryset):
    #setup csv writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=CAM2UserList.csv'
    writer = csv.writer(response)
```
The CSV-creation acts on file-like objects such as the HttpResponse in Django.
  
See [Django documentation](https://docs.djangoproject.com/en/1.11/howto/outputting-csv/).
```
    opts = queryset.model._meta  #obtaining User model as meta data because models are not iterable
    required_field_names = [field.name for field in opts.fields] #get names of all fields in User model as a list
    optional_field_names = [field.name for field in RegisterUser._meta.fields] ##get names of all fields in User model as a list
```
We need to seperate them because they will be used for every iteration of selected users. And create another combined list for the final CSV form.
```
    field_names = required_field_names.copy()
    for field in optional_field_names:
        field_names.append(field)
    writer.writerow(field_names)
```
To obtain info of each user, an for loop is used, and the required info and optional info will be gained through each iteration.
  
The field in `required_field_names` and `optional_field_names` decide which info from `User` and `RegisterUser` model we will get.
  
More info on `RegisterUser`, see [here](https://purduecam2project.github.io/CAM2WebUI/implementationDetail/User.html#creating-a-model).
  
```
    for obj in queryset:
        required_info = [getattr(obj, field) for field in required_field_names]
        try:
            optional = RegisterUser.objects.get(user=obj)  # get optional info of user
            optional_info = [getattr(optional, field) for field in optional_field_names]
        except:
            optional_info = ['N/A' for field in optional_field_names]
        for data in optional_info:
            required_info.append(data)
        writer.writerow(required_info)
    return response
```
At last, give this action a name outside function(no indentation):
```
export_csv.short_description = "Export selected user as csv"
```

