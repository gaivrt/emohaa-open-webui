# Changelog

## [2025-07-30] - 2025-07-30

### 🐛 Bug Fixes
- **WebUI 后端转发**: 修复 X-OpenWebUI-Chat-Id 头部未正确转发到外部 API 的问题
- **配置依赖**: 移除 chat_id 转发对 ENABLE_FORWARD_USER_INFO_HEADERS 配置的依赖
- **请求头处理**: 改为直接从 HTTP 请求头获取 chat_id，而不仅仅依赖 metadata

### ✨ Features
- **User ID 转发**: 实现用户ID从前端到外部API的完整传递链路
- **双重身份传递**: 同时转发 Chat ID 和 User ID，支持精确的用户会话管理
- **调试日志**: 添加详细的 chat_id 和 user_id 转发状态跟踪日志
- **兼容性**: 同时支持从请求头和 metadata 获取身份信息

### 🔧 Technical Details
- 修改文件: 
  - `backend/open_webui/routers/openai.py` - 后端转发逻辑
  - `src/lib/apis/openai/index.ts` - 前端API函数
  - `src/lib/components/chat/Chat.svelte` - 组件调用
- 核心变更: 
  - 从 `request.headers.get("x-openwebui-chat-id")` 和 `request.headers.get("x-openwebui-user-id")` 获取身份信息
  - 始终转发 chat_id 和 user_id 到外部 API，不受配置限制
  - 前端发送 `X-OpenWebUI-Chat-Id` 和 `X-OpenWebUI-User-Id` 头部
  - 添加详细的转发状态调试日志

### 🎯 Impact
修复了多轮对话和用户身份识别问题：
- **Chat ID**: 前端发送 chat_id 但后端未正确转发给 OpenDify/Dify
- **User ID**: 实现用户身份的端到端传递，支持用户级会话管理
- **解决方案**: 直接从请求头获取并始终转发关键身份信息

### 📊 Validation
- 前端已验证正确发送 `x-openwebui-chat-id` 和 `x-openwebui-user-id` 头部
- 后端转发逻辑实现完成
- User ID 转发功能文档已完成 (`docs/USER_ID_FORWARDING_SOLUTION.md`)

### 🔄 功能状态
- ✅ Chat ID 转发: 完成并验证
- ✅ User ID 转发: 完成实现
- ✅ 前端发送: 同时发送 Chat ID 和 User ID
- ✅ 后端转发: 始终转发关键身份信息
- ✅ 调试日志: 详细的转发状态跟踪
- ✅ 文档完善: 问题分析和解决方案文档