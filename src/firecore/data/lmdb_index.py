import lmdb
from typing import Optional
from pathlib import Path
import struct


class LmdbIndex:
    def __init__(
        self, path: str, map_size: int = 1024 * 1024 * 1024, max_readers: int = 128
    ):  # 默认1GB
        """初始化LMDB索引存储

        Args:
            path: LMDB数据库路径
            map_size: 初始映射大小(字节)
        """
        self._path = Path(path)
        self._path.mkdir(parents=True, exist_ok=True)
        self._env = lmdb.Environment(
            str(self._path),
            map_size=map_size,
            readahead=False,
            map_async=True,
            max_readers=max_readers,
            max_dbs=2,
        )

    @staticmethod
    def _get_key(key: int) -> bytes:
        return struct.pack(">Q", key)

    def put(self, key: int, value: bytes) -> None:
        """存储键值对

        Args:
            key: 整数键
            value: 字节串值
        """
        key_bytes = self._get_key(key)
        while True:
            try:
                with self._env.begin(write=True) as txn:
                    txn.put(key_bytes, value)
                break
            except lmdb.MapFullError:
                # 空间不足时将map_size翻倍
                current_size = self._env.info()["map_size"]
                new_size = current_size * 2
                self._env.set_mapsize(new_size)

    def get(self, key: int) -> Optional[bytes]:
        """获取键对应的值

        Args:
            key: 整数键
        Returns:
            对应的值，如果不存在则返回None
        """
        key_bytes = self._get_key(key)
        with self._env.begin() as txn:
            value = txn.get(key_bytes)
            return value

    def delete(self, key: int) -> bool:
        """删除键值对

        Args:
            key: 整数键
        Returns:
            是否成功删除
        """

        key_bytes = self._get_key(key)
        with self._env.begin(write=True) as txn:
            return txn.delete(key_bytes)

    def __del__(self):
        """析构时关闭数据库"""
        if hasattr(self, "env"):
            self._env.close()

    def __len__(self):
        """返回数据库中键值对的数量"""
        with self._env.begin() as txn:
            return txn.stat()["entries"]


if __name__ == "__main__":
    index = LmdbIndex("/tmp/test.lmdb")
    index.put(1, b"hello")
    index.put(2, b"world")
    print(index.get(1))
    print(index.get(2))
    print(len(index))
