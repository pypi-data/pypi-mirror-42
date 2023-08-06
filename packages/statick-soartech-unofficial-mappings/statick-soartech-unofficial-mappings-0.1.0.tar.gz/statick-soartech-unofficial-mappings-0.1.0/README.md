# SoarTech Unofficial Statick Rule Mappings

| Service | Status |
| ------- | ------ |
| Build   | [![Travis-CI](https://api.travis-ci.org/soartech/statick-soartech-unofficial-mappings.svg?branch=master)](https://travis-ci.org/soartech/statick-soartech-unofficial-mappings/branches) |
| PyPI    | [![PyPI version](https://badge.fury.io/py/statick-soartech-unofficial-mappings.svg)](https://badge.fury.io/py/statick-soartech-unofficial-mappings) |
| Codecov | [![Codecov](https://codecov.io/gh/soartech/statick-soartech-unofficial-mappings/branch/master/graphs/badge.svg)](https://codecov.io/gh/soartech/statick-soartech-unofficial-mappings) |

The SoarTech Unofficial Statick Rule Mappings plugin adds additional rule mappings to the the CMU SEI rule mappings provided by Statick.
These mappings have not been evaluated by CMU SEI and are for experimental use only.

## Additions to Statick
This plugin adds several new rule mappings to Statick.
The plugin should be automatically detected the next time you run Statick.
In order to use these mappings, run Statick with the flag `--mapping-file-suffix=soartech-unofficial`.
If this plugin does not provide a mapping file for a given tool, the default Statick mapping file will be used.
