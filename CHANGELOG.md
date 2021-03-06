# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


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
