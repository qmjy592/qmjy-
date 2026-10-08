# 🌸 芊茗静语的专属空间 (Portal Project)

这是一个基于 Android Termux 环境构建的**全栈个人专属空间**。项目集成了个人主页、云端 AI 伴侣、本地推理框架 (llama.cpp)、音乐播放器以及联机/单机小游戏等丰富功能。

## ✨ 功能特性

- **🏠 个人主页 (Profile)**
  - 动态展示个人资料（昵称、身份标签：跨性别女性/INFP/HRT、口号及现居地）。
  - 实时统计数据（距离出生已过天数、发帖数量等）。
  - 支持修改个人资料并持久化保存。

- **🤖 AI 伴侣 (AI Companion)**
  - 基于云端 API 的智能对话系统。
  - 支持聊天气泡渲染、历史记录滚动、思考中状态提示。
  - 包含“访客模式”与“主人模式”身份切换。

- **🎵 音乐盒 (Music Box)**
  - 本地音乐播放器，支持歌单展示、循环模式（单曲/列表）、进度条控制。
  - 适配移动端与桌面端的沉浸式播放界面。

- **🎮 小游戏 (Mini Games)**
  - **五子棋（联机）**：支持房间匹配与对弈。
  - **扫雷（单机）**：修复了首点保护机制，优化了自动展开算法（点击空白格自动展开一片，点击数字仅显示数字）。

- **🌐 论坛与媒体 (Forum & Media)**
  - 展示个人媒体账号（GitHub、Bilibili、Twitter、QQ等）。
  - 本地化论坛帖子存储与展示。

## 🛠️ 技术栈

- **前端**：HTML5 / CSS3 (渐变主题、毛玻璃特效、响应式深浅色模式) / 原生 JavaScript。
- **后端**：Python 3 (内置 HTTP Server，处理 API 路由与静态资源)。
- **推理框架**：llama.cpp (在 Android ARM64 环境下本地编译，作为备用离线方案)。
- **AI 服务**：云端 API（当前主力对话方案）。
- **运行环境**：Termux (Android 终端模拟器)。

## 📁 项目结构

```text
portal_project/
├── index.html                  # 前端主页面 (UI 与前端逻辑)
├── my_ultimate_portal.py       # Python 后端核心程序 (路由与 API 转发)
├── llama.cpp-master/           # 本地编译的推理框架 (包含编译产物)
├── models/                     # AI 模型文件夹 (未包含在此仓库中，需本地放置)
├── music/                      # 音乐资源文件夹
├── profile.json                # 个人资料数据
├── hrt.json                    # HRT 记录数据
├── forum.json                  # 论坛帖子数据
├── requirements.txt            # Python 依赖清单
├── LICENSE                     # 版权声明
└── README.md                   # 项目说明文档
```

🚀 安装与运行 (Termux 环境)

1. 环境准备

确保你的 Termux 已安装基础依赖：

```bash
pkg update && pkg upgrade -y
pkg install python git cmake make clang -y
termux-setup-storage
```

2. 安装项目依赖

```bash
cd ~/portal_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 准备 AI 模型 (可选)

如果你需要使用本地 llama.cpp 推理，请将 .gguf 模型文件放入 models/ 目录中。
(注意：本仓库已通过 .gitignore 忽略 models/，模型文件需自行通过网盘等方式备份)

4. 启动后端服务

```bash
cd ~/portal_project
source venv/bin/activate
nohup python my_ultimate_portal.py > server.log 2>&1 &
```

启动后，在手机浏览器访问 http://127.0.0.1:8001 即可进入你的专属空间。

💾 数据安全与备份

· 云端备份：代码、前端资源、编译产物已通过 Git 上传至 GitHub。
· 本地备份：AI 模型文件（models/）、虚拟环境（venv/）以及日志文件（server.log）不会被 Git 追踪，建议定期通过网盘或本地存储进行备份。
· 敏感信息：请勿将 API 密钥直接写入 Python 代码中。建议使用环境变量或本地 config.json 进行配置，并确保该文件已加入 .gitignore。

⚠️ 版权声明 (Copyright)

Copyright (c) 2024 卢清茗 (芊茗静语). All Rights Reserved.

This source code and all associated files (including but not limited to frontend, backend, music, and compiled binaries) are the exclusive property of the author.

1. NO UNAUTHORIZED COPYING: You may not copy, modify, merge, publish, distribute, sublicense, or sell copies of this software.
2. NO COMMERCIAL USE: This software may not be used for any commercial purposes without explicit written permission from the author.
3. VIEWING ONLY: This repository is made public for viewing and demonstration purposes only.

Any unauthorized use, reproduction, or distribution of this code or its associated assets will be considered a violation of copyright law and will be pursued to the fullest extent of the law.
