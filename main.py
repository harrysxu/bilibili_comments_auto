"""
主应用文件 - FastAPI应用的入口点
"""
import json
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import API_TITLE, API_DESCRIPTION, API_VERSION
from app.utils import setup_logging
from app.api.comments import router as comments_router
from app.api.health import router as health_router
from app.api.dify import router as dify_router

# 设置日志
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动事件
    logger.info("Bilibili API Server 正在启动...")
    
    # 启动Dify定时调度器
    try:
        from app.dify.service import start_scheduler
        success = start_scheduler()
        if success:
            logger.info("✅ Dify定时调度器启动成功")
        else:
            logger.warning("⚠️ Dify定时调度器启动失败")
    except Exception as e:
        logger.error("启动Dify定时调度器时发生错误: %s", str(e))
    
    logger.info("应用已成功启动！")
    
    yield
    
    # 关闭事件
    logger.info("正在关闭应用...")
    
    # 清理Dify调度器
    try:
        from app.dify.service import cleanup_scheduler
        cleanup_scheduler()
    except Exception as e:
        logger.warning("清理Dify调度器时发生错误: %s", str(e))
    
    logger.info("应用已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan
)

# 注册路由
app.include_router(health_router, tags=["基础功能"])
app.include_router(comments_router, prefix="/api/comments", tags=["评论管理"])
app.include_router(dify_router, prefix="/api/dify", tags=["Dify集成"])


# 保留原有的测试函数（可选）
if __name__ == "__main__":
    import asyncio
    
    async def test_api():
        """
        测试API功能
        """
        from app.bilibili.service import get_unreplied_comments
        
        try:
            print("正在测试获取未回复评论...")
            result = await get_unreplied_comments()
            print(f"获取到 {result.count} 条未回复评论")
            
            for comment in result.result[:3]:  # 只显示前3条
                print(f"评论ID: {comment.rpid}, 用户: {comment.uname}, 内容: {comment.content[:50]}...")
                
        except Exception as e:
            print(f"测试失败: {e}")

    async def test_dify():
        """
        测试Dify集成
        """
        from app.dify.service import manual_call_dify
        
        try:
            print("正在测试Dify API调用...")
            result = await manual_call_dify()
            
            if result.success:
                print("Dify调用成功!")
                print(f"调用时间: {result.call_time}")
                if result.response_data:
                    print(f"响应数据: {json.dumps(result.response_data, indent=2, ensure_ascii=False)}")
            else:
                print(f"Dify调用失败: {result.message}")
                
        except Exception as e:
            print(f"测试失败: {e}")

    # 运行测试
    print("选择测试功能:")
    print("1. 测试Bilibili API")
    print("2. 测试Dify API")
    choice = input("请输入选择 (1或2): ")
    
    if choice == "1":
        asyncio.run(test_api())
    elif choice == "2":
        asyncio.run(test_dify())
    else:
        print("无效选择") 