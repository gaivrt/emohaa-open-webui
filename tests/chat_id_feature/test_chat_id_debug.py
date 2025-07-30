#!/usr/bin/env python3
"""
测试脚本：检查 Open WebUI 的 chat_id 传递机制
"""

import json
import logging
import sys
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def add_debug_logging_to_openai_router():
    """在 OpenAI 路由中添加调试日志"""
    
    openai_py_path = Path("backend/open_webui/routers/openai.py")
    
    if not openai_py_path.exists():
        logger.error(f"找不到文件: {openai_py_path}")
        return False
    
    # 读取原始文件
    with open(openai_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经添加了调试日志
    if "# DEBUG: Chat ID investigation" in content:
        logger.info("调试日志已存在，跳过添加")
        return True
    
    # 在 generate_chat_completion 函数开始处添加调试日志
    debug_code = '''
    # DEBUG: Chat ID investigation
    log.debug(f"=== Chat Completion Request Debug ===")
    log.debug(f"Headers: {dict(request.headers)}")
    log.debug(f"Form data keys: {list(form_data.keys())}")
    log.debug(f"Metadata: {metadata}")
    log.debug(f"User: {user.name} (ID: {user.id})")
    
    # 检查是否有 chat_id 相关的信息
    chat_id_from_header = request.headers.get("X-OpenWebUI-Chat-Id")
    chat_id_from_metadata = metadata.get("chat_id") if metadata else None
    
    log.debug(f"Chat ID from header: {chat_id_from_header}")
    log.debug(f"Chat ID from metadata: {chat_id_from_metadata}")
    log.debug(f"=====================================")
'''
    
    # 找到插入位置（在 metadata 提取之后）
    insert_position = content.find("model_id = form_data.get(\"model\")")
    
    if insert_position == -1:
        logger.error("找不到插入位置")
        return False
    
    # 插入调试代码
    new_content = content[:insert_position] + debug_code + "\n    " + content[insert_position:]
    
    # 写回文件
    with open(openai_py_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    logger.info("成功添加调试日志到 OpenAI 路由")
    return True

def create_test_request_script():
    """创建测试请求脚本"""
    
    test_script = '''#!/usr/bin/env python3
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
    
    print("\\n" + "="*50 + "\\n")
    
    print("Testing chat request without chat_id...")
    test_chat_request_without_chat_id()
'''
    
    with open("test_request.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    logger.info("创建了测试请求脚本: test_request.py")

def check_frontend_chat_implementation():
    """检查前端聊天实现中是否包含 chat_id"""
    
    logger.info("=== 检查前端实现 ===")
    
    # 检查前端 API 调用
    openai_api_path = Path("src/lib/apis/openai/index.ts")
    
    if openai_api_path.exists():
        with open(openai_api_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查 chatCompletion 函数
        if "X-OpenWebUI-Chat-Id" in content:
            logger.info("✅ 前端已包含 X-OpenWebUI-Chat-Id 头部")
        else:
            logger.warning("❌ 前端未包含 X-OpenWebUI-Chat-Id 头部")
        
        if "metadata" in content:
            logger.info("✅ 前端支持 metadata 字段")
        else:
            logger.warning("❌ 前端不支持 metadata 字段")
    
    else:
        logger.error("找不到前端 API 文件")

def main():
    """主函数"""
    logger.info("开始调试 Open WebUI 的 chat_id 传递机制")
    
    # 1. 添加后端调试日志
    if add_debug_logging_to_openai_router():
        logger.info("✅ 已添加后端调试日志")
    else:
        logger.error("❌ 添加后端调试日志失败")
        return
    
    # 2. 检查前端实现
    check_frontend_chat_implementation()
    
    # 3. 创建测试脚本
    create_test_request_script()
    
    logger.info("调试设置完成！")
    logger.info("请执行以下步骤:")
    logger.info("1. 重启 Open WebUI 后端服务")
    logger.info("2. 修改 test_request.py 中的 token 和端口")
    logger.info("3. 运行 python test_request.py")
    logger.info("4. 查看后端日志中的调试信息")

if __name__ == "__main__":
    main()