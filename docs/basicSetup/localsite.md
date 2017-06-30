# Viewing the Website Locally

There are three steps to viewing the website locally.

## Virtualenv Setup (if you only have python 3.6 in your machine, you can skip this step)

To simplify Python dependencies, use `virtualenv`. This tool can be install with `pip`:
```bash
pip install virtualenv
```

A virtual environment named `venv` already exists in the root project directory. To activate it:
```bash
source venv/bin/activate
```

Your `bash` prompt will now begin with `(venv)`. To deactivate virtualenv:

```bash
deactivate
```

## Configuring Python virtual environment

[Create a Python virtual environment]([Guide]-virtualenv) and activate it. Then install requirements with

```bash
pip install -r requirements.txt
```

If you are using Ubuntu, you may get compilation errors related to psycopg2. In this case, install the needed libraries with:

```bash
sudo apt-get install libpq-dev python3-dev
```

## Exporting config vars

Django expects several environment variables on startup. For each required environment variable, execute

```bash
export <VAR_NAME>=<value>
```

The required environment variables are:

| Name                 | Value |
|:---------------------|:------|
| `DJANGO_SECRET_KEY`  | Give this variable a dummy value. |
| `GITHUB_KEY`         | [Retrieve this value from GitHub](https://github.com/settings/applications/new) |
| `GITHUB_SECRET`      | [Retrieve this value from GitHub](https://github.com/settings/applications/new) |
| `BASICAUTH_USERNAME` | Give this variable a dummy value. (you will need to enter it when accessing the local site) |
| `BASICAUTH_PASSWORD` | Give this variable a dummy value. (you will need to enter it when accessing the local site) |

It might be helpful to add these to a file that you can run whenever you need to export them to your environment. Just remember not to commit it!

If you want to disable basic authentication for the local site, remove `BasicAuthMiddleware` from `cam2webui/settings.py`.

## Run the local server

```bash
python manage.py runserver
```

Then open [lvh.me:8000](http://lvh.me:8000) in your browser.
