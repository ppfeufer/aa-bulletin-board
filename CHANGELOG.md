# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


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
