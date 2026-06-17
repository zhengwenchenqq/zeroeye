"""
Tests for Python tools (AI reviewer, analyzer, etc).

Covers:
- AI code review functionality
- Legacy analysis
- Security audit patterns
- Health checks
"""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestAiReviewer:
    """Test AI code reviewer functionality."""
    
    def test_security_patterns_loaded(self):
        """Security patterns are initialized."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
        from ai_reviewer import SecurityAuditor
        
        auditor = SecurityAuditor()
        assert len(auditor.patterns) > 0
    
    def test_sql_injection_detection(self):
        """SQL injection patterns are detected."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
        from ai_reviewer import SecurityAuditor
        
        auditor = SecurityAuditor()
        code = 'cursor.execute("SELECT * FROM users WHERE id=" + user_id)'
        findings = auditor.audit(code, "test.py")
        # Should detect SQL injection
        assert any("SQL" in f.message or "injection" in f.message.lower() for f in findings)
    
    def test_hardcoded_key_detection(self):
        """Hardcoded API keys are detected."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
        from ai_reviewer import SecurityAuditor
        
        auditor = SecurityAuditor()
        code = 'api_key = "sk-1234567890abcdef1234567890abcdef"'
        findings = auditor.audit(code, "config.py")
        assert any("secret" in f.message.lower() or "key" in f.message.lower() for f in findings)
    
    def test_clean_code_no_findings(self):
        """Clean code produces no security findings."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
        from ai_reviewer import SecurityAuditor
        
        auditor = SecurityAuditor()
        code = 