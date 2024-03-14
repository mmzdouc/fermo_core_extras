import logging
from typing import Self
import sys
from pathlib import Path

import coloredlogs
from pydantic import BaseModel


class Logger(BaseModel):
    """Enables colored logging throughout the mibig_spectral_library pipeline

    Attributes:
        logging_level: Lowest logging level that will be output to terminal
        output_folder: Path of the output folder containing intermediate files and the .mgf MIBiG spectral library

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    logging_level: str
    output_folder: str

    def enable_logging(self: Self):
        """Enables colored logging throughout the mibig_spectral_library pipeline

        Returns:
                logger: Logger instance that writes to terminal and spectral_library_creator.log in s_output
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(self.logging_level)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.logging_level)

        path_log_file = Path(self.output_folder).joinpath(
            "spectral_library_creator.log"
        )
        file_handler = logging.FileHandler(path_log_file, mode="w")
        file_handler.setLevel(self.logging_level)

        formatter = coloredlogs.ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


if __name__ == "__main__":
    argdict = {"logging_level": "DEBUG", "output_folder": "s_output"}
    testie = Logger(**argdict)
    this_logger = testie.enable_logging()
    this_logger.info("Test info")
    this_logger.error("Test error")
    this_logger.critical("Test critical")
