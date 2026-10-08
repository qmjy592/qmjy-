# 🌸 芊茗静语的专属空间 (Portal Project)

一个基于 Python 的个人全栈空间，支持 **Linux (PC/服务器)** 与 **Android Termux** 双端运行。包含个人主页、云端 AI 伴侣、音乐盒、五子棋、扫雷及论坛等模块。

## ✨ 核心功能
- **🏠 个人主页**：个人资料与统计，支持实时修改。
- **🤖 AI 伴侣**：云端 API 对话，支持气泡渲染、历史记录、主人/访客模式。
- **🎵 音乐盒**：本地音乐播放器，支持单曲/列表循环。
- **🎮 小游戏**：五子棋（联机）、扫雷（单机，含首点保护与空白格自动展开）。
- **🌐 论坛与媒体**：媒体账号展示及本地帖子存储。

## 🛠️ 技术栈
- **前端**：HTML5 / CSS3 / 原生 JavaScript (渐变主题、毛玻璃特效)
- **后端**：Python 3 (内置 HTTP Server)
- **AI**：云端 API (主力)，llama.cpp (本地编译备用)
- **环境**：Linux (Ubuntu/Debian) 或 Termux

## 🚀 部署指南

### 1. Linux 环境
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv git cmake build-essential -y
git clone https://github.com/qmjy592/qmjy-.git && cd qmjy-
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
nohup python3 my_ultimate_portal.py > server.log 2>&1 &
```

2. Termux 环境

```bash
pkg update && pkg upgrade -y
pkg install python git cmake make clang -y
termux-setup-storage
cd ~/portal_project && source venv/bin/activate
pip install -r requirements.txt
nohup python my_ultimate_portal.py > server.log 2>&1 &
```

启动后，浏览器访问 http://127.0.0.1:8001 即可。

⚠️ 重要提示

1. 编译兼容：仓库中的 llama.cpp-master 为手机 ARM64 编译产物，Linux 上无法直接运行。如需在 Linux 使用，请重新执行 cmake -B build && cmake --build build --config Release -j4。
2. 密钥安全：切勿将云端 API 密钥直接写入代码。请使用 config.json 或环境变量配置，并确保将其加入 .gitignore。
3. 模型备份：AI 模型 (models/) 和虚拟环境 (venv/) 体积较大，未上传至仓库，请通过网盘等另行备份。

📜 版权声明 (Copyright)

中文说明：
Copyright (c) 2024 卢清茗 (芊茗静语). All Rights Reserved.
未经作者明确书面许可，禁止任何形式的修改、分发、商用。仅供个人查看和演示使用。

English Version:
Copyright (c) 2024 Lu Qingming (Qianming Jingyu). All Rights Reserved.
No unauthorized copying, modification, distribution, or commercial use is permitted without explicit written permission from the author. This repository is made public for viewing and demonstration purposes only.

(任何未经授权的使用、复制或分发行为都将被视为违反版权法，并保留追究法律责任的权利。)
