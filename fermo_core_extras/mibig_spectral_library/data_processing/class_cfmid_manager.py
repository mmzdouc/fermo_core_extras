"""Runs the program CFM-ID in a dockerized environment

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

import subprocess
from typing import Self

from pydantic import BaseModel


class CfmidManager(BaseModel):
    """Class that runs the program CFM-ID in a dockerized environment

    Attributes:
        prepped_cfmid_file: Path of input file containing metabolite name, SMILES.
        cfm_id_folder: Path of cfm-id output folder where it will create 1 fragmentation
         spectrum file per metabolite
        prune_probability: Probability below which metabolite fragments will be excluded
         from predictions
        niceness: Niceness value to run the CFM-ID analysis in.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    prepped_cfmid_file: str
    cfm_id_folder: str
    prune_probability: str
    niceness: str

    def run_program(self: Self, logger):
        """Builds and executes the command to run CFM-ID in dockerized environment
        using nice -16

        Arguments:
            logger: Logger instance that writes to terminal and spectral_library_creator.log in s_output
        """
        command = (
            f"nice -{self.niceness} docker run --rm=true"
            f" -v $(pwd):/cfmid/public/ -i wishartlab/cfmid:latest sh -c"
            f' "cd /cfmid/public/; cfm-predict {self.prepped_cfmid_file}'
            f" {self.prune_probability} "
            f"/trained_models_cfmid4.0/[M+H]+/param_output.log"
            f" /trained_models_cfmid4.0/[M+H]+/param_config.txt 1"
            f' {self.cfm_id_folder}"'
        )
        logger.debug(f"running docker with the following command:{command}")
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        for line in iter(process.stdout.readline, b""):
            logger.info(line.decode().strip())

        process.communicate()
