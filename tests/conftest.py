# tests/conftest.py
"""Test configuration and fixtures."""
import atexit
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class _WebpackManifestManager:
    """Manages test webpack manifest creation and cleanup."""

    def __init__(self) -> None:
        self.created_manifest_path: Path | None = None

    def create_manifest(self) -> None:
        """
        Create test webpack manifest before Django settings load.

        This must run before Django imports to ensure webpack_boilerplate
        can find the manifest file when it initializes.

        CRITICAL: Runs at module import time, before pytest collects.
        """
        base_dir = Path(__file__).resolve().parent.parent
        manifest_path = base_dir / 'frontend' / 'build' / 'manifest.json'

        # Skip if manifest already exists (e.g., from actual build)
        if manifest_path.exists():
            return

        manifest_content = {
            'entrypoints': {
                'turbo_drive': {
                    'assets': {
                        'js': ['/static/js/turbo_drive.js'],
                        'css': ['/static/css/turbo_drive.css'],
                    }
                },
                'main': {
                    'assets': {
                        'js': ['/static/js/main.js'],
                        'css': ['/static/css/main.css'],
                    }
                },
            },
            'turbo_drive.js': '/static/js/turbo_drive.js',
            'turbo_drive.css': '/static/css/turbo_drive.css',
            'main.js': '/static/js/main.js',
            'main.css': '/static/css/main.css',
        }

        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest_content, indent=2), encoding='utf-8'
        )

        # Remember that we created this file for cleanup
        self.created_manifest_path = manifest_path

    def cleanup_manifest(self) -> None:
        """
        Remove test-generated manifest after session completes.

        Only removes if created by this manager.
        Does not remove manifests that existed before tests ran.
        """
        if (
            self.created_manifest_path
            and self.created_manifest_path.exists()
        ):
            try:
                self.created_manifest_path.unlink()
            except Exception as e:
                # Log but don't fail - cleanup errors are not critical
                logger.debug(
                    'Failed to cleanup test manifest: %s', e
                )
                logger.debug(
                    'Failed to cleanup test manifest: %s', e
                )


# Create manager instance and register cleanup
_manifest_manager = _WebpackManifestManager()
atexit.register(_manifest_manager.cleanup_manifest)

# Execute manifest creation immediately at import time
# This happens BEFORE Django settings are loaded
_manifest_manager.create_manifest()

# NOW safe to import Django and pytest
import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db: Any) -> None:  # noqa: ANN401
    """Ensures the database is available for all tests."""
