# Dict Pretty Printer

[pypi homepage](https://pypi.org/project/xxx/)

## Install

```bash
pip3 install xxx
```

only python3 supported.

## Usage


## Developments

#### Setup development env

```bash
$ pip3 install -r requirements-dev.txt
```

or simply

```bash
$ make dev-setup
```

#### Packaging and release to pypi


1. Unittest

```bash
$ make test
```

2. Testing before release

```bash
$ make build
$ make install
```

3. Run examples:

```bash
$ python3 examples/show_placeholder.py
```

4. Release to pypi

```bash
$ make build
$ make upload
```
