# AA Bulletin Board

[![Version](https://img.shields.io/pypi/v/aa-bulletin-board?label=release)](https://pypi.org/project/aa-bulletin-board/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-bulletin-board)](https://github.com/ppfeufer/aa-bulletin-board/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-bulletin-board)](https://pypi.org/project/aa-bulletin-board/)
[![Django](https://img.shields.io/pypi/djversions/aa-bulletin-board?label=django)](https://pypi.org/project/aa-bulletin-board/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)
[![Automated Checks](https://github.com/ppfeufer/aa-bulletin-board/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-bulletin-board/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-bulletin-board/branch/master/graph/badge.svg?token=UCXABR42QC)](https://codecov.io/gh/ppfeufer/aa-bulletin-board)
[![Translation Status](https://weblate.ppfeufer.de/widgets/alliance-auth-apps/-/aa-bulletin-board/svg-badge.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-forum/blob/master/CODE_OF_CONDUCT.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

Simple bulletin board for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth)


---

<!-- TOC -->
* [AA Bulletin Board](#aa-bulletin-board)
  * [⚠️ Before You Install This Module ⚠️](#-before-you-install-this-module-)
  * [Installation](#installation)
    * [Step 1: Install the Package](#step-1-install-the-package)
    * [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
      * [Settings in `/home/allianceserver/myauth/myauth/settings/local.py`](#settings-in-homeallianceservermyauthmyauthsettingslocalpy)
      * [Settings in `/home/allianceserver/myauth/myauth/urls.py`](#settings-in-homeallianceservermyauthmyauthurlspy)
    * [Step 3: Configure Your Webserver](#step-3-configure-your-webserver)
      * [Apache](#apache)
      * [Nginx](#nginx)
    * [Step 4: Finalizing the Installation](#step-4-finalizing-the-installation)
    * [Step 5: Set Up Permissions](#step-5-set-up-permissions)
  * [Permissions](#permissions)
  * [Changelog](#changelog)
  * [Contributing](#contributing)
<!-- TOC -->

---


## ⚠️ Before You Install This Module ⚠️

This module needs quite some configuration done before working properly. You need to
modify your Apache/Nginx configuration as well as the global URL config of Alliance
Auth. So please only install if you know what you're doing/feel comfortable to make
these kinds of changes. For your own sanity, and mine :-)


## Installation

**Important**: Please make sure you meet all preconditions before you proceed:

- AA Bulletin Board is a plugin for Alliance Auth. If you don't have Alliance Auth
  running already, please install it first before proceeding. (see the official
  [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html)
  or details)
- Aa Bulletin Board needs a couple of changes made to your Webserver and Alliance
  Auth configuration. So make sure you know how to do so. The steps needed will be
  described in this document, but you need to understand what will be changed.


### Step 1: Install the Package

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-bulletin-board
```

### Step 2: Configure Alliance Auth

#### Settings in `/home/allianceserver/myauth/myauth/settings/local.py`

This is fairly simple, configure your AA settings (`local.py`) as follows:

```python
# AA Bulletin Board
INSTALLED_APPS += [
    "ckeditor",
    "ckeditor_uploader",
    "django_ckeditor_youtube_plugin",
    "aa_bulletin_board",  # https://github.com/ppfeufer/aa-bulletin-board
]

if "ckeditor" in INSTALLED_APPS:
    # ckEditor
    import ckeditor.configs

    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/var/www/myauth/media/"

    X_FRAME_OPTIONS = "SAMEORIGIN"

    CKEDITOR_UPLOAD_PATH = "uploads/"
    CKEDITOR_RESTRICT_BY_USER = True
    CKEDITOR_ALLOW_NONIMAGE_FILES = False

    # Editor configuration
    #
    # If you already have this from another app, like `aa-forum`, you don't need to
    # define this again, just add it to the `CKEDITOR_CONFIGS` dict, see below
    #
    # You can extend and change this to your needs
    # Some of the options are commented out, feel free to play around with them
    ckeditor_default_config = {
        "width": "100%",
        "height": "45vh",
        "youtube_responsive": True,
        "youtube_privacy": True,
        "youtube_related": False,
        "youtube_width": 1920,
        "youtube_height": 1080,
        "extraPlugins": ",".join(
            [
                "uploadimage",
                # "div",
                "autolink",
                # "autoembed",
                # "embedsemantic",
                "clipboard",
                "elementspath",
                # "codesnippet",
                "youtube",
            ]
        ),
        "toolbar": [
            {
                "name": "styles",
                "items": [
                    "Styles",
                    "Format",
                    # "Font",
                    # "FontSize",
                ],
            },
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    # "Subscript",
                    # "Superscript",
                    # "-",
                    # "RemoveFormat",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    # "Cut",
                    # "Copy",
                    # "Paste",
                    # "PasteText",
                    # "PasteFromWord",
                    # "-",
                    "Undo",
                    "Redo",
                ],
            },
            {
                "name": "links",
                "items": [
                    "Link",
                    "Unlink",
                    "Anchor",
                ],
            },
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Youtube",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    # "PageBreak",
                    # "Iframe",
                ],
            },
            {
                "name": "colors",
                "items": [
                    "TextColor",
                    "BGColor",
                ],
            },
            {
                "name": "document",
                "items": [
                    # "Source",
                    # "-",
                    # "Save",
                    # "NewPage",
                    # "Preview",
                    # "Print",
                    # "-",
                    # "Templates",
                ],
            },
        ],
    }

    # Add the external YouTube plugin
    aa_bulletin_board__external_plugin_resources = [
        (
            "youtube",
            "/static/ckeditor/ckeditor/plugins/youtube/",
            "plugin.min.js",
        )
    ]

    # Put it all together
    CKEDITOR_CONFIGS = {
        "default": ckeditor.configs.DEFAULT_CONFIG,
        "aa_bulletin_board": ckeditor_default_config,
    }

    CKEDITOR_CONFIGS["aa_bulletin_board"][
        "external_plugin_resources"
    ] = aa_bulletin_board__external_plugin_resources
```

#### Settings in `/home/allianceserver/myauth/myauth/urls.py`

Now let's move on to editing the global URL configuration of Alliance Auth. To do so,
you need to open `/home/allianceserver/myauth/myauth/urls.py` and change the
following block right before the `handler` definitions:

```python
# URL configuration for cKeditor
from django.apps import apps

if apps.is_installed("ckeditor"):
    # Django
    from django.contrib.auth.decorators import login_required
    from django.views.decorators.cache import never_cache

    # ckEditor
    from ckeditor_uploader import views as ckeditor_views

    urlpatterns = [
        re_path(
            r"^upload/", login_required(ckeditor_views.upload), name="ckeditor_upload"
        ),
        re_path(
            r"^browse/",
            never_cache(login_required(ckeditor_views.browse)),
            name="ckeditor_browse",
        ),
    ] + urlpatterns
```

After this, your `urls.py` should look similar to this:

```python
from django.urls import include, re_path

from allianceauth import urls

# Alliance auth urls
urlpatterns = [
    re_path(r"", include(urls)),
]

# URL configuration for cKeditor
from django.apps import apps

if apps.is_installed("ckeditor"):
    # Django
    from django.contrib.auth.decorators import login_required
    from django.views.decorators.cache import never_cache

    # ckEditor
    from ckeditor_uploader import views as ckeditor_views

    urlpatterns = [
        re_path(
            r"^upload/", login_required(ckeditor_views.upload), name="ckeditor_upload"
        ),
        re_path(
            r"^browse/",
            never_cache(login_required(ckeditor_views.browse)),
            name="ckeditor_browse",
        ),
    ] + urlpatterns

handler500 = "allianceauth.views.Generic500Redirect"
handler404 = "allianceauth.views.Generic404Redirect"
handler403 = "allianceauth.views.Generic403Redirect"
handler400 = "allianceauth.views.Generic400Redirect"
```


### Step 3: Configure Your Webserver

Your webserver needs to know from where to serve the uploaded images, of course, so we
have to tell it.

#### Apache

In your vhost configuration you have a line `ProxyPassMatch ^/static !`, which tells
the server where to find all the static files. We're adding a similar line for the
media, right below that one.

Add the following right below the static proxy match:
```apache
ProxyPassMatch ^/media !
```

Now we also need to let the server know where to find the media directory we just
configured the proxy for. To do so, add a new Alias to your configuration. This can
be done right below the already existing Alias for `/static`:
```apache
Alias "/media" "/var/www/myauth/media/"
```

At last, a Directory rule is needed as well. Add the following code below to the
already existing Directory rule for the static files:

```apache
<Directory "/var/www/myauth/media/">
    Require all granted
</Directory>
```

So the whole block should now look like this:
```apache
ProxyPassMatch ^/static !
ProxyPassMatch ^/media !  # *** NEW proxy rule
ProxyPass / http://127.0.0.1:8000/
ProxyPassReverse / http://127.0.0.1:8000/
ProxyPreserveHost On

Alias "/static" "/var/www/myauth/static/"
Alias "/media" "/var/www/myauth/media/"

<Directory "/var/www/myauth/static/">
    Require all granted
</Directory>

<Directory "/var/www/myauth/media/">
    Require all granted
</Directory>
```

Restart your Apache webserver.


#### Nginx

In order to let Nginx know where to find the uploaded files, you need to add a new
location rule to the configuration.
```nginx
location /media {
    alias /var/www/myauth/media;
    autoindex off;
}
```

Restart your Nginx webserver.


### Step 4: Finalizing the Installation

Run static files collection and migrations

```shell
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for Auth


### Step 5: Set Up Permissions

Now it's time to set up access permissions for your new module. You can do so in
your admin backend. Read the [Permissions](#permissions) section for more information
about the available permissions.


## Permissions

| ID                 | Description                   | Notes                                                                           |
|:-------------------|:------------------------------|:--------------------------------------------------------------------------------|
| `basic_access`     | Can access the Bulletin Board | Grants read access to the bulletin board                                        |
| `manage_bulletins` | Can manage bulletins          | Grants the right to edit and delete existing bulletins and create new bulletins |


## Changelog

See [CHANGELOG.md](https://github.com/ppfeufer/aa-bulletin-board/blob/master/CHANGELOG.md)


## Contributing

You want to contribute to this project? That's cool!

Please make sure to read the [contribution guidelines](https://github.com/ppfeufer/aa-bulletin-board/blob/master/CONTRIBUTING.md) (I promise,
it's not much, just some basics)
