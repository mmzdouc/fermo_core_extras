"""Main entry point to the MIBiG spectral library preparation

Copyright (c) 2022 to present Koen van Ingen, Mitja M. Zdouc, PhD and individual
 contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from sys import argv

from fermo_core_extras.mibig_spectral_library.data_processing.class_parsing_manager import (
    ParsingManager,
)
from fermo_core_extras.mibig_spectral_library.data_processing.class_script_manager import (
    LibraryPrep,
)


def run_library_prep():
    """Drives the MIBiG spectral library pipeline and enables logging"""
    data.make_output_folder()
    logger = data.run_logger()

    logger.info("Extracting metabolites and metadata from the MIBiG folder")
    data.process_mibig()

    logger.info("Started CFM-ID ms/ms spectra prediction for MIBiG entries")
    data.run_cfmid(logger)
    logger.info("CFM-ID ms/ms spectra prediction completed")

    logger.info("Adding metadata to CFM-ID output and generating .mgf file")
    data.run_metadata()
    logger.info("All actions completed successfully")


if __name__ == "__main__":
    arguments_dictionary = ParsingManager.run_parser(argv[1:])
    data = LibraryPrep(**arguments_dictionary)
    run_library_prep()
