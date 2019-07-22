import logging.config

logging.config.fileConfig("./app/config/logger.ini")
logger = logging.getLogger("main")