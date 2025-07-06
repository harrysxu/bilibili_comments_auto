"""
Dify Workflow 服务模块
提供workflow调用和定时调度功能
"""
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from dify_config import (
    DIFY_API_KEY, 
    DIFY_WORKFLOW_ENDPOINT, 
    REQUEST_TIMEOUT,
    DEFAULT_INTERVAL_HOURS
)
from app.utils import setup_logging
from app.models import DifyCallResponse

# 设置日志
logger = setup_logging()

# 全局调度器实例
scheduler: Optional[AsyncIOScheduler] = None
scheduler_running = False


async def call_dify_workflow(inputs: Dict[str, Any] = None) -> DifyCallResponse:
    """
    调用Dify workflow
    
    Args:
        inputs: workflow输入参数，默认为空字典
        
    Returns:
        DifyCallResponse: 调用结果
    """
    if inputs is None:
        inputs = {}
    
    call_time = datetime.now()
    
    try:
        logger.info("开始调用Dify workflow: %s", DIFY_WORKFLOW_ENDPOINT)
        
        # 准备请求数据
        request_data = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": "bilibili-api-server"
        }
        
        logger.info("请求参数: %s", json.dumps(request_data, ensure_ascii=False))
        
        # 发送请求
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                DIFY_WORKFLOW_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=request_data
            )
            
            logger.info("Dify API响应状态码: %d", response.status_code)
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info("Dify调用成功，响应数据: %s", 
                          json.dumps(response_data, indent=2, ensure_ascii=False))
                
                return DifyCallResponse(
                    success=True,
                    message="Workflow执行成功",
                    response_data=response_data,
                    call_time=call_time
                )
            else:
                error_msg = f"Dify API调用失败，状态码: {response.status_code}"
                logger.error(error_msg)
                logger.error("响应内容: %s", response.text)
                
                return DifyCallResponse(
                    success=False,
                    message=error_msg,
                    response_data={"status_code": response.status_code, "content": response.text},
                    call_time=call_time
                )
                
    except httpx.TimeoutException:
        error_msg = f"Dify API调用超时（超过{REQUEST_TIMEOUT}秒）"
        logger.error(error_msg)
        return DifyCallResponse(
            success=False,
            message=error_msg,
            call_time=call_time
        )
        
    except Exception as e:
        error_msg = f"Dify API调用发生异常: {str(e)}"
        logger.error(error_msg)
        return DifyCallResponse(
            success=False,
            message=error_msg,
            call_time=call_time
        )


async def scheduled_dify_call():
    """定时执行的Dify workflow调用"""
    logger.info("🚀 开始执行定时Dify workflow调用")
    
    try:
        result = await call_dify_workflow()
        
        if result.success:
            logger.info("✅ 定时Dify workflow调用成功")
            # 打印执行结果
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Dify Workflow执行成功")
            if result.response_data:
                print(f"响应数据: {json.dumps(result.response_data, indent=2, ensure_ascii=False)}")
        else:
            logger.error("❌ 定时Dify workflow调用失败: %s", result.message)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Dify Workflow执行失败: {result.message}")
            
    except Exception as e:
        logger.error("定时调用Dify workflow时发生异常: %s", str(e))
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 定时调用异常: {str(e)}")


def start_scheduler(interval_hours: int = DEFAULT_INTERVAL_HOURS):
    """
    启动定时调度器
    
    Args:
        interval_hours: 调度间隔（小时）
    """
    global scheduler, scheduler_running
    
    if scheduler_running:
        logger.warning("调度器已经在运行中")
        return False
    
    try:
        scheduler = AsyncIOScheduler()
        
        # 添加定时任务
        scheduler.add_job(
            scheduled_dify_call,
            trigger=IntervalTrigger(hours=interval_hours),
            id="dify_workflow_scheduler",
            name=f"Dify Workflow定时执行 (每{interval_hours}小时)",
            replace_existing=True
        )
        
        # 启动调度器
        scheduler.start()
        scheduler_running = True
        
        logger.info("🎯 Dify workflow调度器已启动，每%d小时执行一次", interval_hours)
        print(f"✅ Dify调度器已启动，每{interval_hours}小时执行一次")
        
        # 立即执行一次
        asyncio.create_task(scheduled_dify_call())
        
        return True
        
    except Exception as e:
        logger.error("启动调度器失败: %s", str(e))
        scheduler_running = False
        return False


def stop_scheduler():
    """停止定时调度器"""
    global scheduler, scheduler_running
    
    if not scheduler_running or scheduler is None:
        logger.warning("调度器未运行")
        return False
    
    try:
        scheduler.shutdown()
        scheduler = None
        scheduler_running = False
        
        logger.info("🛑 Dify workflow调度器已停止")
        print("✅ Dify调度器已停止")
        return True
        
    except Exception as e:
        logger.error("停止调度器失败: %s", str(e))
        return False


def get_scheduler_status() -> Dict[str, Any]:
    """获取调度器状态"""
    global scheduler, scheduler_running
    
    if not scheduler_running or scheduler is None:
        return {
            "running": False,
            "message": "调度器未运行"
        }
    
    try:
        jobs = scheduler.get_jobs()
        if jobs:
            job = jobs[0]
            return {
                "running": True,
                "job_name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "message": "调度器正常运行"
            }
        else:
            return {
                "running": True,
                "message": "调度器运行中，但没有任务"
            }
            
    except Exception as e:
        logger.error("获取调度器状态失败: %s", str(e))
        return {
            "running": False,
            "message": f"获取状态失败: {str(e)}"
        }


async def manual_call_dify() -> DifyCallResponse:
    """手动调用Dify workflow（用于测试）"""
    logger.info("执行手动Dify workflow调用")
    return await call_dify_workflow()


# 应用关闭时的清理函数
def cleanup_scheduler():
    """清理调度器资源"""
    global scheduler, scheduler_running
    
    if scheduler_running and scheduler is not None:
        logger.info("✅ Dify调度器已停止")
        try:
            scheduler.shutdown()
        except:
            pass
        scheduler = None
        scheduler_running = False 