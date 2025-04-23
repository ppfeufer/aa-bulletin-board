# AA Bulletin Board<a name="aa-bulletin-board"></a>

[![Version](https://img.shields.io/pypi/v/aa-bulletin-board?label=release)](https://pypi.org/project/aa-bulletin-board/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-bulletin-board)](https://github.com/ppfeufer/aa-bulletin-board/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-bulletin-board)](https://pypi.org/project/aa-bulletin-board/)
[![Django](https://img.shields.io/pypi/djversions/aa-bulletin-board?label=django)](https://pypi.org/project/aa-bulletin-board/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ppfeufer/aa-bulletin-board/master.svg)](https://results.pre-commit.ci/latest/github/ppfeufer/aa-bulletin-board/master)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)
[![Automated Checks](https://github.com/ppfeufer/aa-bulletin-board/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-bulletin-board/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-bulletin-board/branch/master/graph/badge.svg?token=UCXABR42QC)](https://codecov.io/gh/ppfeufer/aa-bulletin-board)
[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-bulletin-board/svg-badge.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-forum/blob/master/CODE_OF_CONDUCT.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

Simple bulletin board for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth)

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Before You Install This Module](#before-you-install-this-module)
- [Installation](#installation)
  - [Step 1: Install the Package](#step-1-install-the-package)
  - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    - [Settings in `/home/allianceserver/myauth/myauth/settings/local.py`](#settings-in-homeallianceservermyauthmyauthsettingslocalpy)
    - [Settings in `/home/allianceserver/myauth/myauth/urls.py`](#settings-in-homeallianceservermyauthmyauthurlspy)
  - [Step 3: Configure Your Webserver](#step-3-configure-your-webserver)
    - [Apache](#apache)
    - [Nginx](#nginx)
  - [Step 4: Finalizing the Installation](#step-4-finalizing-the-installation)
  - [Step 5: Set Up Permissions](#step-5-set-up-permissions)
- [Permissions](#permissions)
- [Changelog](#changelog)
- [Translation Status](#translation-status)
- [Contributing](#contributing)

<!-- mdformat-toc end -->

______________________________________________________________________

![AA Bulletin Board](https://raw.githubusercontent.com/ppfeufer/aa-bulletin-board/master/docs/images/presentation/aa-bulletin-board.jpg "AA Bulletin Board")

## Before You Install This Module<a name="before-you-install-this-module"></a>

This app needs quite some configuration done before working properly. You need to
modify your Apache/Nginx configuration as well as the global URL config of Alliance
Auth. So please only install if you know what you're doing/feel comfortable to make
these kinds of changes. For your own sanity, and mine :-)

## Installation<a name="installation"></a>

> [!IMPORTANT]
>
> Please make sure you meet all preconditions before you proceed.

- AA Bulletin Board is a plugin for Alliance Auth. If you don't have Alliance Auth
  running already, please install it first before proceeding. (see the official
  [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html)
  or details)
- Aa Bulletin Board needs a couple of changes made to your Webserver and Alliance
  Auth configuration. So make sure you know how to do so. The steps needed will be
  described in this document, but you need to understand what will be changed.

### Step 1: Install the Package<a name="step-1-install-the-package"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth
installation Then install the latest release directly from PyPi.

```shell
pip install aa-bulletin-board
```

### Step 2: Configure Alliance Auth<a name="step-2-configure-alliance-auth"></a>

#### Settings in `/home/allianceserver/myauth/myauth/settings/local.py`<a name="settings-in-homeallianceservermyauthmyauthsettingslocalpy"></a>

This is fairly simple, configure your AA settings (`local.py`) as follows:

```python
# AA Bulletin Board
INSTALLED_APPS += [
    "django_ckeditor_5",  # https://github.com/hvlads/django-ckeditor-5
    "aa_bulletin_board",  # https://github.com/ppfeufer/aa-bulletin-board
]

# Django CKEditor 5 Configuration
if "django_ckeditor_5" in INSTALLED_APPS:
    # CKEditor 5 File Upload Configuration
    CKEDITOR_5_FILE_UPLOAD_PERMISSION = (
        "authenticated"  # Possible values: "staff", "authenticated", "any"
    )

    MEDIA_URL = "/media/uploads/"
    MEDIA_ROOT = "/var/www/myauth/media/uploads"

    customColorPalette = [
        {"color": "hsl(4, 90%, 58%)", "label": "Red"},
        {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
        {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
        {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
        {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
        {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
    ]

    CKEDITOR_5_CONFIGS = {
        "default": {
            "toolbar": [
                "heading",
                "|",
                "bold",
                "italic",
                "link",
                "bulletedList",
                "numberedList",
                "blockQuote",
            ],
        },
        "extends": {
            "blockToolbar": [
                "paragraph",
                "heading1",
                "heading2",
                "heading3",
                "|",
                "bulletedList",
                "numberedList",
                "|",
                "blockQuote",
            ],
            "toolbar": [
                "heading",
                "|",
                "outdent",
                "indent",
                "|",
                "bold",
                "italic",
                "link",
                "underline",
                "strikethrough",
                "subscript",
                "superscript",
                "highlight",
                "|",
                "insertImage",
                "mediaEmbed",
                "|",
                "bulletedList",
                "numberedList",
                "todoList",
                "insertTable",
                "|",
                "blockQuote",
                "codeBlock",
                "|",
                "fontSize",
                "fontFamily",
                "fontColor",
                "fontBackgroundColor",
                "removeFormat",
                "|",
                "sourceEditing",
            ],
            "image": {
                "toolbar": [
                    "imageTextAlternative",
                    "|",
                    "imageStyle:alignLeft",
                    "imageStyle:alignRight",
                    "imageStyle:alignCenter",
                    "imageStyle:side",
                    "|",
                ],
                "styles": [
                    "full",
                    "side",
                    "alignLeft",
                    "alignRight",
                    "alignCenter",
                ],
            },
            "table": {
                "contentToolbar": [
                    "tableColumn",
                    "tableRow",
                    "mergeTableCells",
                    "tableProperties",
                    "tableCellProperties",
                ],
                "tableProperties": {
                    "borderColors": customColorPalette,
                    "backgroundColors": customColorPalette,
                },
                "tableCellProperties": {
                    "borderColors": customColorPalette,
                    "backgroundColors": customColorPalette,
                },
            },
            "heading": {
                "options": [
                    {
                        "model": "paragraph",
                        "title": "Paragraph",
                        "class": "ck-heading_paragraph",
                    },
                    {
                        "model": "heading1",
                        "view": "h1",
                        "title": "Heading 1",
                        "class": "ck-heading_heading1",
                    },
                    {
                        "model": "heading2",
                        "view": "h2",
                        "title": "Heading 2",
                        "class": "ck-heading_heading2",
                    },
                    {
                        "model": "heading3",
                        "view": "h3",
                        "title": "Heading 3",
                        "class": "ck-heading_heading3",
                    },
                ]
            },
        },
        "list": {
            "properties": {
                "styles": "true",
                "startIndex": "true",
                "reversed": "true",
            }
        },
    }
```

#### Settings in `/home/allianceserver/myauth/myauth/urls.py`<a name="settings-in-homeallianceservermyauthmyauthurlspy"></a>

Now let's move on to editing the global URL configuration of Alliance Auth. To do so,
you need to open `/home/allianceserver/myauth/myauth/urls.py` and change the
following block right before the `handler` definitions:

```python
from django.apps import apps  # Only if not already imported earlier
from django.conf import settings  # Only if not already imported earlier
from django.conf.urls.static import static  # Only if not already imported earlier
from django.urls import path  # Only if not already imported earlier

# If django_ckeditor_5 is loaded
if apps.is_installed("django_ckeditor_5"):
    # URL configuration for CKEditor 5
    urlpatterns = (
        [
            path("ckeditor5/", include("django_ckeditor_5.urls")),
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + urlpatterns
    )
```

After this, your `urls.py` should look similar to this:

```python
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from allianceauth import urls

# Alliance auth urls
urlpatterns = [
    path(r"", include(urls)),
]

# If django_ckeditor_5 is loaded
if apps.is_installed("django_ckeditor_5"):
    # URL configuration for CKEditor 5
    urlpatterns = (
        [
            path("ckeditor5/", include("django_ckeditor_5.urls")),
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + urlpatterns
    )

handler500 = "allianceauth.views.Generic500Redirect"
handler404 = "allianceauth.views.Generic404Redirect"
handler403 = "allianceauth.views.Generic403Redirect"
handler400 = "allianceauth.views.Generic400Redirect"
```

### Step 3: Configure Your Webserver<a name="step-3-configure-your-webserver"></a>

Your webserver needs to know from where to serve the uploaded images, of course, so we
have to tell it.

#### Apache<a name="apache"></a>

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

#### Nginx<a name="nginx"></a>

In order to let Nginx know where to find the uploaded files, you need to add a new
location rule to the configuration.

```nginx
location /media {
    alias /var/www/myauth/media;
    autoindex off;
}
```

Restart your Nginx webserver.

### Step 4: Finalizing the Installation<a name="step-4-finalizing-the-installation"></a>

Run static files collection and migrations

```shell
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for Auth

### Step 5: Set Up Permissions<a name="step-5-set-up-permissions"></a>

Now it's time to set up access permissions for your new module. You can do so in
your admin backend. Read the [Permissions](#permissions) section for more information
about the available permissions.

## Permissions<a name="permissions"></a>

| ID                 | Description                   | Notes                                                                           |
| :----------------- | :---------------------------- | :------------------------------------------------------------------------------ |
| `basic_access`     | Can access the Bulletin Board | Grants read access to the bulletin board                                        |
| `manage_bulletins` | Can manage bulletins          | Grants the right to edit and delete existing bulletins and create new bulletins |

## Changelog<a name="changelog"></a>

See [CHANGELOG.md](https://github.com/ppfeufer/aa-bulletin-board/blob/master/CHANGELOG.md)

## Translation Status<a name="translation-status"></a>

[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-bulletin-board/multi-auto.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)

Do you want to help translate this app into your language or improve the existing
translation? - [Join our team of translators][weblate engage]!

## Contributing<a name="contributing"></a>

Do you want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines].\
(I promise, it's not much, just some basics)

<!-- Links -->

[contribution guidelines]: https://github.com/ppfeufer/aa-bulletin-board/blob/master/CONTRIBUTING.md "Contribution Guidelines"
[weblate engage]: https://weblate.ppfeufer.de/engage/alliance-auth-apps/ "Weblate Translations"
