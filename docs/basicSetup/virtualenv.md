# [Guide] virtualenv
Joseph Sweeney edited this page on Mar 22

___

To simplify Python dependencies, use `virtualenv`. This tool can be install with `pip`:

```
pip install virtualenv
```

A virtual environment named `venv` already exists in the root project directory. To activate it:

```
source venv/bin/activate
```

Your `bash` prompt will now begin with `(venv)`. To deactivate virtualenv:

```
deactivate
```