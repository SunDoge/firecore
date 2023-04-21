import logging
import numpy as np

logger = logging.getLogger(__name__)

try:
    import cv2
except ImportError:
    logger.exception("you should install opencv")


def cv2_loader(filename: str, flags: int = cv2.IMREAD_COLOR) -> np.ndarray:
    """
    Return RGB image as np.ndarray
    """
    img = cv2.imread(filename, flags=flags)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def cv2_worker_init_fn(worker_id: int):
    cv2.setNumThreads(0)
    logger.info("cv2 get num threads: %d", cv2.getNumThreads())
