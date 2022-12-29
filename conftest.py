from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    path = Path(__file__)
    return path.parent / "tests" / "fixtures"

@pytest.fixture(scope="module")
def location_path() -> Path:
    path = Path(__file__)
    return path.parent / "tests" / "fixtures" / "location.json"

@pytest.fixture(scope="module")
def location_none() -> None:
    return None

