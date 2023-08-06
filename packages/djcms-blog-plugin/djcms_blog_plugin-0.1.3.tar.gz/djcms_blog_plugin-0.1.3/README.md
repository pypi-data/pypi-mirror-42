# DjangoCMS Blog plugin


![image](https://img.shields.io/pypi/v/djangocms_blog_plugin.svg%0A%20%20%20%20%20:target:%20https://pypi.python.org/pypi/djangocms_blog_plugin)

![image](https://img.shields.io/travis/carlosmart626/djangocms_blog_plugin.svg%0A%20%20%20%20%20:target:%20https://travis-ci.org/carlosmart626/djangocms_blog_plugin)

![image](https://readthedocs.org/projects/djangocms-blog-plugin/badge/?version=latest%0A%20%20%20%20%20:target:%20https://djangocms-blog-plugin.readthedocs.io/en/latest/?badge=latest%0A%20%20%20%20%20:alt:%20Documentation%20Status)

![image](https://pyup.io/repos/github/carlosmart626/djangocms_blog_plugin/shield.svg%0A%20%20:target:%20https://pyup.io/repos/github/carlosmart626/djangocms_blog_plugin/%0A%20%20:alt:%20Updates)

DjangoCMS Blog plugin is a plugin enabled for DjangoCMS to add a feed of your posts created in [djcms_blog](https://github.com/CarlosMart626/djcms_blog) in any page.

-   Free software: MIT license
-   Documentation: <https://djangocms-blog-plugin.readthedocs.io>.


## Features
* Support DjangoCMS
* Can define a Blog to display
* Can define how many entries to display

## Installation

Install using pip
```
pip install djcms_blog_plugin
```

Add to installed apps:
```
INSTALLED_APPS = (`
    # Your django apps
    'cms', # required django cms
    
    'djcms_blog', # required djcms_blog
    'djcms_blog_plugin',
```

## Settings

```
DJCMS_BLOG_ID = 1 # Defines the Main blog id
DJCMS_BLOG_ENTRIES_NUMBER # Define the number of entries to display in the widget
```

## Contributing
Install dev dependencies
```
pip install -r requirements_dev.txt
```
Run tests
```
pytest . --cov=. --cov-report=term-missing

# virtualenv
python -m pytest . --cov=. --cov-report=term-missing
```
