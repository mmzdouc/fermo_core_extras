"""Manages the classes of mibig_spectral_library

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

import os
from pathlib import Path
from typing import Self

from pydantic import BaseModel

from fermo_core_extras.mibig_spectral_library.data_processing.class_cfmid_manager import (
    CfmidManager,
)
from fermo_core_extras.mibig_spectral_library.data_processing.class_logger import Logger
from fermo_core_extras.mibig_spectral_library.data_processing.class_postprocessing_manager import (
    PostprocessingManager,
)
from fermo_core_extras.mibig_spectral_library.data_processing.class_preprocessing_manager import (
    PreprocessingManager,
)


class LibraryPrep(BaseModel):
    """Class that manages the other MIBiG spectral library classes.

    Attributes:
        input: Path of the mibig.json folder containing .json files.
        output_folder: Path of the output folder containing intermediate files and the .mgf MIBiG spectral library.
        prune: Probability below which metabolite fragments will be excluded from predictions.
        niceness: Niceness value to run the CFM-ID analysis in.
        level: Logging level that will be used in the library.
        mass_threshold: Threshold for maximum peptide mass.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    input: str
    output_folder: str
    prune: float
    niceness: int
    level: str
    mass_threshold: int

    def process_mibig(self: Self):
        """Processes the .json files from MIBiG into input for CFM-ID and
        metadata file."""
        args_dict = {
            "prepped_cfmid_file": str(
                Path(self.output_folder).joinpath("cfm_id_input.txt")
            ),
            "prepped_metadata_file": str(
                Path(self.output_folder).joinpath("mibig_metadata.csv")
            ),
            "mass_threshold": self.mass_threshold,
        }
        preprocessed_data = PreprocessingManager(**args_dict)
        file_list = preprocessed_data.extract_filenames(self.input, ".json")
        for file_path in file_list:
            preprocessed_data.extract_metadata(file_path)
        preprocessed_data.write_outfiles()

    def run_cfmid(self: Self, logger):
        """Builds and executes the command to run CFM-ID in dockerized environment
        using nice -16

        Arguments:
            logger: Logger instance that writes to terminal and spectral_library_creator.log in s_output
        """
        args_dict = {
            "prepped_cfmid_file": Path(self.output_folder).joinpath("cfm_id_input.txt"),
            "cfm_id_folder": Path(self.output_folder).joinpath(
                "cfm_id_predicted_spectra"
            ),
            "prune_probability": self.prune,
            "niceness": self.niceness,
        }
        spectra = CfmidManager(**args_dict)
        spectra.run_program(logger)

    def run_metadata(self: Self):
        """Adds real mass, publication IDs and MIBiG cluster IDs to CFM-ID output."""
        args_dict = {
            "cfm_id_folder": str(
                Path(self.output_folder).joinpath("cfm_id_predicted_spectra")
            ),
            "prepped_metadata_file": str(
                Path(self.output_folder).joinpath("mibig_metadata.csv")
            ),
            "mgf_file": str(
                Path(self.output_folder).joinpath("mibig_spectral_library.mgf")
            ),
        }
        metadata = PostprocessingManager(**args_dict)
        file_list = PreprocessingManager.extract_filenames(
            f"{self.output_folder}/cfm_id_predicted_spectra", ".log"
        )
        metadata.extract_metadata()
        metadata.add_metadata_cfmid_files(file_list)
        metadata.format_log_dict()
        metadata.write_mgf_to_file()

    def make_output_folder(self: Self):
        """Check for the existence of the output folder and makes one if required"""
        if not os.path.isdir(self.output_folder):
            os.makedirs(self.output_folder)

    def run_logger(self: Self):
        """Enables colored logging throughout the mibig_spectral_library pipeline

        Returns:
            logger: Logger instance that writes to terminal and spectral_library_creator.log in s_output
        """
        args_dict = {"logging_level": self.level, "output_folder": self.output_folder}
        logging = Logger(**args_dict)
        logger = logging.enable_logging()
        return logger
