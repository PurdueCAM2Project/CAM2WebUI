Django version 1.10.5
***
We are using login and logout views written by Django, imported from django.contrib.auth.view.Login, this view does basic authentication such as verify username and password when users logging in.
  
To better distinguish the imported views and views written by ourselves, we imported `auth.view` (views from Django) as “auth_view” and `app.view` (Our views) as “app_view”.
  
    from . import views as app_views
    from django.contrib.auth import views as auth_views
  
### Routing the URLS:
Since all of the links related to login and register is in app “app”, so we will put our URLs in app.urls(If there isn't such a file, create one) and include them in our project URLs (inside the folder that has settings.py).
  
>cam2webui/urls.py
  
    from django.conf.urls import url,include

    urlpatterns = [ 
        url(r'^', include('app.urls')),
    ]
>app/urls.py:
  
    from . import views as app_views
    from django.contrib.auth import views as auth_views

    urlpatterns = [
        url(r'^login/$', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout),
    ]
  
If we don’t specify the template for this login view, Django will look for template from `registration/login.html`. But we want to keep our template together inside `app` folder, so we specify the template in the url:
  
    url(r'^login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),
  
Besides, after users logged out, we want them to go back to home page, so we use `next_page` parameter to redirect:
  
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
  
The Django login view implements a redirect function, all we need to do is to go to `settings.py` and add:
  
    LOGIN_REDIRECT_URL = 'index'
  
(We use the names we defined for our URLs. For here, `index` is the home page.)
  
### Login template:
The website design will not be covered in this documentation. Apart from that, we simply use for loops to display all the field necessary for login and any error corresponding to each field:
  
    {% block content %}
        <form role="form" action="" method="post" class="login-form">
            {% csrf_token %}
            {% for field in form %}
              <p>
              {{ field.label_tag }}<br>
              {{ field }}
              </p>
            {% endfor %}
            <button type="submit" class="btn">Sign in</button>
            {% if form.non_field_errors %}
              <ul class='form-errors'>
                {% for error in form.non_field_errors %}
                    <li>{{ error }}</li>
                {% endfor %}
              </ul>
            {% endif %}
        </form>
    {% endblock %}

Instead of creating a successful login page after user logged in, it is easier for users to know whether they have logged in by showing the status on the top right corner of the website. Therefore, we will use an `{% if %}{% else %}` statement in our `base.html`, which all other template extends, so the user can see the status on all pages of our website.
  
    {% if user.is_authenticated %}
      <li><a href="/profile/">{{request.user.username}}'s Profile </a></li>
      <li><a href="/logout/">Logout</a></li>
    {% else %}
      <li><a href="/login/">Login</a></li>
      <li><a href="/register/">Register</a></li>
    {% endif %}
`User.is.authenticated` returns `True` if a user has logged in, then the website will display the name of the user with the links to their profile and logout. If it returns `False`, then the website will show the links to login and register.
***
Next Documentation: [User Registration](https://github.com/PurdueCAM2Project/CAM2WebUI/wiki/User-Registration)
***
[Useful tutorial from "SIMPLE IS BETTER THAN COMPLEX"](https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html)
