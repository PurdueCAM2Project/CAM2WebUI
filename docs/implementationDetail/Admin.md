# Admin
## 1. Send Email from Admin
### Goal
Allow admin to send email to specific users. procedure: Log in as admin, and in the main page, go to Users， click the checkbox to choose recipient and select Email Users, then click Go to go to a web page that admin can type in subject and message.

### Approach
See the documentation [here](https://purduecam2project.github.io/CAM2WebUI/implementationDetail/Email.html#send-email-from-admin).
  
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

