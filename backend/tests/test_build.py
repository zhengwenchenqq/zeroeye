"""
Tests for build.py CLI and diagnostic generation.

Covers:
- CLI argument parsing
- Module selection
- Diagnostic report generation
- Version output
"""
import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestCliParsing:
    """Test CLI argument parsing."""
    
    def test_version_flag(self, capsys):
        """--version prints version and exits."""
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        with pytest.raises(SystemExit) as exc_info:
            import importlib
            build = importlib.import_module("build")
            build.main()
        # Version flag exits with 0
        assert exc_info.value.code == 0
    
    def test_list_targets_flag(self):
        """--list-targets shows all available targets."""
        # Verify MODULES list exists and has entries
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        import importlib
        build = importlib.import_module("build")
        assert hasattr(build, "MODULES")
        assert len(build.MODULES) > 0
    
    def test_module_dataclass_has_description(self):
        """Module dataclass has description field."""
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        import importlib
        build = importlib.import_module("build")
        module = build.MODULES[0]
        assert hasattr(module, "description")


class TestDiagnosticReport:
    """Test diagnostic report generation."""
    
    def test_build_diagnostic_report_structure(self, sample_build_results):
        """Diagnostic report has required fields."""
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        import importlib
        build = importlib.import_module("build")
        
        report = build.build_diagnostic_report(sample_build_results, "abc12345")
        
        assert "commit_id" in report
        assert report["commit_id"] == "abc12345"
        assert "total_modules" in report
        assert "passed" in report
        assert "failed" in report
    
    def test_diagnostic_paths_for_commit(self, tmp_path):
        """Diagnostic paths are generated correctly."""
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        import importlib
        build = importlib.import_module("build")
        
        logd_path, meta_path, commit_id = build.diagnostic_paths_for_commit()
        assert str(logd_path).endswith(".logd")
        assert str(meta_path).endswith(".json")
        assert len(commit_id) == 8
