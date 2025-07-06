#!/bin/bash

# API 后台启动脚本 - 重构后版本
# 使用 uvicorn 后台启动 FastAPI 应用

# 配置参数
PORT=8000
HOST="0.0.0.0"
APP_MODULE="main:app"
APP_NAME="Bilibili API Server"
LOG_FILE="api_server.log"
PID_FILE="api_server.pid"

echo "🚀 后台启动 $APP_NAME (重构版)..."
echo "📍 检查端口 $PORT 是否被占用..."

# 检查端口是否被占用
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
    echo "⚠️  端口 $PORT 已被进程 $PID 占用"
    echo "🔄 正在终止进程..."
    
    # 尝试优雅关闭
    kill $PID
    sleep 2
    
    # 检查进程是否还在运行
    if kill -0 $PID 2>/dev/null; then
        echo "⚡ 强制终止进程..."
        kill -9 $PID
        sleep 1
    fi
    
    echo "✅ 进程已终止"
else
    echo "✅ 端口 $PORT 空闲"
fi

# 再次检查端口是否真的空闲了
REMAINING_PID=$(lsof -ti:$PORT)
if [ ! -z "$REMAINING_PID" ]; then
    echo "❌ 无法释放端口 $PORT，退出启动"
    exit 1
fi

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  未检测到虚拟环境"
    if [ -d "venv" ]; then
        echo "🔄 激活虚拟环境..."
        source venv/bin/activate
    else
        echo "❌ 找不到虚拟环境，请先运行: python -m venv venv && source venv/bin/activate"
        exit 1
    fi
else
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
fi

# 检查main.py是否存在
if [ ! -f "main.py" ]; then
    echo "❌ 找不到 main.py 文件"
    exit 1
fi

# 检查uvicorn是否安装
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn 未安装，正在安装..."
    pip install uvicorn[standard]
fi

echo "🔥 后台启动 FastAPI 服务器..."

# 后台启动 FastAPI 应用
nohup uvicorn $APP_MODULE --host $HOST --port $PORT > $LOG_FILE 2>&1 &
SERVER_PID=$!

# 保存PID到文件
echo $SERVER_PID > $PID_FILE

# 等待一秒，检查服务是否成功启动
sleep 2

if kill -0 $SERVER_PID 2>/dev/null; then
    echo "✅ 服务启动成功！"
    echo "🆔 进程ID: $SERVER_PID"
    echo "📝 日志文件: $LOG_FILE"
    echo "🔄 PID文件: $PID_FILE"
    echo "🛑 停止服务: ./stop_api.sh"
    echo "🌐 API 地址: http://localhost:$PORT"
    echo "📚 API 文档: http://localhost:$PORT/docs"
    echo "🔧 交互式文档: http://localhost:$PORT/redoc"
    echo "📊 查看日志: tail -f $LOG_FILE"
    echo "📊 实时日志: tail -f $LOG_FILE"
else
    echo "❌ 服务启动失败，请检查日志文件: $LOG_FILE"
    exit 1
fi 