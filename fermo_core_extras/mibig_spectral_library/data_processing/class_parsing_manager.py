"""Manages methods related to argparse-based command line argument parsing.

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

from argparse import ArgumentParser


class ParsingManager:
    """Manages methods related to argparse-based command line argument parsing."""

    @staticmethod
    def run_parser(commandline_args):
        """Parses user input and returns a formatted dictionary

        Attributes:
            commandline_args: Raw command line input from argv[1:].

        Returns:
            args.mode: Mode that the program will be run in.
        """
        parser = ArgumentParser(
            description="Generates a spectral library from a folder of MIBiG entries"
            " using CFM-ID"
        )
        parser.add_argument(
            "-i",
            "--input",
            help="Path of the mibig.json folder containing .json files.",
            required=True,
        )
        parser.add_argument(
            "-o",
            "--output_folder",
            help="Path of the output folder containing intermediate files and the .mgf"
            " MIBiG spectral library",
            required=True,
        )
        parser.add_argument(
            "-p",
            "--prune",
            help="Pruning threshold for CFM-ID. Values between 1 and 0. Default=0.001",
            required=False,
            default="0.001",
        )
        parser.add_argument(
            "-n",
            "--niceness",
            help="Set resource demand for CFM-ID using nice. "
            "Value between 20 and 0 with 0 being the most demanding. Default=16",
            default="16",
            required=False,
        )
        parser.add_argument(
            "-l",
            "--level",
            help="Sets logging level for console and log file output. Default=INFO",
            default="INFO",
            required=False,
        )
        parser.add_argument(
            "-m",
            "--mass_threshold",
            help="Sets a maximum molar mass threshold. CFM-ID can't analyse extremely large molecules. Default=2000",
            default=2000,
            required=False,
        )
        args = parser.parse_args(commandline_args)
        args_dict = {}
        for arg_name, arg_value in vars(args).items():
            args_dict[arg_name] = arg_value

        return args_dict
