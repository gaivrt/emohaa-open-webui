#!/usr/bin/env python3
"""
修复前端 chat_id 传递问题的脚本
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_openai_api():
    """修复前端 OpenAI API 调用，添加 chat_id 支持"""
    
    api_file = Path("src/lib/apis/openai/index.ts")
    
    if not api_file.exists():
        logger.error(f"文件不存在: {api_file}")
        return False
    
    with open(api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经修复
    if "X-OpenWebUI-Chat-Id" in content:
        logger.info("前端已包含 chat_id 支持，跳过修复")
        return True
    
    # 修复 chatCompletion 函数
    old_function = '''export const chatCompletion = async (
\ttoken: string = '',
\tbody: object,
\turl: string = `${WEBUI_BASE_URL}/api`
): Promise<[Response | null, AbortController]> => {
\tconst controller = new AbortController();
\tlet error = null;

\tconst res = await fetch(`${url}/chat/completions`, {
\t\tsignal: controller.signal,
\t\tmethod: 'POST',
\t\theaders: {
\t\t\tAuthorization: `Bearer ${token}`,
\t\t\t'Content-Type': 'application/json'
\t\t},
\t\tbody: JSON.stringify(body)
\t}).catch((err) => {
\t\tconsole.error(err);
\t\terror = err;
\t\treturn null;
\t});'''

    new_function = '''export const chatCompletion = async (
\ttoken: string = '',
\tbody: object,
\turl: string = `${WEBUI_BASE_URL}/api`,
\tchat_id?: string
): Promise<[Response | null, AbortController]> => {
\tconst controller = new AbortController();
\tlet error = null;

\t// 构建请求头
\tconst headers: Record<string, string> = {
\t\tAuthorization: `Bearer ${token}`,
\t\t'Content-Type': 'application/json'
\t};

\t// 如果提供了 chat_id，添加到头部和 body 中
\tif (chat_id) {
\t\theaders['X-OpenWebUI-Chat-Id'] = chat_id;
\t\t// 同时在 body 中添加 metadata
\t\tif (typeof body === 'object' && body !== null) {
\t\t\t(body as any).metadata = {
\t\t\t\t...(body as any).metadata,
\t\t\t\tchat_id: chat_id
\t\t\t};
\t\t}
\t}

\tconst res = await fetch(`${url}/chat/completions`, {
\t\tsignal: controller.signal,
\t\tmethod: 'POST',
\t\theaders,
\t\tbody: JSON.stringify(body)
\t}).catch((err) => {
\t\tconsole.error(err);
\t\terror = err;
\t\treturn null;
\t});'''

    # 替换函数
    if old_function in content:
        content = content.replace(old_function, new_function)
        logger.info("✅ 修复了 chatCompletion 函数")
    else:
        logger.warning("❌ 未找到 chatCompletion 函数的预期格式")
        return False

    # 同样修复 generateOpenAIChatCompletion 函数
    old_generate_function = '''export const generateOpenAIChatCompletion = async (
\ttoken: string = '',
\tbody: object,
\turl: string = `${WEBUI_BASE_URL}/api`
) => {
\tlet error = null;

\tconst res = await fetch(`${url}/chat/completions`, {
\t\tmethod: 'POST',
\t\theaders: {
\t\t\tAuthorization: `Bearer ${token}`,
\t\t\t'Content-Type': 'application/json'
\t\t},
\t\tbody: JSON.stringify(body)
\t})'''

    new_generate_function = '''export const generateOpenAIChatCompletion = async (
\ttoken: string = '',
\tbody: object,
\turl: string = `${WEBUI_BASE_URL}/api`,
\tchat_id?: string
) => {
\tlet error = null;

\t// 构建请求头
\tconst headers: Record<string, string> = {
\t\tAuthorization: `Bearer ${token}`,
\t\t'Content-Type': 'application/json'
\t};

\t// 如果提供了 chat_id，添加到头部和 body 中
\tif (chat_id) {
\t\theaders['X-OpenWebUI-Chat-Id'] = chat_id;
\t\t// 同时在 body 中添加 metadata
\t\tif (typeof body === 'object' && body !== null) {
\t\t\t(body as any).metadata = {
\t\t\t\t...(body as any).metadata,
\t\t\t\tchat_id: chat_id
\t\t\t};
\t\t}
\t}

\tconst res = await fetch(`${url}/chat/completions`, {
\t\tmethod: 'POST',
\t\theaders,
\t\tbody: JSON.stringify(body)
\t})'''

    if old_generate_function in content:
        content = content.replace(old_generate_function, new_generate_function)
        logger.info("✅ 修复了 generateOpenAIChatCompletion 函数")
    else:
        logger.warning("❌ 未找到 generateOpenAIChatCompletion 函数的预期格式")

    # 写回文件
    with open(api_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info("✅ 前端 OpenAI API 修复完成")
    return True

def create_test_integration_script():
    """创建集成测试脚本"""
    
    test_script = '''#!/usr/bin/env python3
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
    
    print("\\n" + "="*50 + "\\n")
    
    # 测试不带 chat_id 的单次对话
    test_without_chat_id()
    
    print("\\n=== 测试完成 ===")
    print("查看后端日志以确认 chat_id 是否被正确接收")
'''
    
    with open("test_chat_integration.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    logger.info("创建了集成测试脚本: test_chat_integration.py")

def main():
    """主函数"""
    logger.info("开始修复前端 chat_id 传递问题")
    
    # 1. 修复前端 API
    if fix_openai_api():
        logger.info("✅ 前端修复完成")
    else:
        logger.error("❌ 前端修复失败")
        return
    
    # 2. 创建测试脚本
    create_test_integration_script()
    
    logger.info("修复完成！")
    logger.info("接下来的步骤:")
    logger.info("1. 重新构建前端: npm run build")
    logger.info("2. 重启 WebUI 服务")
    logger.info("3. 修改 test_chat_integration.py 中的配置")
    logger.info("4. 运行集成测试: python test_chat_integration.py")
    logger.info("5. 查看后端日志确认 chat_id 被正确接收")

if __name__ == "__main__":
    main()