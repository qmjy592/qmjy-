import os, re
p = os.path.expanduser('~/portal_project/index.html')
with open(p, 'r', encoding='utf-8') as f: html = f.read()

# 1. 清理之前所有失败或冲突的背景样式
html = re.sub(r'<style>\s*/\* 桌面端背景 \*/[\s\S]*?</style>', '', html)
html = re.sub(r'<style>\s*/\* 1\. 基础背景（所有设备通用）[\s\S]*?</style>', '', html)

# 2. 定义最终完美的背景样式
bg_filename = "CH0335_home_Idle_01_2.592500000000002.png"

css = f"""
<style>
/* 手机端：继续保持跨性别旗渐变 */
@media (max-width: 768px) {{
    body {{
        background: linear-gradient(135deg, #5BCEFA 0%, #F5A9B8 35%, #FFFFFF 50%, #F5A9B8 65%, #5BCEFA 100%) !important;
        background-attachment: fixed !important;
    }}
    body.dark {{
        background: linear-gradient(135deg, #2d0a3e 0%, #4a154b 35%, #1a0b2e 50%, #4a154b 65%, #2d0a3e 100%) !important;
    }}
}}
/* 电脑端：使用你提供的专属图片 */
@media (min-width: 769px) {{
    body {{
        background-image: url('{bg_filename}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        background-color: #F5A9B8 !important; /* 兜底颜色，即使图片没加载出来也不会白屏 */
    }}
    /* 电脑端卡片调整不透明度，保证文字清晰 */
    .profile-card, .section-card, .stat-box, .game-box, .modal-content, .social-item {{
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
    }}
    body.dark .profile-card, body.dark .section-card, body.dark .stat-box, body.dark .game-box, body.dark .modal-content, body.dark .social-item {{
        background: rgba(30, 15, 50, 0.85) !important;
    }}
}}
</style>
"""
if '/* 手机端：继续保持跨性别旗渐变 */' not in html:
    html = html.replace('</head>', css + '\n</head>')

with open(p, 'w', encoding='utf-8') as f: f.write(html)
print("✅ 电脑端专属背景已成功应用！")
