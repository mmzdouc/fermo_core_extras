# Fermo Core Extras



[![DOI](https://zenodo.org/badge/766056239.svg)](https://zenodo.org/doi/10.5281/zenodo.11193478)


Description
============
A collection of pre-processing functionality intended to produce 
files used by [fermo_core](github.com/mmzdouc/fermo_core). These modules are  
independent of fermo_core. For detailed information, see the READMEs in the 
individual subdirectories.

Overview
============
The following modules are currently available in `fermo_core_extras`:
- `mibig_spectral_library`: a module to create a MS/MS spectral library from entries 
  of the MIBiG database: [README](fermo_core_extras/mibig_spectral_library/README_MIBIG_SPECTRAL_LIB.md)

Prerequisites and Installation
============
- This project requires a Python installation of `3.11` or higher. See the 
  individual READMEs for further specified prerequisites.
- Install the project with the command `poetry install`

Usage
============
See the individual READMEs for instructions on running them.

Compatibility
============
The modules in this project are intended to be run on Linux command line and have 
only been tested on Ubuntu Linux.

About
=====

### Authors

- Mitja M. Zdouc (Wageningen University)
- Koen van Ingen (bachelor student Molecular Life Sciences at Wageningen University)

### Dependencies

A list of dependencies can be found in the file [pyproject.toml](pyproject.toml).

### License

MIT license (see [LICENSE](LICENSE))


For developers
==============

### Contributing
For guidelines regarding contributing to this project, see
[CONTRIBUTING](CONTRIBUTING.md) and the [CODE OF CONDUCT](CODE_OF_CONDUCT.md).

### Getting Started
- Install development dependencies with `poetry install --with dev`
- Initialize pre-commit with `poetry run pre-commit install`
