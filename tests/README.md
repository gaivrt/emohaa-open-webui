# 测试文件目录

本目录包含项目的测试脚本和相关工具。

## 目录结构

### chat_id_feature/
Chat ID 和 User ID 传递功能的相关测试文件：

- `test_request.py` - 基础API请求测试
- `test_chat_id_debug.py` - Chat ID调试测试脚本
- `test_chat_integration.py` - 完整集成测试
- `fix_chat_id_frontend.py` - 前端修复脚本

## 使用说明

### 运行测试
```bash
# 进入测试目录
cd tests/chat_id_feature

# 运行单个测试
python test_request.py

# 运行集成测试
python test_chat_integration.py
```

### 测试环境要求
- Python 3.11+
- 相关依赖包（见各测试文件注释）
- WebUI 后端服务运行中
- OpenDify 服务运行中

## 注意事项

- 运行测试前确保所有相关服务已启动
- 测试脚本中的URL和配置请根据实际环境调整
- 调试测试可能会输出大量日志信息

## 贡献指南

添加新测试时请遵循以下规范：
1. 使用描述性的文件名
2. 在文件头部添加功能说明注释
3. 包含必要的错误处理
4. 更新此 README 文档