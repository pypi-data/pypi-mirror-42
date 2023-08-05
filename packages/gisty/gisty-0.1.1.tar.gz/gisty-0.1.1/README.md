# Gisty

A simple cli utility for retrieving Gists on GitHub.

Written as part of a technical test.

> Using the Github API you should query a user's publicly available github gists. The script should then tell you when a new gist has been published.

### Installation

> Note. Requires python3

```bash
pip3 install gisty
```

### Getting started

List all Gists

```bash
gisty firegrass --format list --colour
```

Find Gists this year

```bash
gisty firegrass --since 'last year' --order 'desc'
```

Watch for new Gists

```bash
gisty firegrass --watch --since 'now'
```

Once you hit GitHub IP address rate limiting (60 requests per hour), you can use a personal access token.

```bash
gisty firegrass --auth USERNAME:TOKEN
```

To debug the script and see the underlying GitHub api requests use `-v`

```bash
gisty firegrass -v
```

## Development

Using [Pipenv](https://pipenv.readthedocs.io) to manage dependencies and virtualenvs.

```bash
# Install locally
python3 setup.py install

# Build and push to test PyPI
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### Potential improvements

- More test coverage (and reports in Travis)
- Use Travis to matrix tests in all Python3 versions
