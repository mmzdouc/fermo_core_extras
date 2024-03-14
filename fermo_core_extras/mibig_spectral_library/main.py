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
from typing import Self
from sys import argv
import os

from pydantic import BaseModel

from data_processing.class_cfmid_manager import CfmidManager
from data_processing.class_preprocessing_manager import PreprocessingManager
from data_processing.class_postprocessing_manager import PostprocessingManager
from data_processing.class_parsing_manager import ParsingManager
from data_processing.class_logger import Logger


class LibraryPrep(BaseModel):
    """Class that manages the other MIBiG spectral library classes.

    Attributes:
        input: Path of the mibig.json folder containing .json files.
        output_folder: Path of the output folder containing intermediate files and the .mgf MIBiG spectral library
        prune: Probability below which metabolite fragments will be excluded from predictions.
        niceness: Niceness value to run the CFM-ID analysis in.
        level: Logging level that will be used in the library

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    input: str
    output_folder: str
    prune: str
    niceness: str
    level: str

    def process_mibig(self: Self):
        """Processes the .json files from MIBiG into input for CFM-ID and
        metadata file."""
        args_dict = {
            "prepped_cfmid_file": f"{self.output_folder}/cfm_id_input.txt",
            "prepped_metadata_file": f"{self.output_folder}/mibig_metadata.csv",
        }
        preprocessed_data = PreprocessingManager(**args_dict)
        file_list = preprocessed_data.extract_filenames(self.input, ".json")
        for file_path in file_list:
            preprocessed_data.extract_metadata(file_path)
        preprocessed_data.write_outfiles()

    def run_cfmid(self: Self):
        """Builds and executes the command to run CFM-ID in dockerized environment
        using nice -16"""
        args_dict = {
            "prepped_cfmid_file": f"{self.output_folder}/cfm_id_input.txt",
            "cfm_id_folder": f"{self.output_folder}/cfm_id_predicted_spectra",
            "prune_probability": self.prune,
            "niceness": self.niceness,
        }
        spectra = CfmidManager(**args_dict)
        spectra.run_program()

    def run_metadata(self: Self):
        """Adds real mass, publication IDs and MIBiG cluster IDs to CFM-ID output."""
        args_dict = {
            "cfm_id_folder": f"{self.output_folder}/cfm_id_predicted_spectra",
            "prepped_metadata_file": f"{self.output_folder}/mibig_metadata.csv",
            "mgf_file": f"{self.output_folder}/mibig_spectral_library.mgf",
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

    @staticmethod
    def run_library_prep():
        """Drives the MIBiG spectral library pipeline and enables logging"""
        data.make_output_folder()
        logger = data.run_logger()

        logger.info("Extracting metabolites and metadata from the MIBiG folder")
        data.process_mibig()

        logger.info("Started CFM-ID ms/ms spectra prediction for MIBiG entries")
        data.run_cfmid()
        logger.info("CFM-ID ms/ms spectra prediction completed")

        logger.info("Adding metadata to CFM-ID output and generating .mgf file")
        data.run_metadata()
        logger.info("All actions completed successfully")


if __name__ == "__main__":
    arguments_dictionary = ParsingManager.run_parser(argv[1:])
    data = LibraryPrep(**arguments_dictionary)
    data.run_library_prep()
