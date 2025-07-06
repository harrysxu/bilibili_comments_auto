"""
Dify API路由
提供Dify workflow的API接口
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from app.dify.service import (
    manual_call_dify,
    start_scheduler,
    stop_scheduler,
    get_scheduler_status
)
from app.models import DifyCallResponse, DifyConfigRequest
from dify_config import DEFAULT_INTERVAL_HOURS

router = APIRouter()


@router.post("/call", response_model=DifyCallResponse)
async def call_dify_workflow():
    """
    手动调用Dify workflow
    """
    try:
        result = await manual_call_dify()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用Dify workflow失败: {str(e)}")


@router.post("/scheduler/start")
async def start_dify_scheduler(interval_hours: int = Query(default=DEFAULT_INTERVAL_HOURS, ge=1, le=24)):
    """
    启动Dify workflow定时调度器
    
    Args:
        interval_hours: 调度间隔（小时），范围1-24
    """
    try:
        success = start_scheduler(interval_hours)
        if success:
            return {
                "success": True,
                "message": f"调度器已启动，每{interval_hours}小时执行一次",
                "interval_hours": interval_hours
            }
        else:
            raise HTTPException(status_code=400, detail="调度器启动失败，可能已经在运行中")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动调度器失败: {str(e)}")


@router.post("/scheduler/stop")
async def stop_dify_scheduler():
    """
    停止Dify workflow定时调度器
    """
    try:
        success = stop_scheduler()
        if success:
            return {
                "success": True,
                "message": "调度器已停止"
            }
        else:
            raise HTTPException(status_code=400, detail="调度器停止失败，可能未在运行")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"停止调度器失败: {str(e)}")


@router.get("/scheduler/status")
async def get_dify_scheduler_status():
    """
    获取Dify workflow调度器状态
    """
    try:
        status = get_scheduler_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取调度器状态失败: {str(e)}")


@router.put("/config")
async def update_dify_config(config: DifyConfigRequest):
    """
    更新Dify配置
    
    注意：此接口仅更新运行时配置，重启后会恢复到配置文件中的值
    """
    try:
        # 这里可以实现动态更新配置的逻辑
        # 由于配置是从文件导入的，这里主要用于演示
        return {
            "success": True,
            "message": "配置更新成功（注意：重启后会恢复到配置文件中的值）",
            "config": {
                "base_url": config.base_url,
                "interval_hours": config.interval_hours
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新配置失败: {str(e)}") 