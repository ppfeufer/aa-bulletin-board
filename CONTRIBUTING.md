<!-- TOC -->
* [Contributing](#contributing)
  * [Code Formatting](#code-formatting)
  * [Contributing via pull requests](#contributing-via-pull-requests)
    * [Test Coverage](#test-coverage)
  * [Translation](#translation)
<!-- TOC -->

# Contributing

## Code Formatting

This app is utilizing the [Black] code style. Every commit has to adhere to it.

This repository uses [pre-commit] to
verify compliance with formatting rules. To use:

1. Install `pre-commit`.
2. From inside the `aa-bulletin-board` root directory, run `pre-commit install`.
3. You're all done! Code will be checked automatically using git hooks.

You can check if your code to commit adheres to the given style by simply running:
```shell script
pre-commit
```

Or to check all files:
```shell script
pre-commit run --all-files
```

The following will be checked by `pre-commit`:

- No trailing whitespaces (excluded are: minified js and css, .po and .mo files)
- One, and only one, empty line at the end of every file (excluded are: minified js
  and css, .po and .mo files)
- Line ending is LF
- Code formatted according to black code style
- Code conforms with flake8


## Contributing via pull requests

To contribute code via pull request, make sure that you fork the repository and branch
your changes from the `development` branch. Only pull requests towards the development
branch will be considered.

Please make sure you've signed [CCP's Developer License Agreement] by logging in
at [CCP's Developer Portal] before submitting any pull requests.

### Test Coverage

Please make sure your contribution comes with tests covering your additions and
changes. We aim to always improve the test coverage in this project. Pull
requests lowering the test coverage will not be considered for merging.

You can run tests locally via:
```shell
make coverage
```

The full tox-test suite can be run via:
```shell
make tox_tests
```

## Translation

This app is fully translation-ready and translations are handled via [Weblate]. If
you like to contribute to the app's translation or simply improve it, feel free to
register on my [Weblate] site and message me so I can add you to the right group.


<!-- Links -->
[Black]: https://black.readthedocs.io/en/stable/the_black_code_style.html "Black Code Formatter"
[pre-commit]: https://github.com/pre-commit/pre-commit "pre-commit"
[CCP's Developer License Agreement]: https://developers.eveonline.com/resource/license-agreement "CCP's Developer License Agreement"
[CCP's Developer Portal]: https://developers.eveonline.com/ "CCP's Developer Portal"
[Weblate]: https://weblate.ppfeufer.de/ "Weblate"
