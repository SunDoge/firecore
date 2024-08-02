from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from .jsonnet import eval_files


class Config(BaseModel):
    shared: Dict[str, Any]
    train: Optional[Dict[str, Any]] = None
    val: Optional[Dict[str, Any]] = None
    test: Optional[Dict[str, Any]] = None

    @classmethod
    def from_files(cls, files: List[str]):
        json_str = eval_files(files)
        return cls.model_validate_json(json_str)
