"""
Shared test fixtures for Tent of Trials backend API tests.

Provides test client, mock data, and authentication fixtures
for testing all public API endpoints.
"""
import pytest
import json
import os
from unittest.mock import MagicMock, patch
from pathlib import Path


# ─── Mock Data Fixtures ───────────────────────────────────────

@pytest.fixture
def sample_build_result():
    """Sample build result tuple: (name, success, elapsed, output, binary)"""
    return ("backend", True, 12.5, "Build completed successfully", "/target/release/tent-backend")


@pytest.fixture
def sample_build_results():
    """Multiple build results for testing summary generation."""
    return [
        ("backend", True, 12.5, "cargo build ok", "/target/release/tent-backend"),
        ("frontend", True, 8.3, "npm run build ok", "/frontend/dist"),
        ("market", False, 3.1, "go build failed: missing module", None),
    ]


@pytest.fixture
def sample_config():
    """Sample configuration dictionary."""
    return {
        "node_id": "test-node-0",
        "consensus": True,
        "log_level": "info",
        "bind_address": "0.0.0.0:8080",
    }


@pytest.fixture
def sample_diagnostic_report():
    """Sample diagnostic report for testing."""
    return {
        "commit_id": "abc12345",
        "generated_at": "2026-01-01T00:00:00+00:00",
        "platform": {"os": "linux", "arch": "x86_64"},
        "modules": [
            {"name": "backend", "success": True, "elapsed": 12.5},
            {"name": "frontend", "success": True, "elapsed": 8.3},
        ],
        "total_modules": 2,
        "passed": 2,
        "failed": 0,
    }


@pytest.fixture
def tmp_diagnostic_dir(tmp_path):
    """Temporary diagnostic directory with sample artifacts."""
    diag_dir = tmp_path / "diagnostic"
    diag_dir.mkdir()
    
    # Create sample logd file
    logd_path = diag_dir / "build-abc12345.logd"
    logd_path.write_bytes(b"fake logd content for testing")
    
    # Create sample metadata
    meta_path = diag_dir / "build-abc12345.json"
    meta_path.write_text(json.dumps({
        "commit_id": "abc12345",
        "generated_at": "2026-01-01T00:00:00+00:00",
    }))
    
    return diag_dir


# ─── Mock Service Fixtures ────────────────────────────────────

@pytest.fixture
def mock_service_registry():
    """Mock service registry for testing service discovery."""
    registry = MagicMock()
    registry.register.return_value = True
    registry.discover.return_value = {
        "backend": {"host": "localhost", "port": 8080},
        "frontend": {"host": "localhost", "port": 3000},
    }
    registry.health_check.return_value = {"status": "healthy"}
    return registry


@pytest.fixture
def mock_message_broker():
    """Mock message broker for testing messaging."""
    broker = MagicMock()
    broker.publish.return_value = True
    broker.subscribe.return_value = MagicMock()
    broker.consume.return_value = iter([{"event": "test", "data": {}}])
    return broker


@pytest.fixture
def mock_build_env(tmp_path):
    """Mock build environment with necessary files."""
    # Create mock module directories
    for module in ["backend", "frontend", "market"]:
        module_dir = tmp_path / module
        module_dir.mkdir()
        (module_dir / "README.md").write_text(f"# {module}")
    
    # Create diagnostic dir
    diag_dir = tmp_path / "diagnostic"
    diag_dir.mkdir()
    
    return tmp_path
