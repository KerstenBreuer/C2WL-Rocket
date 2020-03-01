import logging

logger = logging.getLogger("cwltool")
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
