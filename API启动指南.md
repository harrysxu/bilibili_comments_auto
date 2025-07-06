# 🚀 Bilibili API Server 启动指南

> 重构后的 FastAPI 应用启动方法

## 📋 前置准备

### 1. 激活虚拟环境
```bash
source venv/bin/activate
```

### 2. 安装依赖（如果还没安装）
```bash
pip install -r requirements.txt
```

### 3. 检查环境
```bash
which python
python --version
uvicorn --version
```

## 🎯 启动方法

### 方法一：命令行启动（推荐用于开发）

**基本启动：**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**自定义配置：**
```bash
# 指定端口
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# 仅本地访问
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# 生产模式（无自动重载）
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 方法二：使用启动脚本

**前台启动（开发模式）：**
```bash
./start_api.sh
```
- ✅ 自动检查端口占用
- ✅ 自动激活虚拟环境
- ✅ 启用热重载
- ✅ 前台运行，按 Ctrl+C 停止

**后台启动（生产模式）：**
```bash
./start_api_daemon.sh
```
- ✅ 后台运行
- ✅ 自动生成日志文件
- ✅ 保存进程ID
- ✅ 适合生产环境

**停止服务：**
```bash
./stop_api.sh
```
- ✅ 优雅停止服务
- ✅ 清理进程和文件
- ✅ 可选删除日志

### 方法三：Python 脚本启动

**直接运行（测试功能）：**
```bash
python main.py
```
这会启动测试模式，可以选择测试不同功能。

## 🌐 访问地址

启动成功后，可以通过以下地址访问：

- **API 根路径：** http://localhost:8000/
- **API 文档（Swagger）：** http://localhost:8000/docs  
- **交互式文档（ReDoc）：** http://localhost:8000/redoc
- **健康检查：** http://localhost:8000/health

## 📊 服务管理

### 检查服务状态
```bash
# 检查端口占用
lsof -i :8000

# 查看进程
ps aux | grep uvicorn

# 测试API响应
curl http://localhost:8000/health
```

### 查看日志
```bash
# 实时查看日志（后台启动时）
tail -f api_server.log

# 查看应用日志
tail -f dify_scheduler.log
```

### 停止服务
```bash
# 使用脚本停止（推荐）
./stop_api.sh

# 手动停止
kill $(lsof -ti:8000)

# 强制停止
kill -9 $(lsof -ti:8000)
```

## 🔧 常见问题

### 1. 端口被占用
```
ERROR: [Errno 48] Address already in use
```
**解决方法：**
- 使用启动脚本（自动处理）
- 手动停止占用进程：`kill $(lsof -ti:8000)`
- 使用其他端口：`uvicorn main:app --port 8080`

### 2. 模块导入错误
```
ModuleNotFoundError: No module named 'app'
```
**解决方法：**
- 确保在项目根目录
- 激活虚拟环境
- 安装依赖：`pip install -r requirements.txt`

### 3. uvicorn 未找到
```
command not found: uvicorn
```
**解决方法：**
```bash
pip install uvicorn[standard]
```

## 📈 性能调优

### 生产环境启动
```bash
# 使用多进程
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 指定worker类
uvicorn main:app --host 0.0.0.0 --port 8000 --worker-class uvicorn.workers.UvicornWorker

# 使用Gunicorn（需要安装）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Docker 部署
```dockerfile
# Dockerfile 示例
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🎉 快速开始

1. **激活环境并启动：**
   ```bash
   source venv/bin/activate
   ./start_api.sh
   ```

2. **访问文档：**
   打开浏览器访问 http://localhost:8000/docs

3. **测试API：**
   ```bash
   curl http://localhost:8000/health
   ```

4. **停止服务：**
   按 `Ctrl+C` 或运行 `./stop_api.sh`

---

> 💡 **提示：** 推荐使用 `start_api.sh` 进行开发，使用 `start_api_daemon.sh` 进行生产部署。 