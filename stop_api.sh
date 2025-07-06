#!/bin/bash

# API 停止脚本 - 重构后版本
# 停止 uvicorn 启动的 FastAPI 应用

# 配置参数
PORT=8000
APP_NAME="Bilibili API Server"
PID_FILE="api_server.pid"

echo "🛑 停止 $APP_NAME..."

# 方法1: 通过PID文件停止
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    echo "📝 从PID文件读取到进程ID: $PID"
    
    if kill -0 $PID 2>/dev/null; then
        echo "🔄 正在停止进程 $PID..."
        kill $PID
        sleep 2
        
        # 检查进程是否还在运行
        if kill -0 $PID 2>/dev/null; then
            echo "⚡ 强制停止进程..."
            kill -9 $PID
        fi
        
        echo "✅ 进程已停止"
        rm -f $PID_FILE
    else
        echo "⚠️  PID文件中的进程 $PID 不存在，清理PID文件"
        rm -f $PID_FILE
    fi
else
    echo "📄 未找到PID文件: $PID_FILE"
fi

# 方法2: 通过端口查找并停止进程
echo "📍 检查端口 $PORT 上的进程..."
PIDS=$(lsof -ti:$PORT)

if [ ! -z "$PIDS" ]; then
    echo "⚠️  发现端口 $PORT 上仍有进程: $PIDS"
    for PID in $PIDS; do
        echo "🔄 停止进程 $PID..."
        kill $PID
        sleep 1
        
        # 检查进程是否还在运行
        if kill -0 $PID 2>/dev/null; then
            echo "⚡ 强制停止进程 $PID..."
            kill -9 $PID
        fi
    done
    echo "✅ 所有进程已停止"
else
    echo "✅ 端口 $PORT 上没有运行的进程"
fi

# 方法3: 通过进程名查找uvicorn进程
echo "🔍 查找所有uvicorn进程..."
UVICORN_PIDS=$(ps aux | grep "[u]vicorn.*main:app" | awk '{print $2}')

if [ ! -z "$UVICORN_PIDS" ]; then
    echo "⚠️  发现uvicorn进程: $UVICORN_PIDS"
    for PID in $UVICORN_PIDS; do
        echo "🔄 停止uvicorn进程 $PID..."
        kill $PID
        sleep 1
        
        # 检查进程是否还在运行
        if kill -0 $PID 2>/dev/null; then
            echo "⚡ 强制停止进程 $PID..."
            kill -9 $PID
        fi
    done
    echo "✅ 所有uvicorn进程已停止"
else
    echo "✅ 没有找到运行中的uvicorn进程"
fi

# 清理日志文件（可选）
read -p "🗑️  是否删除日志文件 api_server.log? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f api_server.log
    echo "✅ 日志文件已删除"
fi

echo "�� $APP_NAME 已完全停止" 