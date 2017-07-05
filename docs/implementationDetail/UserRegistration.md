# User Registration

## Routing the URLS
Add the URL in `urlpatterns` in `app/urls.py`:
```
    urlpatterns = [ 
        url(r'^register/$', app_views.register, name='register'),
    ]
```
## Creating forms
Create a file `forms.py` in `app` and import `forms` from Django.
```
    from django import forms
```
We are going to use the form `UserCreationForm` provided by Django as our `form1`, the form contains basic information we must know about our users. The form also needs a model called "[User](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#user-model)":
```
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User
```
We could simply use `UserCreationForm` and we don't need to write the `forms.py` file. But it only comes with username and password and we do want to know more about our users. Therefore, we are going to extend the `UserCreationForm` by creating a form of our own:
```
    class RegistrationForm(UserCreationForm):
        first_name = forms.CharField(max_length=30)
        last_name = forms.CharField(max_length=30)
        email = forms.EmailField(max_length=254)

        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
```
Here we use the [User](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#user-model) model from Django, it comes with several fields containing what we defined above(name and email) but not required by default. Since we want to know the name and email of our users, in our `RegistrationForm`, we specify the 2 [CharField](https://docs.djangoproject.com/en/1.11/ref/forms/fields/#charfield) and an [EmailField](https://docs.djangoproject.com/en/1.11/ref/forms/fields/#emailfield) as required(explained in the tips below). Once we are done with defining those fields, we need to add them into `Meta` so the forms know which ones and in what order(from left to right) we want to put them in. (If we use a `{% for %}` loop to display them through Django template, the website will show them in order.)
***
Tips: 
  
In the form that we created, if we do not specify `required=False` such as

    email = forms.EmailField(max_length=254, required=False)
    
when we define a field, it will be a required information by default, and it will produce an error if users do not enter in an acceptable format(such as "12345" in `EmailField`).
  
If we want to put some [help text](https://docs.djangoproject.com/en/1.11/ref/forms/fields/#help-text) next to it, we can do
  
    email = forms.EmailField(max_length=254, help_text='Blah blah blah.')
  
and then add the following in the template:
  
    {% if field.help_text %}
      {{ field.help_text }}
    {% endif %}
  
***
Good! We are done with the required field, now we will use a different approach to recording optional information.
Go to app/models.py and create our own model, `RegisterUser' for optional information:
```  
    from django.contrib.auth.models import User
    from django.db.models.signals import post_save

    class RegisterUser(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        department = models.CharField(verbose_name='Department(Optional)', max_length=100, blank=True, null=True)
        organization = models.CharField(verbose_name='Organization(Optional)', max_length=100, blank=True, null=True)
        title = models.CharField(verbose_name='Title(Optional)', max_length=100, blank=True, null=True)
        country = models.CharField(verbose_name='Country(Optional)', max_length=50, blank=True, null=True)
        about= models.TextField(verbose_name='About(Optional)', max_length=500, blank=True, null=True)
```
You may notice that we have 2 more parameters here: [blank](https://docs.djangoproject.com/en/1.10/ref/models/fields/#blank) and [null](https://docs.djangoproject.com/en/1.10/ref/models/fields/#null). They tell the database to accept empty or blank value. If you want more information, please click on the link to read Django Documentation.
  
We also used a [OneToOneField](https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.OneToOneField) to relate the [User](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#user-model) object to this model. If we want to use any information in this `RegisterUser` model, for instance, the department, we will call: `.registeruser.department`(all lowercase).
  
Now we go back to `app/forms.py` to add our second form.
```
    from .models import RegisterUser
  
    class AdditionalForm(forms.ModelForm):
        class Meta:
            model = RegisterUser
            exclude = ('user')
```
Because we will use exactly the RegisterUser model we just created, so we don't need to define any other fields. However, we do want to exclude the 'user' object that relates the `RegisterUser` model to the user, but we don't want to create a new user object with the same information in the database. Recall that this model is to store optional information, and all the crucial information is in our first form `RegistrationForm`.


## Writing a register view:
Now, we are going to create a view for or user registration. Go to `app/views.py` and add the following:
```
    def register(request):
        if request.method == 'POST':
            form1 = RegistrationForm(request.POST)
            form2 = AdditionalForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                model1 = form1.save()
                model2 = form2.save(commit=False)
                model2.user = model1
                model2.save()
                return redirect('index')
        else:
            form1 = RegistrationForm()
            form2 = AdditionalForm()
        return render(request, 'app/register.html', {'form1': form1, 'form2': form2})
```
The reason we have `commit=False` in `model2 = form2.save(commit=False)` is that we do not want `form2` to create a new user, so when we create `form2`, it does not sync to the database, it allows us to make changes before we sync them. After we assign the `form1.user` to `form2.user`, we call `model2.save()` and the data of `form1` and `form2` goes under the same user in the database. After registration, we will redirect the user to our home page(`redirect('index')`).

### Template:
We just use 2 `{% for %}` loops to display the required information and optional information as 2 columns:
```
    {% for field in form1 %} <!-- or for field in form2 -->
      <p>
      {{ field.label_tag }}<br>
      {{ field }}
      {% for error in field.errors %}
        <p style="color: red">{{ error }}</p>
      {% endfor %}
      </p>
    {% endfor %}
```
***
Last Documentation: [User Login and Logout](https://github.com/PurdueCAM2Project/CAM2WebUI/wiki/User-Login-and-Logout)
***
[Useful tutorial from "SIMPLE IS BETTER THAN COMPLEX"](https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html)
