Repo for the preparation of a spectral library for the FERMO genomics module (fermo_core)

Download, Installation
============

- Create a virtual environment (e.g. with `conda`)
- Install `python 3.11.4`
- Install `fermo_core` with `pip install -e .` (while in the `fermo_core` directory)
- Install and activate docker in a linux environment.
- Download the MIBiG database in .json format from this [link](https://mibig.secondarymetabolites.org/) and
unpack it to a convenient location.
- Execute main.py from the mibig_spectral_library folder

Usage
====

Currently, this module **only** has support for **linux**.
It is used to prepare a spectral tandem mass spectrometry (MS/MS) library from all entries in the Minimum
Information about a Biosynthetic Gene cluster (MIBiG) by using Competitive Fragmentation Modeling for Metabolite
Identification (CFM-ID). This is very computationally intensive and will take several days, as such it is only
recommended if one wants to run the genomics module of FERMO as a command line tool and one wants to generate his own spectral library.

All the steps in this pipeline can be run through the following command:

`python main.py --input <mibig_folder> --output <output_folder>`

Additionally, the following parameters can be added:
- `--prune < 1-0 >` Peak pruning threshold below which CFM-ID will ignore peaks, default = 0.001 with CFM-ID skipping peaks lower than 0.1% abundance.
- `--niceness < 0-20 >` Resource prioritization parameter used by nice in the CFM-ID fragmentation prediction, default = 16 with 20 being lowest priority and 0 being equal to most other running processes on the machine.
- `--level <logging_level>` Lowest logging level to display. Choices: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- `--mass_threshold <molecular mass>` Maximum molecular mass that will be accepted for CFM-ID spectra generation.

Data compatability
=====

- Input data for the MIBiG preprocessing step must be a folder of .json files following the structure of MIBiG.

Background
====

This MIBiG spectral library pipeline, and it's integration into FERMO, are part of my bachelor
thesis. For more information please see the thesis document itself by clicking [here](https://docs.google.com/document/d/1xI45phm3QL6TreeioFiGqSCpSK543esEdKW_mCkF4Ww/edit?usp=sharing) (Available from May 16th 2024)

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

Besides, we use type hinting and document code using Google-style docstrings.
A convenient tool to check documentation style is `pycodestyle`.

We use [Semantic Versioning](http://semver.org/) for versioning.

Slow-running unit tests can be conditionally disabled using the decorator
`@pytest.mark.slow`. To also run slow tests, use `pytest --runslow`. `Pre-commit`
also runs all tests.

About
=====

## Dependencies

A list of dependencies can be found in the file [pyproject.toml](pyproject.toml).

## License

MIT license (see [LICENSE](LICENSE.md))

Authors
=======

- Mitja M. Zdouc (Wageningen University)
- Koen van Ingen (bachelor student Molecular Life Sciences, Wageningen University)