# Bilibili API Server

基于 FastAPI 的 B站评论管理 API 服务，集成 Dify Workflow 自动化功能

## 🌟 功能特性

### 核心功能
- 🔍 **获取未回复评论** - 智能识别需要回复的评论
- 💬 **回复评论功能** - 支持批量回复评论管理
- 🤖 **Dify Workflow 集成** - 自动化工作流程执行
- ⏰ **定时调度器** - 支持定时执行Dify工作流
- 🏥 **健康检查** - 完整的服务状态监控

### 技术特性
- 🎯 **RESTful API 设计** - 标准化接口规范
- 📊 **完整的错误处理** - 统一的异常处理机制
- 📖 **自动生成API文档** - Swagger/OpenAPI 支持
- 🔧 **模块化架构** - 清晰的代码组织结构
- 📝 **详细日志记录** - 完整的操作追踪

## 🏗️ 项目结构

```
bilibili-api-server/
├── app/                    # 应用核心模块
│   ├── api/               # API路由模块
│   │   ├── comments.py    # 评论管理接口
│   │   ├── dify.py        # Dify集成接口
│   │   └── health.py      # 健康检查接口
│   ├── bilibili/          # B站服务模块
│   │   └── service.py     # B站API业务逻辑
│   ├── dify/              # Dify集成模块
│   │   └── service.py     # Dify工作流服务
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据模型定义
│   └── utils.py           # 工具函数
├── docs/                  # 详细文档
├── main.py                # 应用入口文件
├── dify_config.py         # Dify专用配置
├── requirements.txt       # 依赖包列表
├── start_api.sh           # 前台启动脚本
├── start_api_daemon.sh    # 后台启动脚本
├── stop_api.sh            # 停止服务脚本
└── test_*.py              # 测试脚本
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd bilibili-api-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

#### B站凭据配置
编辑 `app/config.py` 文件，设置你的B站凭据：
```python
BILIBILI_SESSDATA = "你的sessdata"
BILIBILI_BILI_JCT = "你的bili_jct"
BILIBILI_MID = "你的用户ID"
```

#### Dify配置（可选）
编辑 `dify_config.py` 文件：
```python
DIFY_API_KEY = "你的Dify API Key"
DIFY_BASE_URL = "http://localhost/v1"  # 你的Dify服务地址
```

### 3. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
# 前台启动（开发模式）
./start_api.sh

# 后台启动（生产模式）
./start_api_daemon.sh

# 停止服务
./stop_api.sh
```

#### 方式二：直接命令启动

```bash
# 开发模式
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 方式三：Python脚本启动

```bash
# 测试模式
python main.py
```

## 📚 API 接口文档

### 基础接口

#### 服务信息
```http
GET /
```
返回API基本信息和版本

#### 健康检查
```http
GET /health
```
检查服务健康状态

### 评论管理接口

#### 获取未回复评论
```http
POST /api/comments/unreplied
```

**响应示例：**
```json
{
  "result": [
    {
      "rpid": 267138228592,
      "mid": "24566904",
      "oid": 114721512489989,
      "root": 0,
      "parent": 0,
      "content": "已三连，求大佬课件[呲牙]",
      "title": "视频标题",
      "uname": "用户名"
    }
  ],
  "count": 1
}
```

#### 回复评论
```http
POST /api/comments/reply
```

**请求参数：**
```json
{
  "oid": 114721512489989,
  "rpid": 267138228592,
  "message": "感谢您的评论！"
}
```

### Dify集成接口

#### 手动调用Dify工作流
```http
POST /api/dify/call
```

#### 启动定时调度器
```http
POST /api/dify/scheduler/start?interval_hours=1
```

#### 停止定时调度器
```http
POST /api/dify/scheduler/stop
```

#### 查看调度器状态
```http
GET /api/dify/scheduler/status
```

## 🔧 使用示例

### Python 客户端示例

```python
import requests

# 基础URL
BASE_URL = "http://localhost:8000"

# 1. 获取未回复评论
response = requests.post(f"{BASE_URL}/api/comments/unreplied")
unreplied = response.json()
print(f"未回复评论数量: {unreplied['count']}")

# 2. 回复评论
reply_data = {
    "oid": 114721512489989,
    "rpid": 267138228592,
    "message": "感谢您的评论！"
}
response = requests.post(f"{BASE_URL}/api/comments/reply", json=reply_data)
result = response.json()
print(f"回复结果: {result['message']}")

# 3. 手动调用Dify工作流
response = requests.post(f"{BASE_URL}/api/dify/call")
dify_result = response.json()
print(f"Dify调用结果: {dify_result['success']}")

