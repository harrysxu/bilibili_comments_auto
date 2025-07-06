#!/usr/bin/env python3
"""
Bilibili API 测试脚本
用于测试获取未回复评论和回复评论的 API 接口
"""

import requests
import json
from typing import Dict, Any

# API 基础地址
BASE_URL = "http://localhost:8000"


def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False


def test_get_unreplied_comments():
    """测试获取未回复评论接口"""
    print("\n🔍 测试获取未回复评论接口...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/comments/unreplied"
        )
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"未回复评论数量: {data['count']}")
            
            if data['result']:
                print("前3条未回复评论:")
                for i, comment in enumerate(data['result'][:3], 1):
                    print(f"  {i}. 用户: {comment['uname']}")
                    print(f"     内容: {comment['content'][:50]}...")
                    print(f"     评论ID: {comment['rpid']}")
                    print(f"     作品ID: {comment['oid']}")
            else:
                print("✅ 当前没有未回复的评论")
            
            return data['result']
        else:
            print(f"❌ 请求失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 获取未回复评论失败: {e}")
        return None


def test_reply_comment(oid: int, rpid: int, root: int, message: str = "感谢您的评论！"):
    """测试回复评论接口"""
    print(f"\n🔍 测试回复评论接口...")
    try:
        reply_data = {
            "oid": oid,
            "rpid": rpid,
            "message": message,
            "root": root
        }
        
        response = requests.post(
            f"{BASE_URL}/api/comments/reply",
            json=reply_data
        )
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 回复成功!")
            print(f"回复ID: {data.get('rpid')}")
            print(f"消息: {data['message']}")
            return True
        else:
            print(f"❌ 回复失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 回复评论失败: {e}")
        return False


def test_api_documentation():
    """测试 API 文档接口"""
    print("\n🔍 测试 API 文档接口...")
    try:
        # 测试根路径
        response = requests.get(f"{BASE_URL}/")
        print(f"根路径状态码: {response.status_code}")
        if response.status_code == 200:
            print("API 信息:", response.json())
        
        # 测试 Swagger 文档
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Swagger 文档状态码: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ 测试文档接口失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试 Bilibili API Server")
    print("=" * 50)
    
    # 检查凭据是否已配置
    # if TEST_CREDENTIALS["sessdata"] == "your_sessdata_here":
    #     print("⚠️  请先在 test_api.py 中配置正确的 B站 凭据:")
    #     print("   - sessdata")
    #     print("   - bili_jct") 
    #     print("   - mid")
    #     print("\n你可以从浏览器的开发者工具中获取这些 cookie 值")
    #     return
    
    # 1. 健康检查
    if not test_health_check():
        print("❌ 服务未启动，请先运行: python main.py")
        return
    
    # 2. 测试 API 文档
    test_api_documentation()
    
    # 3. 获取未回复评论
    unreplied_comments = test_get_unreplied_comments()
    
    # 4. 如果有未回复评论，可以测试回复功能（需要用户确认）
    if unreplied_comments:
        print(f"\n发现 {len(unreplied_comments)} 条未回复评论")
        
        # 这里只是演示，实际使用时需要谨慎
        user_input = input("是否要测试回复第一条评论？(y/N): ")
        if user_input.lower() == 'y':
            first_comment = unreplied_comments[0]
            test_reply_comment(
                oid=first_comment['oid'],
                rpid=first_comment['rpid'],
                root=first_comment['root'],
                message="这是一条测试回复，感谢您的评论！"
            )
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    main() 