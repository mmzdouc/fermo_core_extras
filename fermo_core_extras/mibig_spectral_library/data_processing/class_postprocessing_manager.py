"""Adds real mass, database IDs and MIBiG cluster IDs to CFM-ID output.

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

from typing import Dict, List, Self

import pandas as pd
from pydantic import BaseModel


class PostprocessingManager(BaseModel):
    """Creates a spectral library .mgf file from CFM-ID input combined with metadata
     from preprocessing_manager.py

    Attributes:
        cfm_id_folder: Path of cfm-id output folder where it will create 1 fragmentation
         spectrum file per
        metabolite.
        prepped_metadata_file: Path of parsing_manager output file containing metabolite
         name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        metadata: Dictionary with metabolite_name as key and metadata in a dict of
         values: SMILES, chemical formula, molecular mass, database IDs, MIBiG entry ID.
        log_dict: Dictionary with metabolite_name as key and with value a list of .log
         file lines, now with metadata.
        preprocessed_mgf_list: A triple nested list containing the data on file, lines
         and different columns within
        those lines respectively.
        mgf_file: Path of the .mgf file spectral library generated by this pipeline

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    cfm_id_folder: str
    prepped_metadata_file: str
    mgf_file: str
    metadata: Dict = {}
    log_dict: Dict = {}
    preprocessed_mgf_list: List = []

    def extract_metadata(self: Self):
        """Extracts the relevant metadata from the metadata .csv file and
        adds a new entry to self_metadata for every metabolite found.
        """
        metadata_table = pd.read_csv(self.prepped_metadata_file, sep=" ")
        for entry in metadata_table.iterrows():
            self.metadata[entry[1][0]] = {
                "SMILES": entry[1][1],
                "chemical formula": entry[1][2],
                "molecular mass": entry[1][3],
                "database ID": entry[1][4],
                "MIBiG ID": entry[1][5],
            }

    def add_metadata_cfmid_files(self: Self, file_list):
        """Adds the missing metadata to all files in the CFM-ID output folder and saves
        result in log_dict."""

        def _subroutine(filename):
            metabolite_name = (
                filename.removesuffix(".log")
                .removeprefix(self.cfm_id_folder)
                .strip("\\/")
            )
            return metabolite_name

        for file_name in file_list:
            with open(file_name) as file:
                lines = file.readlines()
                metabolite = _subroutine(file_name)
                for linenr in range(len(lines)):
                    if (
                        lines[linenr].startswith("#PMass")
                        and metabolite in self.metadata
                    ):
                        lines = (
                            lines[0 : linenr + 1]
                            + [
                                "MIBIGACCESSION="
                                + self.metadata[metabolite]["MIBiG ID"]
                                + "\n",
                            ]
                            + lines[linenr + 1 :]
                        )

                self.log_dict[metabolite] = lines

    def format_log_dict(self: Self):
        """Formats the .log files in log_dict to an .mgf like format in
        preprocessed_mgf_list."""

        for _, lines in self.log_dict.items():
            new_lines = []
            for line in lines:
                if not line.startswith("energy"):
                    if line.startswith("\n"):
                        break
                    else:
                        new_lines.append(line)

            for linenr in range(len(new_lines)):
                if new_lines[linenr].startswith("#In-silico"):
                    new_lines[linenr] = (
                        f'INSILICO={lines[linenr][10:].replace(" ", "")}'
                    )

                if new_lines[linenr].startswith("#PREDICTED BY"):
                    new_lines[linenr] = (
                        f'PREDICTEDBY={lines[linenr][13:].replace(" ", "")}'
                    )

                if new_lines[linenr].startswith("#ID="):
                    new_lines[linenr] = f'ID={lines[linenr][4:].replace(" ", "")}'

                if new_lines[linenr].startswith("#SMILES="):
                    new_lines[linenr] = f'SMILES={lines[linenr][8:].replace(" ", "")}'

                if new_lines[linenr].startswith("#InChiKey="):
                    new_lines[linenr] = (
                        f'INCHIKEY={lines[linenr][10:].replace(" ", "")}'
                    )

                if new_lines[linenr].startswith("#Formula="):
                    new_lines[linenr] = f'FORMULA={lines[linenr][9:].replace(" ", "")}'

                if new_lines[linenr].startswith("#PMass="):
                    new_lines[linenr] = f'PEPMASS={lines[linenr][7:].replace(" ", "")}'

            entry_list = []
            for line in new_lines:
                entries = line.replace("\n", "").split(" ")
                entry_list.append(entries)

            self.preprocessed_mgf_list.append(entry_list)

    def write_mgf_to_file(self: Self):
        """Removes duplicate peaks from spectra and writes the spectral library .mgf
        file."""
        output_table = []

        def _subroutine(dataframe_string):
            """Removes the leading spaces that panda adds"""
            df_list = dataframe_string.split("\n")
            new_list = []
            for line in df_list:
                new_list.append(line.strip())

            return "\n".join(new_list)

        for file in self.preprocessed_mgf_list:
            # We want to do modification on only the peaks
            rows = []
            for entry in file[8:]:
                rows.append(entry[0])

            peaks_dataframe = pd.DataFrame(file[8:], index=rows)
            peaks_dataframe.columns = [
                "F" + str(i + 1) for i in range(peaks_dataframe.shape[1])
            ]
            peaks_dataframe["F2"] = peaks_dataframe["F2"].astype(float)
            peaks_dataframe.sort_values("F2", inplace=True, ascending=False)
            peaks_dataframe.drop_duplicates(
                subset="F1", keep="first", ignore_index=False, inplace=True
            )

            # Unpack the header lines from the nested list
            lines = []
            for entry in file[0:8]:
                lines.append(entry[0])

            header = "\n".join(lines)
            output_table.append(
                "BEGIN IONS\n"
                + header
                + "\n"
                + _subroutine(
                    peaks_dataframe[["F1", "F2"]].to_string(index=False, header=False)
                )
                + "\nEND IONS\n\n"
            )
        with open(self.mgf_file, "w") as f:
            for entry in output_table:
                f.write(entry)
