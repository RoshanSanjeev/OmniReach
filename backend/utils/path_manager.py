# backend/utils/path_manager.py
import os
from pathlib import Path

class PathManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.project_root = Path(__file__).parent.parent.parent  # Adjust based on your structure
            self._initialized = True

    def get_path(self, relative_path: str) -> str:
        """Convert relative path to absolute path"""
        absolute_path = (self.project_root / relative_path).resolve()
        return str(absolute_path)

    def verify_path(self, relative_path: str) -> bool:
        """Check if path exists with proper validation"""
        target = self.get_path(relative_path)
        return os.path.exists(target)

# Singleton instance
path_manager = PathManager()