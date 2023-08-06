# Okra

Tools for working with GitHub data. It's helpful to have these tools
in a Python package because GitHub data requires moving across directory
structures. 

## Install

```shell
python setup.py install
```

## Tests

```shell
python setup.py test
```

## Documentation

Generate documentation

```shell
python setup.py build_sphinx
```

View documentation

```shell
python -m http.server --directory build/sphinx/html/
```
