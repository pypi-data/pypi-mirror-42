# Gisty

A cli utility for retrieving Gists on GitHub.

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

## Development

```bash
# Install locally
python3 setup.py install --user

# Build and push to test PyPI
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
