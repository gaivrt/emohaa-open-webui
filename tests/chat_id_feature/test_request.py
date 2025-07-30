#!/usr/bin/env python3
"""
模拟前端发送聊天请求的脚本
"""

import requests
import json
import time

def test_chat_request_with_chat_id():
    """测试带有 chat_id 的请求"""
    
    # 模拟的请求数据
    payload = {
        "model": "gpt-3.5-turbo",  # 或者使用你配置的模型
        "messages": [
            {"role": "user", "content": "Hello, this is a test message"}
        ],
        "stream": False,
        "metadata": {
            "chat_id": "test_chat_123456",
            "user_id": "test_user",
            "timestamp": int(time.time())
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your_token_here",  # 需要替换为实际的 token
        "X-OpenWebUI-Chat-Id": "test_chat_123456"  # 添加自定义头部
    }
    
    try:
        response = requests.post(
            "http://localhost:8080/openai/chat/completions",  # 调整为实际的端口
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.text:
            print(f"Response Body: {response.text[:500]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def test_chat_request_without_chat_id():
    """测试不带 chat_id 的请求"""
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello, this is a test without chat_id"}
        ],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your_token_here"
    }
    
    try:
        response = requests.post(
            "http://localhost:8080/openai/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    print("Testing chat request with chat_id...")
    test_chat_request_with_chat_id()
    
    print("\n" + "="*50 + "\n")
    
    print("Testing chat request without chat_id...")
    test_chat_request_without_chat_id()
