# User Third party login

This page will walk you through some guides on writing third party login including google login and github login on the login page.

## Installation

For the django third party login, there is a django app called social-auth-app-django already built for us. So we can simply download this library to make third party login easier to build. We can use python pip to install the app.

```
pip install social-auth-app-django
```

Then visit settings.py in our app and include that in the installed apps:

```

INSTALLED_APPS = [
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'social_django', # <---- Add this one
]

```

After you save the settings.py. Go to terminal and migrate the database.

```
python manage.py migrate
```

## Configuration

Back to the settings.py, we have several more things to modify.

The first one is Middleware, we need to add one more thing:

```

MIDDLEWARE = [
    'app.middleware.basicauth.BasicAuthMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',    # <--- Add this one
]

```

Then we need to update the template in setting.py:

```

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',                # <--- Add this one
                'social_django.context_processors.login_redirect',          # <--- Add this one
            ],
        },
    },
]

```

Next we will add authentication backend in settings, since we need google and github login, we add github oauth and google oauth. If you would like to add something like facebook login, you can add 'social_core.backends.facebook.FacebookOAuth2' in this model backend if you want.

```

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

```


Let’s set the default values for the LOGIN_URL, LOGOUT_URL and the LOGIN_REDIRECT_URL. The LOGIN_REDIRECT_URL will be used to redirect the user after authenticating from Django Login and Social Auth.

```
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

SOCIAL_AUTH_LOGIN_ERROR_URL = '/register/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/oauthinfo/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
```

Update the urls.py add the social-auth-app-django urls:



```
url(r'^oauth/', include('social_django.urls', namespace='social')),
```

## GitHub Authentication


Log in to your GitHub account, go to Settings. In the left menu you will see Developer settings. Click on OAuth applications.

In the OAuth applications screen click on Register a new application. 

Fill in the form with any name, url or description. The only important one is Authorization callback URL:

Notice that I’m putting a localhost URL. **http://localhost:8000/oauth/complete/github/. You must use this url to accomplish oauth login for github.**


After you create the app, you can get:

* client id

* client secret

Copy and paste those items and send them into the environment. Don't make it public!!

Then in settings.py, add two varialbes called 'SOCIAL_AUTH_GITHUB_KEY' and 'SOCIAL_AUTH_GITHUB_SECRET'

```
SOCIAL_AUTH_GITHUB_KEY = os.environ['GITHUB_KEY']
SOCIAL_AUTH_GITHUB_SECRET = os.environ['GITHUB_SECRET']
```

Settings for github login is finished!


## Google Authentication

For google authentication, it is similar to github authentication. This time we need to acquire google credentials.

Visit [https://console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials)

Click on 'create credentials' -> 'oauth client id' -> 'web application' -> Fill in the form

The same as before, the only important one is Authorized redirect URIs:

Notice that I’m putting a localhost URL. **http://localhost:8000/oauth/complete/google-oauth2/. You must use this url to accomplish oauth login for google.**

After you create the app, you can get:

* client id

* client secret

Copy and paste those items and send them into the environment. Don't make it public!!

Then in settings.py, add two varialbes called 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY' and 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'

```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['GOOGLE_LOGIN_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['GOOGLE_LOGIN_SECRET']
```

Google oauth has one more step than github login. If you just finish this step, you will still get an error. You need to enable Google+ API

On the same page left side, choose 'library', in Social APIs column choose Google+ API: click on enable to enable google+ API.


## Add url in page

```

<div class="social-login">
<h4 style="color:black;text-align:center;">- or -</h4>
<div class="social-login-buttons">
  <a class="btn btn-block btn-social btn-lg btn-github" id="github_login" href="xxx">
    <span class="fa fa-github"></span>Sign in with Github
  </a>
  <a class="btn btn-block btn-social btn-lg btn-google" href="xxx">
    <span class="fa fa-google"></span> Login with Google
  </a>
</div>

</div>

```

Now you can try to login with github and google!

