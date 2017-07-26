# App List

## Build up the new model
Add class `app_list` in `app/models.py`:
```
    class AppList(models.Model):
        applist = models.CharField(max_length=200, null=True)
        user = models.ForeignKey(User,on_delete=models.CASCADE,)
```
The apps is in the [many-to-one](https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_one/) relationship with the User. User in the `app_list` model keeps the foreign key of user from `django.contrib.auth.models`. Applist in the `app_list` model records the app name which the user puts in.

## Creating forms
We are going to use the form `ModelForm` provided by Django. ModelForms render Model fields as HTML. The form needs a model called `AppList`.
```
class AppForm(forms.ModelForm):
    applist = forms.CharField()

    class Meta:
        model = AppList
        fields = ('applist',)
```
We specify the [CharField](https://docs.djangoproject.com/en/1.11/ref/forms/fields/#charfield). Once we are done with defining the field, we need to add it into `Meta` so the forms know what we want to put in.

## Writing a view:
Now, we are going to create a view for our user applist adding. Go to `app/views.py` and add the following in the `profile` function definition:
```
    app_form = AppForm()

    apps = AppList.objects.filter(user=request.user).values()

    if request.method == 'POST' and 'add' in request.POST:
        app_form = AppForm(request.POST)
        if app_form.is_valid():
            applist = app_form.save(commit=False);
            applist.user = request.user
            applist.save()
        return redirect('profile')


    return render(request, 'app/profile.html', {
        'github_login': github_login,
        'form':form,
        'app_form':app_form,
        'apps':apps
     })
```
`commit=False` is to get the form from memoery, not in database. You can make changes before save it. After we assign the applist.user to current user, we call `applist.save()` and the data from form goes under the current user in database. After adding the apps, we will redirect the webpage to `profile`.

### Template:
We use the for loop to display the curret user's apps. 
```
    <h3 class="sub-header">App Lists</h3>

      {% if apps %}
      <ul class="apps">
          {% for app in apps %}
          <li>{{ app.applist }}</li>
          {% endfor %}
      </ul>
      {% endif %}

      <form method="post">
        {% csrf_token %}
        {% for field in app_form %}
           <p>
             {{ field.label_tag }}<br>
             {{ field }}
           </p>
        {% endfor %}
        <button class="btn" type="submit" name="add">Add</button>
      </form>
```
