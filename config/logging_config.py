# config/logging_config.py
import logging.config
import os

# safetynet/config/logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir="logs", log_file="app.log", level=logging.INFO):
    """
    设置全局日志格式和处理器
    """
    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    # 创建根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 防止重复添加 handler（重要！）
    if not root_logger.handlers:
        # 控制台输出（只显示 INFO 及以上）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        # 文件输出（记录所有级别，带轮转）
        file_handler = RotatingFileHandler(
            log_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s() | %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # 添加处理器
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

    return root_logger

# LOGGING_CONFIG = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "standard": {
#             "format": "%(asctime)s | [%(levelname)s] | %(name)s | %(funcName)s() | [%(filename)s:%(lineno)d]: %(message)s"
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "INFO",
#             "formatter": "standard",
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "level": "DEBUG",
#             "formatter": "standard",
#             "class": "logging.FileHandler",
#             "filename": "app.log",
#             "encoding": "utf-8",
#         },
#     },
#     "loggers": {
#         "": {  # root logger
#             "handlers": ["console", "file"],
#             "level": "DEBUG",
#             "propagate": False
#         }
#     }
# }

# def setup_logging():
#     logging.config.dictConfig(LOGGING_CONFIG)