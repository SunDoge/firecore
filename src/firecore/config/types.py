from pydantic import BaseModel
from typing import Dict, Any, Optional, List, NamedTuple
from .jsonnet import eval_files
from .object_pool import ObjectPool


class ConfigObjectPools(NamedTuple):
    shared: ObjectPool
    train: ObjectPool
    val: ObjectPool
    test: ObjectPool


class Config(BaseModel):
    shared: Dict[str, Any]
    train: Optional[Dict[str, Any]] = None
    val: Optional[Dict[str, Any]] = None
    test: Optional[Dict[str, Any]] = None

    @classmethod
    def from_files(cls, files: List[str]):
        json_str = eval_files(files)
        return cls.model_validate_json(json_str)

    def build_object_pools(self, **kwargs):
        shared_object_pool = ObjectPool(self.shared, parent=None, **kwargs)

        return ConfigObjectPools(
            shared_object_pool,
            ObjectPool(
                {} if self.train is None else self.train,
                parent=shared_object_pool,
            ),
            ObjectPool(
                {} if self.val is None else self.val,
                parent=shared_object_pool,
            ),
            ObjectPool(
                {} if self.test is None else self.test,
                parent=shared_object_pool,
            ),
        )
