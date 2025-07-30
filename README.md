# Emohaa Open WebUI

[English](docs/README.md) | [简体中文](docs/README.md)

---

📚 **完整文档请查看 [docs](./docs/) 目录**

## 快速开始

### 方法一：直接部署（推荐）
```bash
git clone https://github.com/gaivrt/emohaa-open-webui.git
cd emohaa-open-webui
chmod +x run-compose.sh
./run-compose.sh
```

### 方法二：导出镜像部署
```bash
# 本地构建并导出
./export_image.sh

# 传输到服务器
scp emohaa-open-webui.tar.gz user@server:/path/

# 服务器部署
docker load < emohaa-open-webui.tar.gz
./run_docker.sh
```

## 文档目录

### 📋 核心文档
- [🏗️ 项目架构](./docs/ARCHITECTURE.md) - 系统架构和技术栈概览
- [📖 完整部署指南](./docs/DEPLOYMENT.md) - 详细的部署和安装指导
- [⚙️ 安装说明](./docs/INSTALLATION.md) - 基础安装步骤
- [🛠️ 故障排除](./docs/TROUBLESHOOTING.md) - 常见问题解决方案

### 🚀 功能特性
- [💬 Chat ID 传递解决方案](./docs/features/CHAT_ID_ISSUE_SOLUTION.md) - 多轮对话历史记录修复
- [👤 User ID 转发功能](./docs/features/USER_ID_FORWARDING_SOLUTION.md) - 用户身份端到端传递

### 🔧 开发相关
- [🤝 贡献指南](./docs/CONTRIBUTING.md) - 如何参与项目开发
- [🔒 安全说明](./docs/SECURITY.md) - 安全相关信息
- [🔧 自定义指南](./docs/CUSTOMIZATION_CHECKLIST.md) - 自定义配置指南

### 📁 目录结构
```
emohaa-open-webui/
├── docs/              # 📚 完整文档
│   ├── features/      # 🚀 功能特性文档
│   ├── development/   # 💻 开发文档
│   └── legal/         # 📄 法律文档
├── tests/             # 🧪 测试文件
│   └── chat_id_feature/
├── backend/           # ⚙️ 后端服务
├── src/               # 🎨 前端源码
└── static/            # 📁 静态资源
```

## 支持

遇到问题？查看 [故障排除文档](./docs/TROUBLESHOOTING.md) 或提交 [Issue](https://github.com/gaivrt/emohaa-open-webui/issues)。

---

> 基于 [Open WebUI](https://github.com/open-webui/open-webui) 定制