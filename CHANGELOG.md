# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [In Development] - Unreleased

### Changed

- More JavaScript modernisation
- CSS now delivered via template bundles
- Minimum dependencies:
  - Python>=3.8

### Removed

- tox tests for AA beta version


## [1.5.1] - 2022-07-11

### Changed

- Templates cleaned up
- Minimum dependencies:
  - Alliance Auth>=2.11.0 (as the latest stable of the 2.x branch for now)


## [1.5.0] - 2022-06-24

### Added

- Versioned static template tag


## [1.4.0] - 2022-03-02

### Added

- Test suite for AA 3.x and Django 4

### Removed

- Deprecated settings

### Changed

- Switched to `setup.cfg` as config file, since `setup.py` is deprecated now
- Minimum dependencies:
  - Alliance Auth>=2.11.0 (as the latest stable of the 2.x branch for now)


## [1.3.0] - 2022-02-28

### Fixed

- Compatibility Fixes (AA 3.x / Django 4):
  - ImportError: cannot import name 'ugettext_lazy' from 'django.utils.translation'
  - URL config in README updated to work with Django 4. **Please make sure to update
    your configuration accordingly!**


## [1.2.1] - 2022-02-02

### Changed

- Using `path` in URL config instead of soon-to-be removed `url`


## [1.2.0] - 2022-01-19

### Added

- Tests for Python 3.11

### Changed

- Minimum dependencies:
  - Alliance Auth>=2.9.4


## [1.1.0] - 2021-11-30

### Changed

- Minimum requirements
  - Python 3.7
  - Alliance Auth v2.9.3


## [1.0.2] - 2021-09-20

### Added

- More tests (test coverage raised to 80%)


## [1.0.1] - 2021-09-19

### Fixed

- An issue where JavaScript and CSS could have been posted in a bulletin
- An issue with unicode characters in bulletin topics


## [1.0.0] - 2021-08-25

### Added

- Group restrictions to bulletins. Bulletins can now be restricted to one or more
  groups. Bulletins without group restrictions can be viewed by everyone who has
  access to the bulletins.

### Fixed

- Small logic error in JavaScript


## [0.1.0-beta.12] - 2021-07-25

### Fixed

- Key in setup.py


## [0.1.0-beta.11] - 2021-07-25

### Updated

- Configuration instructions in README.md to make it easier to understand if you
  have multiple apps that use CKEditor, like `aa-forum`, and how to combine these
  configurations


## [0.1.0-beta.10] - 2021-07-15

### Changed

- CKEditor config changed to prevent possible collisions in static files (see
  [Readme](README.md) for details)


## [0.1.0-beta.9] - 2021-07-08

### Added

- Full example for ``CKEDITOR_CONFIGS`` to README.md

### Changed

- Compatibility with Python 3.9 and Django 3.2 confirmed


## [0.1.0-beta.8] - 2021-06-21

### Fixed

- Spelling
- urlconfig setup in README.md

### Changed

- Code formatting and cleanup
- Slug field in DB to make sure it's unique and uses the right validator


## [0.1.0-beta.7] - 2021-06-13

### Changed

- CSS for cKeditor reverted, it's better as a config in `local.py`
  Add the following to your `local.py`
  ```python
  CKEDITOR_CONFIGS = {"default": {"width": "100%", "height": "45vh"}}
  ````


## [0.1.0-beta.6] - 2021-06-13

### Fixed

- The editor now uses the space it has and doesn't sit in its corner any longer


## [0.1.0-beta.5] - 2021-06-10

### Fixed

- App Name


## [0.1.0-beta.4] - 2021-04-22

### Changed

- Dashboard layout, so it looks nice and doesn't break things when there are HTML
  tags in the excerpts


## [0.1.0-beta.3] - 2021-04-21

### Fixed

- Broken layout in dashboard caused by html tags not being closed in excerpts. With
  this, html tags are removed completely from excerpts on the dashboard


## [0.1.0-beta.2] - 2021-04-20

### Fixed

- Wrong import


## [0.1.0-beta.1] - 2021-04-04

## First release

### Important

If you update from one of the alpha versions, you have to migrate to zero first
before you update this app.

```shell
python manage.py migrate aa_bulleting_board zero
```

Now update the app

```shell
pip install -U aa-bulletin-board
```

And run static collection and migrations again

```shell
python manage.py collectstatic
python manage.py migrate
```
