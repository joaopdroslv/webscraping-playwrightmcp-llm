import logging

log_format = (
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | "
    "%(funcName)s | %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S"))

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False
