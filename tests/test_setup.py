import pytest
from pathlib import Path
from setup import SetUp


@pytest.fixture
def resource_file():
    root = Path(".")
    return root / "resources" / "setup.dat"


def test_load(resource_file):
    setup = SetUp(resource_file)
    print(setup)
    assert "http" in setup.url and "register.php" in setup.url
