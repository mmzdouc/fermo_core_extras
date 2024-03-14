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

This module for is used to prepare a spectral tandem mass spectrometry (MS/MS) library from all entries in the Minimum
Information about a Biosynthetic Gene cluster (MIBiG) by using Competitive Fragmentation Modeling for Metabolite
Identification (CFM-ID). This is very computationally intensive and will take several days, as such it is only
recommended if one wants to run the genomics module of FERMO as a command line tool.

All the steps in this pipeline can be run through the following command:

`python main.py --input <mibig_folder> --output <output_folder>`

Additionally, the following parameters can be added:
- `--prune < 1-0 >` Peak pruning threshold below which CFM-ID will ignore peaks, default = 0.001 with CFM-ID skipping peaks lower than 0.1% abundance.
- `--niceness < 0-20 >` Resource prioritization parameter used by nice in the CFM-ID fragmentation prediction, default = 16 with 20 being lowest priority and 0 being equal to most other running processes on the machine.
- `--level <logging_level>` Lowest logging level to display. Choices: DEBUG, INFO, WARNING, ERROR, CRITICAL.

Data compatability
=====

- Input data for the MIBiG preprocessing step must be a folder of .json files following the structure of MIBiG.

Background
====
(Link to bachelor thesis later)

Natural products, also known as secondary or specialized metabolites, are small molecules produced by living organisms.
Usually, natural products are not required for the organisms survival but often grant an evolutionary advantage
due to their remarkable biological properties, such as antibiotic activities. Therefore, secondary metabolites see many
uses in the fields of medicine and agriculture. Traditionally, these compounds were found by performing bioactivity
assays with consecutive isolation and characterisation. However, these natural products are not uniformly distributed
in nature. Some are very common, while others might be so rare to be only expressed in one out of a million organisms
or might only be expressed in combination with other organisms and specific growth medium. To find any new natural
products at those odds, techniques for rapid and thorough analysis are required. These techniques in turn will result
in a very high amount of data and therefore, computational support is needed to filter the many unimportant molecules,
such as molecules without biological activity or already known secondary metabolites, from the few that are worth
manual inspection for possible further research.
FERMO offers a solution to this problem of secondary metabolite selection. This tool allows in silico selection and
identification of promising candidate molecules from liquid chromatography mass spectrometry (LC-MS) data. LC-MS is an
analytical technique for quick detection and analysis of metabolites. FERMO then facilitates the selection of these
metabolites in a convenient web-based interface and currently has several options of filtering the metabolites that
are likely linked to biological activity.

This software package could be made even better by incorporating antiSMASH results.  AntiSMASH is a tool
for predicting biosynthetic gene clusters (BGC) within the genome of a natural product producer. Usually, these BGC
encode for secondary metabolites, and it is possible to compare predicted BGC against the MIBiG database to obtain
the possible metabolites they encode. If in silico MS/MS spectra can be predicted for the metabolites in the MIBiG
database, these can then be used to annotate the detected BGCs with the experimental LC-MS data.

To accomplish this, a new module for the generation of a spectral library of all MIBiG entries will be made. Secondly,
the main fermo module will need to be modified to allow for the automated comparison between experimental and MIBiG
predicted spectra.

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