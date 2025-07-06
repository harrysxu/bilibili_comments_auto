"""
健康检查和基础API路由
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": "欢迎使用 Bilibili API Server",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@router.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {
        "status": "healthy",
        "message": "服务运行正常"
    } 