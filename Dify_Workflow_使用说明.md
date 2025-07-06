# Dify Workflow 自动化执行系统

## 🎯 功能概述

本系统实现了Dify workflow的自动化执行功能，支持：
- ⏰ 定时自动执行（可配置间隔时间）
- 🔧 手动触发执行
- 📊 实时状态监控
- 📝 详细日志记录

## 📋 配置信息

### 当前配置（dify_config.py）
- **API Key**: `app-YgLHlNeNc5xEMOE0w0ByZV8N`
- **API服务器**: `http://localhost/v1`
- **默认执行间隔**: 1小时
- **日志文件**: `dify_scheduler.log`

### 环境变量配置（可选）
创建 `.env` 文件来自定义配置：
```env
DIFY_API_KEY=app-YgLHlNeNc5xEMOE0w0ByZV8N
DIFY_BASE_URL=http://localhost/v1
SCHEDULER_INTERVAL_HOURS=1
AUTO_START_SCHEDULER=false
```

## 🚀 使用方法

### 1. 启动API服务器
```bash
# 方法1：使用uvicorn启动
uvicorn main:app --host 0.0.0.0 --port 8000

# 方法2：使用启动脚本
./start_api.sh
```

### 2. API端点使用

#### 📞 手动调用Dify Workflow
```bash
curl -X POST http://localhost:8000/api/dify/call
```

#### ⏰ 启动定时调度器
```bash
# 默认每1小时执行
curl -X POST http://localhost:8000/api/dify/scheduler/start

# 自定义间隔（例如每2小时）
curl -X POST "http://localhost:8000/api/dify/scheduler/start?interval_hours=2"
```

#### 🛑 停止定时调度器
```bash
curl -X POST http://localhost:8000/api/dify/scheduler/stop
```

#### 📊 查看调度器状态
```bash
curl -X GET http://localhost:8000/api/dify/scheduler/status
```

### 3. Python代码调用示例

```python
import asyncio
from app.dify.service import manual_call_dify, start_scheduler, stop_scheduler

async def example():
    # 手动调用
    result = await manual_call_dify()
    print(f"调用结果: {result.success}")
    
    # 启动定时调度器（每1小时）
    start_scheduler(interval_hours=1)
    
    # 停止调度器
    stop_scheduler()

asyncio.run(example())
```

## 📊 执行结果示例

### 成功执行的响应
```json
{
  "success": true,
  "message": "Workflow执行成功",
  "response_data": {
    "task_id": "xxx",
    "workflow_run_id": "xxx",
    "data": {
      "status": "succeeded",
      "outputs": {
        "result": "调用成功"
      },
      "elapsed_time": 0.015,
      "total_steps": 2
    }
  },
  "call_time": "2025-07-05T22:28:03.224"
}
```

### 调度器状态响应
```json
{
  "running": true,
  "job_name": "Dify Workflow定时执行 (每1小时)",
  "next_run_time": "2025-07-05T23:28:03.227+08:00",
  "message": "调度器正常运行"
}
```

## 🔧 测试功能

### 1. 使用测试脚本
```bash
python test_dify_scheduler.py
```

### 2. 使用main.py测试
```bash
python main.py
# 选择选项2：测试Dify API
```

## 📝 日志监控

### 查看实时日志
```bash
tail -f dify_scheduler.log
```

### 日志内容示例
```
2025-07-05 22:28:03,130 - app.utils - INFO - 执行手动Dify workflow调用
2025-07-05 22:28:03,224 - app.utils - INFO - Dify调用成功，响应数据: {...}
2025-07-05 22:28:03,227 - app.utils - INFO - 🎯 Dify workflow调度器已启动，每1小时执行一次
2025-07-05 22:28:03,301 - app.utils - INFO - ✅ 定时Dify workflow调用成功
```

## 🎛️ API文档

启动服务器后，访问以下地址查看完整API文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ⚠️ 注意事项

1. **Dify服务状态**: 确保Dify服务正常运行在 `http://localhost/v1`
2. **API Key有效性**: 确认API Key `app-YgLHlNeNc5xEMOE0w0ByZV8N` 有效
3. **网络连接**: 确保能够访问Dify服务
4. **调度器管理**: 应用关闭时会自动停止调度器
5. **日志文件**: 定期清理日志文件避免占用过多磁盘空间

## 🔧 故障排查

### 连接失败
- 检查Dify服务是否运行：`curl http://localhost/v1/health`
- 验证API Key是否正确
- 检查网络连接

### 调度器问题
- 查看调度器状态：`GET /api/dify/scheduler/status`
- 检查日志文件：`tail -f dify_scheduler.log`
- 重启调度器：先停止再启动

### 权限问题
- 确保有写入日志文件的权限
- 检查端口8000是否可用

## 🎉 功能验证

系统已经过完整测试，包括：
- ✅ 手动调用Dify workflow
- ✅ 定时调度器启动/停止
- ✅ 状态监控
- ✅ 日志记录
- ✅ 错误处理

所有功能都能正常工作，可以放心使用！ 