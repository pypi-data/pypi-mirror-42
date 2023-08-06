# Takuhai Project

[![PyPI version][pypi-image]][pypi-link]
[![Travis][travis-image]][travis-link]

[pypi-image]: https://badge.fury.io/py/takuhai.svg
[pypi-link]: https://pypi.org/project/takuhai
[travis-image]: https://travis-ci.org/daizutabi/takuhai.svg?branch=master
[travis-link]: https://travis-ci.org/daizutabi/takuhai

An enhanced version of pelican-livereload.py from [1] and [2].

Takuhai automatically builds a Pelican project and reloads browser pages
when an article is modified.

## Reference

1. [Using LiveReload with Pelican](https://merlijn.vandeen.nl/2015/pelican-livereload.html)
2. [LiveReload with Pelican](http://tech.agilitynerd.com/livereload-with-pelican.html)

## Installation

From PyPI

```bash
> pip install takuhai
```

If you write articles using markdown format, you also need to install `markdown` package:

```bash
> pip install markdown
```

## Usage

In a Pelican project directory which contains the `pelicanconf.py`

```bash
> takuhai
```

To show options

```bash
> takuhai --help
```
