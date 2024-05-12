# fermo_core_extras
Collection of pre- and post-processing functionality for fermo_core

Download, Installation
============

- Create a virtual environment (e.g. with `conda`)
- Install `python 3.11.4`
- Install `fermo_core_extras` with `pip install -e .` (while in the `fermo_core_extras`
  directory)

Additionally, `fermo_core_extas/mibig_spectral_library` requires:
- An installed and active version of `docker`

Background
==========

`Fermo_core_extras/mibig_spectral_library` governs the creation a spectral library from the MIBiG database. For more information please see its respective [README_MIBIG_SPECTRAL_LIB.md](fermo_core_extras/mibig_spectral_library/README_MIBIG_SPECTRAL_LIB.md)

For developers
==============

For guidelines regarding contributing to this project, see
[CONTRIBUTING](CONTRIBUTING.md).

Install development dependencies with `pip install -e '.[dev]'`.

Several tools are used to keep code and style consistent.
These tools include:
- `black` (v23.3.0)
- `flake8` (v6.0.0)

We recommend using the package `pre-commit` to run these tools before committing.
`pre-commit` can be installed with `pre-commit install`.

About
=====

## Dependencies

A list of dependencies can be found in the file [pyproject.toml](pyproject.toml).

## License

MIT license (see [LICENSE](LICENSE))

Authors
=======

- Mitja M. Zdouc (Wageningen University)
- Koen van Ingen (bachelor student Molecular Life Sciences at Wageningen University)
