"""
Storage utilities for travel-planner
提供統一的檔案存取介面
"""

import json
from pathlib import Path
from typing import Any, Optional


class Storage:
    """簡化的檔案儲存類"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
    
    def _get_path(self, filename: str) -> Path:
        return self.data_dir / filename
    
    def load(self, filename: str, default: Any = None) -> Any:
        """載入 JSON 檔案"""
        path = self._get_path(filename)
        if not path.exists():
            return default if default is not None else {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default if default is not None else {}
    
    def save(self, filename: str, data: Any) -> None:
        """儲存 JSON 檔案"""
        path = self._get_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def append(self, filename: str, item: Any, key: Optional[str] = None) -> None:
        """附加項目到列表或字典"""
        data = self.load(filename)
        if key:
            if key not in data:
                data[key] = []
            data[key].append(item)
        else:
            if not isinstance(data, list):
                data = []
            data.append(item)
        self.save(filename, data)


# 全域 storage 實例
storage = Storage()