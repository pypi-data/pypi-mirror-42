from fastgenomics.data import FGData
import logging
import pytest


def test_env_input_file_mapping(data_root, data_root_no_mapping_file, caplog):
    caplog.set_level(logging.DEBUG)
    mapping = '{"x": "y"}'

    # both env variable and the file mapping file are there
    with pytest.raises(RuntimeError):
        FGData(data_root, env_input_file_mapping=mapping)

    # neither is there
    with pytest.raises(RuntimeError):
        FGData(data_root_no_mapping_file)

    # no input file mapping but env variable defined
    data = FGData(data_root_no_mapping_file, env_input_file_mapping=mapping)

    assert "x" in data.input_file_mapping
    assert data.input_file_mapping["x"] == "y"
    assert any(
        'Loading the file mapping from an environmental variable "INPUT_FILE_MAPPING".'
        in x.message
        for x in caplog.records
    )
