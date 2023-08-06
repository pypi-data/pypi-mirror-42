
# Simple Django Blog

Simple Django Blog app using Markdown

* Free software: MIT license
* Documentation: https://djcms-blog.readthedocs.io.


## Features

* Works on pure Django
* Markdown blog post format
* Built-in template
* Multiple languages support
* SEO tags supported to customize

## Usage

### Install
Add the following apps to your INSTALLED_APPS in `settings.py`
```
INSTALLED_APPS += [
    'django.contrib.sitemaps',
    'dj_markdown',
    'simplemde',
    'django.contrib.humanize',
    'djcms_blog',
]
```
Add `django.middleware.locale.LocaleMiddleware` to MIDDLEWARE
```
MIDDLEWARE += [
    'django.middleware.locale.LocaleMiddleware',
]
```
Define default language and supported languages.
```
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('es', 'ES'),
    ('en', 'EN'),
]
```
Update your `urls.py` adding blog urls.
```
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from djcms_blog.sitemaps import PostsSitemap

sitemaps = {
    'blog': PostsSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

urlpatterns += i18n_patterns(
    url(r'^', include('djcms_blog.urls')),
)
```

## Configuration
You can define the following blog settings in your settings.

**DEFAULT_BLOG_ID** Define the default blog id to be used in the urls and links.

**DEFAULT_URL** URL to open the blog

**BLOG_TITLE** HTML title

**ROOT_TITLE** Title for links

**DJCMS_BLOG_CACHE_TIME** Cache time used in public views.

**MARKDOWN_CODE_CSS_THEME** Code theme for markdown code in the blog.

**DEFAULT_COVER_IMAGE** Cover image used in blog

**DEFAULT_NAVBAR_IMAGE** Image used as icon in navigation

### Example
In `settings.py`
```
# Blog config
DJCMS_BLOG_CACHE_TIME = 0
DEFAULT_BLOG_ID = 1
```

## Contributing
Install dev dependencies
```
pip install -r requirements_dev.txt
```
Run tests
```
pytest . --cov=. --cov-report=term-missing
```
Static Analysis
```
flake8 .
```

## Credits

This package was created with **Cookiecutter** and the `audreyr/cookiecutter-pypackage` project template.
