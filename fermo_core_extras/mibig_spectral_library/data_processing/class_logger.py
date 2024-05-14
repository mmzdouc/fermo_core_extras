"""Enables colored logging throughout the mibig_spectral_library pipeline

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
