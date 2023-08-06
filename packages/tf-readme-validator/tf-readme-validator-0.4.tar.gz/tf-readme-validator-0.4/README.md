# Terraform README.md Validator

[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/tf-readme-validator/develop/LICENSE)
[![Build Status](https://travis-ci.org/lean-delivery/tf-readme-validator.svg?branch=develop)](https://travis-ci.org/lean-delivery/tf-readme-validator)

## Summary

The validation of a terraform README.md file is performed against the default specification that can be tuned by the config file.

## Installation

* Make sure that https://github.com/segmentio/terraform-docs is installed and terraform-docs is in $PATH
* pip install tf-readme-validator

## Path for files

Take into account that the validator looks for all files (*README.md*, *variables.tf*, *outputs.tf* and *.tf_readme_validator.yml*) only in the current directory.

## Specification

* Description (header, level 2)
* Usage (header, level 2)
* Conditional creation (header, level 3, optional)
* Known issues / Limitations (header, level 3, optional)
* Code included in this module (header, level 3, optional)
* Examples (header, level 3, optional)
* Inputs (header, level 2)
* inputs table (table)
* Outputs (header, level 2)
* outputs table (table)
* Tests (header, level 2, optional)
* Terraform versions (header, level 2)
* Contributing (header, level 2)
* License (header, level 2)
* Authors (header, level 2)

## Input and Output variables

Input and output variables are supposed to be read from **variables.tf** and **outputs.tf** files accordingly.

## Config file

The default specification, inputs and outputs varibales can be tuned by means of a config file *.tf_readme_validator.yml*

### Config file methods

* update - add/update a field
* remove - remove a field
* replace - replace a whole entity

### Config file entities

* readme
* inputs
* outputs

### Config file examples

Do not validate optional fields, inputs variables and read outputs variables from _out.tf_ file.

```yaml
update:
  options:
    optional_validate: False
  inputs:
    validate: False
  outputs:
    path: out.tf
```

Add _Complex Examples_ and _Improvements_ headers for validation and remove _Tests_.

```yaml
update:
  readme:
    Complex Examples:
      type: header
      level: 2
    Improvements:
      type: header
      level: 2

remove:
  readme:
    Tests: False
```

License
-------

Apache

Author Information
------------------

authors:
  - Lean Delivery Team <team@lean-delivery.com>
