# audittrail/tests/conftest.py
"""
Test fixtures for Audit Trail and CID integration.

Fixtures are app-specific and only imported by audittrail tests.
"""
import uuid
from typing import Callable, Generator

import pytest
from cid import locals as cid_locals
from cid.locals import set_cid


@pytest.fixture
def clean_cid() -> None:
    """
    Ensure clean CID state for each test.

    This fixture does NOT set a CID - it only ensures the thread-local
    storage is clean. Tests must either:
    - Use correlation_id fixture to set a test CID
    - Use custom_cid fixture to set a specific CID
    - Use client fixture to trigger middleware (which sets CID automatically)

    Usage:
        def test_something(clean_cid):
            # CID should be clean at start
            set_cid('my-cid')
            assert get_cid() == 'my-cid'
    """
    # Cleanup before test: Access internal storage directly
    # django-cid uses contextvars, not threading.local in newer versions
    if hasattr(cid_locals, '_cid'):
        cid_locals._cid.set(None)


@pytest.fixture
def correlation_id() -> Generator[str, None, None]:
    """
    Set a unique test CID.

    Use this for unit tests that don't go through Django's request cycle
    (i.e., no middleware). The fixture automatically sets a CID before
    the test runs.

    Usage:
        def test_something(correlation_id):
            # CID is already set by fixture
            assert get_cid() == correlation_id

    For tests using Django's test client, prefer clean_cid instead,
    as the middleware will set the CID automatically.
    """
    test_cid = f"test-{uuid.uuid4()}"
    set_cid(test_cid)
    yield test_cid

    # Cleanup after test
    if hasattr(cid_locals, '_cid'):
        cid_locals._cid.set(None)


@pytest.fixture
def custom_cid() -> Generator[Callable[[str], str], None, None]:
    """
    Set a specific CID for testing.

    Use this when you need control over the exact CID value,
    e.g., for testing CID concatenation or specific formats.

    Usage:
        def test_something(custom_cid):
            my_cid = custom_cid('my-workflow-id-123')
            assert get_cid() == 'my-workflow-id-123'
    """
    def _set_custom_cid(cid: str) -> str:
        set_cid(cid)
        return cid

    yield _set_custom_cid

    # Cleanup after test
    if hasattr(cid_locals, '_cid'):
        cid_locals._cid.set(None)


@pytest.fixture
def external_cid() -> str:
    """
    Generate an external CID (simulating external system).

    Useful for testing CID concatenation scenarios where
    an external lab system sends its own correlation ID.

    Usage:
        def test_concatenation(external_cid, client):
            response = client.get(
                '/',
                HTTP_X_CORRELATION_ID=external_cid
            )
            assert external_cid in response['X-Correlation-ID']
    """
    return f"external-lab-{uuid.uuid4()}"
