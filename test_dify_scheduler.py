#!/usr/bin/env python3
"""
Dify调度器测试脚本
"""
import asyncio
import time
from datetime import datetime

from app.dify.service import start_scheduler, stop_scheduler, get_scheduler_status, manual_call_dify


async def test_dify_scheduler():
    """测试Dify调度器功能"""
    print("🧪 开始测试Dify调度器功能...")
    
    # 1. 测试手动调用
    print("\n1️⃣ 测试手动调用Dify workflow...")
    result = await manual_call_dify()
    print(f"   ✅ 手动调用结果: {'成功' if result.success else '失败'}")
    if result.response_data:
        print(f"   📊 响应数据: {result.response_data.get('data', {}).get('outputs', {})}")
    
    # 2. 测试启动调度器（短间隔用于测试）
    print("\n2️⃣ 测试启动调度器（每5分钟执行一次，用于测试）...")
    success = start_scheduler(interval_hours=1/12)  # 5分钟 = 1/12小时
    print(f"   ✅ 调度器启动: {'成功' if success else '失败'}")
    
    # 3. 检查调度器状态
    print("\n3️⃣ 检查调度器状态...")
    status = get_scheduler_status()
    print(f"   📊 调度器状态: {status}")
    
    # 4. 等待一段时间观察调度器执行
    print("\n4️⃣ 等待10秒观察调度器执行...")
    await asyncio.sleep(10)
    
    # 5. 停止调度器
    print("\n5️⃣ 停止调度器...")
    success = stop_scheduler()
    print(f"   ✅ 调度器停止: {'成功' if success else '失败'}")
    
    print("\n🎉 测试完成！")


if __name__ == "__main__":
    asyncio.run(test_dify_scheduler()) 