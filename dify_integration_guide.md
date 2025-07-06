# Dify Workflow 定时调用集成指南

## 功能介绍

本应用已集成 Dify workflow 定时调用功能，可以每隔指定时间自动调用您在 Dify 中创建的 workflow。

## 配置说明

### 1. 基本配置

- **API Key**: `app-MGsxM687qxK8sDVZzkAex7Op` (已在代码中配置)
- **默认 Dify 地址**: `http://localhost/v1` (本地 Docker 部署)
- **默认调用间隔**: 1小时

### 2. 环境变量配置 (可选)

您可以通过创建 `.env` 文件来自定义配置：

```env
# Dify 服务配置
DIFY_BASE_URL=http://localhost:3000/v1

# 自动启动定时调度器 (true/false)  
AUTO_START_SCHEDULER=true

# 定时调度器间隔时间（小时）
SCHEDULER_INTERVAL_HOURS=2
```

### 3. Docker 部署 Dify 常见端口

根据您的 Dify Docker 配置，可能需要调整 `DIFY_BASE_URL`：
- 默认: `http://localhost/v1`
- 端口 3000: `http://localhost:3000/v1`
- 端口 80: `http://localhost:80/v1`

## API 端点

### 手动调用 Dify Workflow
```bash
curl -X POST http://localhost:8000/api/dify/call
```

### 启动定时调度器 (每1小时)
```bash
curl -X POST "http://localhost:8000/api/dify/scheduler/start?interval_hours=1"
```

### 停止定时调度器
```bash
curl -X POST http://localhost:8000/api/dify/scheduler/stop
```

### 查看调度器状态
```bash
curl http://localhost:8000/api/dify/scheduler/status
```

### 更新 Dify 配置
```bash
curl -X PUT http://localhost:8000/api/dify/config \
  -H "Content-Type: application/json" \
  -d '{
    "base_url": "http://localhost:3000/v1",
    "interval_hours": 2
  }'
```

## 使用步骤

### 1. 启动服务
```bash
python main.py
```

### 2. 测试 Dify 连接
```bash
python main.py test-dify
```

### 3. 启动定时调度器
通过 API 调用启动：
```bash
curl -X POST "http://localhost:8000/api/dify/scheduler/start?interval_hours=1"
```

或者设置环境变量自动启动：
```env
AUTO_START_SCHEDULER=true
```

### 4. 监控运行状态
访问 `http://localhost:8000/api/dify/scheduler/status` 查看：
- 是否正在运行
- 上次调用时间
- 调用成功/失败次数
- 下次运行时间

## 日志文件

系统会生成以下日志文件：
- `dify_scheduler.log`: 定时调用日志
- `server.log`: 服务器运行日志

## 故障排查

### 1. 连接失败
- 检查 Dify 服务是否正常运行
- 确认端口和地址配置正确
- 验证 API Key 是否有效

### 2. 调用失败
- 查看 `dify_scheduler.log` 日志
- 检查 workflow 是否正确配置
- 确认 workflow 不需要输入参数

### 3. 定时任务不运行
- 检查调度器状态: `GET /api/dify/scheduler/status`
- 查看错误日志
- 重启调度器: 先停止再启动

## 开发测试

### 测试 Dify API 连接
```bash
python main.py test-dify
```

### 测试定时调度器
```bash
python main.py scheduler
```

### 查看所有可用端点
访问 `http://localhost:8000/` 查看完整的 API 文档。 