import logging
import numpy as np

logger = logging.getLogger(__name__)

try:
    import cv2
except ImportError:
    logger.exception("you should install opencv")


def read_rgb(filename: str) -> np.ndarray:
    img = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def cv2_worker_init_fn(worker_id: int):
    cv2.setNumThreads(0)
    logger.info("worker_id: %d cv2 get num threads: %d",
                worker_id, cv2.getNumThreads())


def decode_from_buffer(buf: bytes, flags: int = cv2.IMREAD_COLOR) -> np.ndarray:
    img_buf = np.frombuffer(buf, dtype=np.uint8)
    img = cv2.imdecode(img_buf, flags)
    return img


def decode_rgb(buf: bytes) -> np.ndarray:
    img = decode_from_buffer(buf)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