# 4. 启动定时调度器（每2小时执行一次）
response = requests.post(f"{BASE_URL}/api/dify/scheduler/start?interval_hours=2")
scheduler_result = response.json()
print(f"调度器启动: {scheduler_result}")
```

### curl 命令示例

```bash
# 获取未回复评论
curl -X POST http://localhost:8000/api/comments/unreplied

# 回复评论
curl -X POST http://localhost:8000/api/comments/reply \
  -H "Content-Type: application/json" \
  -d '{"oid": 114721512489989, "rpid": 267138228592, "message": "感谢评论！"}'

# 调用Dify工作流
curl -X POST http://localhost:8000/api/dify/call

# 启动定时调度器
curl -X POST "http://localhost:8000/api/dify/scheduler/start?interval_hours=1"

# 查看调度器状态
curl -X GET http://localhost:8000/api/dify/scheduler/status
```

## 🧪 测试功能

### 运行测试脚本

```bash
# 测试API功能
python test_api.py

# 测试Dify调度器
python test_dify_scheduler.py

# 使用main.py测试
python main.py
# 然后选择相应的测试选项
```

## 📊 服务监控

### 访问API文档
启动服务后，访问以下地址：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 查看日志
```bash
# 查看应用日志（后台模式）
tail -f api_server.log

# 查看Dify调度器日志
tail -f dify_scheduler.log

# 实时监控日志
tail -f *.log
```

### 服务状态检查
```bash
# 检查端口占用
lsof -i :8000

# 检查进程状态
ps aux | grep uvicorn

# 测试服务响应
curl http://localhost:8000/health
```

## ⚙️ 配置说明

### 环境变量配置
创建 `.env` 文件进行个性化配置：

```env
# B站凭据
BILIBILI_SESSDATA=你的sessdata
BILIBILI_BILI_JCT=你的bili_jct
BILIBILI_MID=你的用户ID

# Dify配置
DIFY_API_KEY=你的Dify_API_Key
DIFY_BASE_URL=http://localhost/v1
SCHEDULER_INTERVAL_HOURS=1
AUTO_START_SCHEDULER=false

# 日志配置
LOG_LEVEL=INFO
```

### 服务配置
- **默认端口**: 8000
- **默认主机**: 0.0.0.0
- **日志文件**: `api_server.log`, `dify_scheduler.log`
- **PID文件**: `api_server.pid`

## 🔒 安全注意事项

1. **凭据安全**: 
   - 不要将B站凭据提交到版本控制系统
   - 使用环境变量或配置文件管理敏感信息
   - 定期更新API密钥

2. **网络安全**:
   - 生产环境建议使用HTTPS
   - 配置防火墙规则
   - 限制API访问频率

3. **数据安全**:
   - 定期备份重要数据
   - 监控异常访问行为

## 📋 依赖包说明

- **FastAPI**: 现代高性能的Web框架
- **uvicorn**: ASGI服务器
- **pydantic**: 数据验证和设置管理
- **requests**: HTTP请求库
- **APScheduler**: 定时任务调度
- **httpx**: 异步HTTP客户端
- **python-dotenv**: 环境变量管理
- **curl_cffi**: HTTP请求库

## 🐛 故障排查

### 常见问题

1. **端口被占用**
   ```bash
   # 查找占用端口的进程
   lsof -i :8000
   # 杀死进程
   kill -9 <PID>
   ```

2. **虚拟环境问题**
   ```bash
   # 重新创建虚拟环境
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **依赖包问题**
   ```bash
   # 更新pip
   pip install --upgrade pip
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

4. **Dify连接问题**
   - 检查Dify服务是否正常运行
   - 验证API Key是否正确
   - 确认网络连接正常

## 📖 详细文档

项目包含完整的文档系统，详细信息请参考：

- **[API快速参考](docs/api-quick-reference.md)** - 快速上手指南
- **[完整接口文档](docs/api-documentation.md)** - 详细的API文档
- **[产品需求文档](docs/prd.md)** - 产品功能规划
- **[Dify集成指南](dify_integration_guide.md)** - Dify功能使用说明
- **[重构总结](重构总结.md)** - 项目重构说明

## 🎯 版本信息

- **当前版本**: 1.0.0
- **最后更新**: 2025-01-31
- **Python版本**: 3.8+
- **FastAPI版本**: 0.104.1+

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 📞 支持与反馈

- 🐛 **Bug报告**: 请在GitHub Issues中提交
- 💡 **功能建议**: 欢迎提出改进建议
- 📖 **文档问题**: 如有文档不清楚的地方，请及时反馈
- 💬 **技术讨论**: 欢迎在Discussions中交流

---

**🎉 感谢使用 Bilibili API Server！** 