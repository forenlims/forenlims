# tests/conftest.py
from typing import Any

# Provide database access for all tests automatically
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db: Any) -> None: # noqa: ANN401
    """Ensures the database is available for all tests."""
    pass
