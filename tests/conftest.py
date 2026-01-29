# tests/conftest.py
import json
from pathlib import Path
from typing import Any

import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db: Any) -> None:  # noqa: ANN401
    """Ensures the database is available for all tests."""
    pass


@pytest.fixture(scope='session', autouse=True)
def webpack_manifest(tmp_path_factory):
    """
    Provide a minimal manifest for tests when none exists.

    Prefer not to overwrite an existing configured manifest file.
    """
    manifest_content = {
        'main.js': '/static/main.js',
        'main.css': '/static/main.css',
    }
    manifest_json = json.dumps(manifest_content)

    configured = None
    try:
        configured = settings.WEBPACK_LOADER.get('MANIFEST_FILE')
    except Exception:
        configured = None

    if configured:
        configured_path = Path(configured)
        if not configured_path.is_absolute():
            configured_path = Path.cwd() / configured_path
        if configured_path.exists():
            return

        configured_path.parent.mkdir(parents=True, exist_ok=True)
        configured_path.write_text(manifest_json, encoding='utf-8')
        return

    tmpdir = tmp_path_factory.mktemp('webpack')
    manifest_path = tmpdir / 'manifest.json'
    manifest_path.write_text(manifest_json, encoding='utf-8')

    loader = dict(getattr(settings, 'WEBPACK_LOADER', {}))
    loader['MANIFEST_FILE'] = str(manifest_path)
    try:
        settings.WEBPACK_LOADER.update(loader)
    except Exception:
        setattr(settings, 'WEBPACK_LOADER', loader)

    return
