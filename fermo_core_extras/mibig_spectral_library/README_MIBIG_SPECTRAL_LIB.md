Description
=======

### Overview
Module for the preparation of an MS/MS in silico spectral library from the MIBiG 
database. While this spectral library is intended to be used within the context of 
the knownclusterblast-matching module of `fermo_core`, it can be also used in any 
spectral library matching context. This module has been developed in the scope of a 
bachelor thesis by Koen van Ingen.


Prerequisites
============
In addition to the prerequisites specified in the [README](../../README.md) in the 
parent directory, this module needs an installed and active version of `docker`.


Usage
===========

### Considerations
This pipeline uses [CFM-ID 4.0](https://cfmid.wishartlab.com/) to calculate in 
silico MS/MS fragmentation spectra for SMILES extracted from MIBiG entries. 
Additionally, it takes the output of CFM-ID and produces `matchms`-compatible .mgf 
files, including metadata extracted from MIBiG. Fragmentation spectra calculation is 
 very computationally intensive and will take several days to calculate on a single 
core machine. We recommend splitting up the MIBiG dataset into subsets and running 
multiple processes in parallel. Also, the use of `screen` is recommended.

### Running the module:
- Install the package as specified in the [README](../../README.md) in the 
parent directory
- Install and activate docker in a Linux environment
- Download the MIBiG database in .json format from this [link](https://mibig.secondarymetabolites.org/) and
unpack it to a convenient location.
- Run `poetry run python main.py` (while in the current directory)

### Parameters:

All the steps in this pipeline can be run through the following command:

`poetry run python main.py --input <mibig_folder> --output <output_folder>`

Additionally, the following parameters can be specified:
- `--prune <0-1.0>`: Peak pruning threshold below which CFM-ID will ignore peaks, 
  default 
  = 0.001 with CFM-ID skipping peaks lower than 0.1% abundance.
- `--niceness <0-20>`: Resource prioritization parameter used by nice in the CFM-ID 
  fragmentation prediction, default = 16 with 20 being lowest priority and 0 being equal to most other running processes on the machine.
- `--level <logging_level>`: Lowest logging level to display. Choices: DEBUG, INFO, 
  WARNING, ERROR, CRITICAL.
- `--mass_threshold <molecular mass>`: Maximum molecular mass that will be accepted 
  for CFM-ID spectra generation.

Authors
=======

- Koen van Ingen (bachelor student Molecular Life Sciences at Wageningen University)
- Mitja M. Zdouc (Wageningen University)