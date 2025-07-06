"""
通用工具函数
"""
import logging
from app.config import LOG_LEVEL, LOG_FILE, LOG_FORMAT


def setup_logging():
    """
    配置日志系统
    """
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__) 