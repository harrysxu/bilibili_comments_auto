"""
Dify Workflow 配置文件
包含Dify API的所有配置信息
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Dify API 配置
DIFY_API_KEY = "app-owHsgSWYzHzMvKhFK6wFsAUd"
DIFY_BASE_URL = "http://localhost/v1"
DIFY_WORKFLOW_ENDPOINT = f"{DIFY_BASE_URL}/workflows/run"

# 定时调度配置
DEFAULT_INTERVAL_HOURS = 1  # 默认每小时执行一次
AUTO_START_SCHEDULER = False  # 是否自动启动调度器

# 从环境变量读取配置（可选）
DIFY_API_KEY = os.getenv("DIFY_API_KEY", DIFY_API_KEY)
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", DIFY_BASE_URL)
DEFAULT_INTERVAL_HOURS = int(os.getenv("SCHEDULER_INTERVAL_HOURS", DEFAULT_INTERVAL_HOURS))
AUTO_START_SCHEDULER = os.getenv("AUTO_START_SCHEDULER", "false").lower() == "true"

# 更新workflow端点
DIFY_WORKFLOW_ENDPOINT = f"{DIFY_BASE_URL}/workflows/run"

# 请求配置
REQUEST_TIMEOUT = 30  # 请求超时时间（秒）
MAX_RETRIES = 3  # 最大重试次数

# 日志配置
DIFY_LOG_FILE = "dify_scheduler.log" 