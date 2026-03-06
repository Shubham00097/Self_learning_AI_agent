import pytest
import logging
from pathlib import Path
from agent.logger import setup_logger

def test_setup_logger_creates_directory_and_writes(tmp_path):
    log_dir = tmp_path / "logs"
    assert not log_dir.exists()
    
    logger = setup_logger(log_dir, "DEBUG")
    
    assert log_dir.exists()
    assert (log_dir / "agent.log").exists()
    
    logger.debug("Test debug message")
    logger.info("Test info message")
    
    # Force flush
    for handler in logger.handlers:
        handler.flush()
        
    with open(log_dir / "agent.log", "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "Test debug message" in content
    assert "Test info message" in content
    
    # Clean up handlers for other tests
    logger.handlers.clear()

def test_setup_logger_permission_error(tmp_path, monkeypatch):
    def mock_mkdir(*args, **kwargs):
        raise PermissionError("Mock permission error")
        
    log_dir = tmp_path / "logs"
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    
    with pytest.raises(PermissionError, match="Cannot create log directory"):
        setup_logger(log_dir)
