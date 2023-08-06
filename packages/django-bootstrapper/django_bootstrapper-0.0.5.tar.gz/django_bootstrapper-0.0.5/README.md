# Django Bootstrapper

[![PyPI](https://img.shields.io/pypi/v/django-bootstrapper.svg)](https://pypi.org/project/django-bootstrapper)
[![Build Status](https://travis-ci.org/contraslash/django-bootstrapper.svg?branch=master)](https://travis-ci.org/contraslash/django-bootstrapper)

This is a simple django project generator, it uses django default command and complete the schema generating a full application ready to use, including base, authentication, and template_base applications.

The main idea behind this projects is to automate some labors when we create projects.

# Usage
First create a new environment

```bash
# For pip users
python -m venv my_custom_environment
# For conda users
conda create --name my_custom_environment
```

Now install django-bootstrapper

```bash
pip install django-bootstrapper
```

Now just execute `django-bootstrapper.py` and follow the rules

The project folder structure will be:

```bash
project_folder
├── applications
│   ├── authentication (Authentication app from https://github.com/contraslash/authentication-django)
│   ├── base_template (Base template from https://github.com/contraslash/template_cdn_bootstrap)
│   └── __init__.py
├── base (base from https://github.com/contraslash/base-django)
├── manage.py
└── project_name
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```

The project is git submodule based, and creates submodules for `authentication`, `base_template` and `base`, 
all open source projects  created by contraslash.

Also we recommend to use [Django Crud Generator](https://django-crud-generator.readthedocs.io/en/latest/) to create CRUD
automatically.

Our main goal is to create a project with a structure that we can extend using templates and existing files.
 
If you want to modify and add to your tree any submodule, we recommend to follow [this question](https://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule) 


## Test your changes
We want to include test on this suite so, to test your changes use

```bash
pytest
```


## Compile locally
```bash
python setup.py sdist
python setup.py install
```