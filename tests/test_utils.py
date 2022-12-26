from cliriculum.utils import copy_files
import pytest


def test_copy_files(tmp_path, fixtures_path):
    file_ = fixtures_path / "contact.json"
    with pytest.raises(TypeError):
        copy_files(file_, tmp_path)
    
    copy_files([file_], dst=tmp_path)
