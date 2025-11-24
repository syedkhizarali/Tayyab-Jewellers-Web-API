import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jewellery_api")

@contextmanager
def log_exceptions(operation: str):
    try:
        yield
    except Exception as e:
        logger.error(f"{operation} failed: {str(e)}", exc_info=True)
        raise
