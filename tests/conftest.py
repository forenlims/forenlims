# tests/conftest.py
from typing import Any

import pytest

# Provide database access for all tests automatically
#from cid.locals import set_cid
#import uuid


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db: Any) -> None: # noqa: ANN401
    """Ensures the database is available for all tests."""
    pass
