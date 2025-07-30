#!/usr/bin/env python3
"""
测试修复后的 chat_id 传递机制
"""

import requests
import json
import time

def test_with_real_webui():
    """使用真实的 WebUI 进行测试"""
    
    # 这些需要根据实际情况修改
    base_url = "http://localhost:8080"  # WebUI 的实际地址
    token = "your_actual_token_here"    # 实际的认证令牌
    model = "gpt-3.5-turbo"             # 实际可用的模型
    
    chat_id = f"test_chat_{int(time.time())}"
    
    # 第一轮对话
    payload1 = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello, I'm starting a new conversation. Please remember my name is Alice."}
        ],
        "stream": False,
        "metadata": {
            "chat_id": chat_id
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "X-OpenWebUI-Chat-Id": chat_id
    }
    
    print(f"🚀 开始测试 chat_id: {chat_id}")
    print(f"📡 发送第一轮对话...")
    
    try:
        response1 = requests.post(
            f"{base_url}/openai/chat/completions",
            json=payload1,
            headers=headers,
            timeout=30
        )
        
        print(f"第一轮响应状态: {response1.status_code}")
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"第一轮响应: {result1.get('choices', [{}])[0].get('message', {}).get('content', 'No content')[:100]}...")
            
            # 等待一下
            time.sleep(2)
            
            # 第二轮对话 - 测试上下文连续性
            payload2 = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "What is my name? (This should test conversation continuity)"}
                ],
                "stream": False,
                "metadata": {
                    "chat_id": chat_id
                }
            }
            
            print(f"📡 发送第二轮对话...")
            response2 = requests.post(
                f"{base_url}/openai/chat/completions",
                json=payload2,
                headers=headers,
                timeout=30
            )
            
            print(f"第二轮响应状态: {response2.status_code}")
            if response2.status_code == 200:
                result2 = response2.json()
                content2 = result2.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
                print(f"第二轮响应: {content2}")
                
                # 检查是否记住了名字
                if "Alice" in content2 or "alice" in content2.lower():
                    print("✅ 成功！AI 记住了之前的对话内容")
                else:
                    print("❌ 失败！AI 没有记住之前的对话内容")
                    print("这可能意味着 chat_id 没有正确传递，或者后端没有正确处理")
            else:
                print(f"第二轮对话失败: {response2.text}")
        else:
            print(f"第一轮对话失败: {response1.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        print("请确保:")
        print("1. WebUI 服务正在运行")
        print("2. 端口和地址正确")
        print("3. token 有效")
        print("4. 模型配置正确")

def test_without_chat_id():
    """测试不带 chat_id 的情况"""
    
    base_url = "http://localhost:8080"
    token = "your_actual_token_here"
    model = "gpt-3.5-turbo"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello, this is a test without chat_id"}
        ],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print(f"📡 测试不带 chat_id 的请求...")
    
    try:
        response = requests.post(
            f"{base_url}/openai/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"响应状态: {response.status_code}")
        if response.status_code == 200:
            print("✅ 不带 chat_id 的请求也能正常工作")
        else:
            print(f"❌ 请求失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    print("=== Chat ID 传递机制集成测试 ===")
    print("请先修改脚本中的配置参数!")
    print()
    
    # 测试带 chat_id 的连续对话
    test_with_real_webui()
    
    print("\n" + "="*50 + "\n")
    
    # 测试不带 chat_id 的单次对话
    test_without_chat_id()
    
    print("\n=== 测试完成 ===")
    print("查看后端日志以确认 chat_id 是否被正确接收")
