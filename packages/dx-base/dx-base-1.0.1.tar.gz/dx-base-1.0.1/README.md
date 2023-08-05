# `dx-base` package

A collection of base packages and modules for structural design software.

# Installation

## Development

This repository includes nested submodules. Thus it has to be cloned with the
appropriate options for initializing and cloning the submodules. For more
information on working with submodules see the relevant discussion
[here][nested-submodules] and the reference on [Pro Git][pro-git-submodules].

* Clone the repository

        $ git clone --recurse-submodules git@gitlab.com:d-e/dx-base.git [local-path]

* Create virtual environment:

        $ make install

* Activate virtual environment and run tests:

        $ source venv/bin/activate
        $ nose2

## As a dependency

### From source code

```
$ pip install git://git@gitlab.com/d-e/dx-base.git#egg=dx_base
```

### From Python Package Index (PyPI)

```
$ pip install dx-base
```

## Features

* Structural elements in plane.
* Exceptions with error-code.
* Nodal forces.
* Structural materials.
* Material safety factors.

### Sample usage

```
>>> from dx_base.safety_factors import SafetyFactor
>>> sf = SafetyFactor(1.24, 'persistent', 'serviceability')
>>> sf
1.24
>>> sf.design_situation
'persistent'
>>> sf.limit_stte
'serviceability'
```

## Contribute

Source code lives in https://gitlab.com/d-e/dx-base.

### Code of conduct

We abide by the provisions of [Contributor Coventant Code of Conduct][COC].

### Workflow

Follow this [simplified gitflow model][gitflow].

### Coding standards

* Follow [PEP8 rules](https://www.python.org/dev/peps/pep-0008/).
* Populate docstrings with concise descriptions and the signature
  of the object according to [sphinx guidelines][sphinx-sig]. For a
  complete overview of documentation options see
  [Sphinx docs](http://www.sphinx-doc.org)
* Write unit-tests.

### Versioning

We follow [semantic versioning][semver].

### Review the docs locally

Documentation is generated through continuous-integration (CI). For
review purposes it can be generated locally with:

```
$ make MODPATH=../dx_base -C docs apidoc html
```

For more details on the process run

```
$ make docs-help
```

### Error codes

The package includes coded exceptions. The list of error codes, along
with associated metadata is generated in [`ERROR_CODES.md`](ERROR_CODES.md).

Upon refactoring or additions of coded exceptions this list must be
regenerated through

```
$ make parse-error-codes
```

## Public API

See the [documentation pages](https://d-e.gitlab.io/dx-base/).

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU Affero General Public License](LICENSE) as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

[gitflow]: https://gitlab.com/d-e/dx-utilities/wikis/git-workflow
[semver]: https://semver.org/
[COC]: https://www.contributor-covenant.org/version/1/4/code-of-conduct
[sphinx-sig]: http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists
[nested-submodules]: http://social.d-e.gr/techblog/posts/10-python-projects-with-git-submodules
[pro-git-submodules]: https://git-scm.com/book/en/v2/Git-Tools-Submodules
