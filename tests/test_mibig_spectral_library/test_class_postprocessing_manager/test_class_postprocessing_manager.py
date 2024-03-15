import pytest

from mibig_spectral_library.data_processing.class_postprocessing_manager import (
    PostprocessingManager,
)


@pytest.fixture
def initialize_class():
    args_dict = {
        "cfm_id_folder": "tests/test_mibig_spectral_library/test_class_postprocessing_manager/test_spectra",
        "prepped_metadata_file": "tests/test_mibig_spectral_library/test_class_postprocessing_manager/test_metadata.csv",
        "mgf_file": "test.mgf",
    }
    return PostprocessingManager(**args_dict)


def return_file_list():
    file_list = [
        "tests/test_mibig_spectral_library/test_class_postprocessing_manager/test_spectra/(+)-O-methylkolavelool.log",
        "tests/test_mibig_spectral_library/test_class_postprocessing_manager/test_spectra/abyssomicin_C.log",
    ]
    return file_list


def test_postprocessing_manager_format_log_dict_valid(initialize_class):
    test_case = initialize_class
    test_case.extract_metadata()
    test_case.add_metadata_cfmid_files(return_file_list())
    test_case.format_log_dict()
    assert len(test_case.log_dict) == 2
    assert len(test_case.log_dict["(+)-O-methylkolavelool"]) == 291
    assert len(test_case.log_dict["abyssomicin_C"]) == 75
