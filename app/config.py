"""
配置文件 - 包含所有配置常量和环境变量
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# B站凭据配置
BILIBILI_SESSDATA = {BILIBILI_SESSDATA}
BILIBILI_BILI_JCT = {BILIBILI_BILI_JCT}
BILIBILI_MID = {BILIBILI_MID}

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "dify_scheduler.log"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# API配置
API_TITLE = "Bilibili API Server"
API_DESCRIPTION = "B站评论管理API服务"
API_VERSION = "1.0.0" 