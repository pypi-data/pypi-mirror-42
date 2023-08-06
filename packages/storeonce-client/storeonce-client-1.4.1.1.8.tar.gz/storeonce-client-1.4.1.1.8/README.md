# HPE StoreOnce SDK Python Client

The Python package containing an API that wraps the Hewlett Packard Enterprise StoreOnce REST interface.

## Requirements

* Python 2.7 and 3.4+

## Installation

You can install this package using the following pip command:

```sh
pip install .
```

## Documentation

The documentation can be built using the command:

```
sphinx-build -b html documentation <destination path>
```
It should be noted that you will need to have Sphinx and the Sphinx RTD theme already installed in your environment; 
these can be installed with the pip command:
```
pip install sphinx && pip install sphinx_rtd_theme
```

## Known issues

Known issues are listed in the documentation [here](./documentation/issues.rst).

## Contributions

Please be aware that a code generator creates and manages this code as part of a product release cycle.

This means it won't be possible for us to merge the pull requests you raise.