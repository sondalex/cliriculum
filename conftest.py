from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    path = Path(__file__)
    return path.parent / "tests" / "fixtures"
