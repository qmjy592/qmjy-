import os
p = os.path.expanduser('~/portal_project/index.html')
with open(p, 'r', encoding='utf-8') as f: html = f.read()

# 只做纯追加，不删除任何已有代码，保证不弄乱！
css = """
<style>
/* 纯追加的电脑端排版补丁，绝不覆盖背景 */
@media (min-width: 769px) {
    /* 1. 卡片样式：极简白底、柔和阴影、大圆角（仿朋友的干净风格） */
    .profile-card, .section-card, .stat-box, .game-box, .social-item, .song-item, .post-item {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06) !important;
        border-radius: 24px !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
    }
    
    /* 2. 个人资料卡：左图右文布局 */
    #home .profile-card {
        flex-direction: row !important;
        text-align: left !important;
        padding: 40px !important;
        gap: 40px !important;
        align-items: center !important;
    }
    #home .profile-card .avatar { width: 160px !important; height: 160px !important; margin-bottom: 0 !important; }
    #home .profile-card h1 { font-size: 2.5rem !important; }
    #home .profile-card .info-wrapper { flex: 1 !important; }

    /* 3. 统计卡片：9个排成两行，居中 */
    #home .stats-grid {
        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        gap: 20px !important;
        margin-bottom: 40px !important;
    }

    /* 4. 顶部导航栏：变成居中悬浮的胶囊 */
    .nav-bar {
        top: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: auto !important;
        min-width: 600px !important;
        max-width: 90% !important;
        border-radius: 40px !important;
        padding: 10px 24px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
    }

    /* 5. 媒体账号：变成一排四个卡片 */
    #social-links { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 15px !important; }
    #social-links .social-item { flex-direction: column !important; text-align: center !important; gap: 10px !important; padding: 20px 10px !important; }
}
</style>
"""
# 使用 find 追加，如果已经存在则忽略，绝不删除旧内容
if '/* 纯追加的电脑端排版补丁，绝不覆盖背景 */' not in html:
    html = html.replace('</head>', css + '\n</head>')

with open(p, 'w', encoding='utf-8') as f: f.write(html)
print("✅ 安全排版补丁已追加！背景图毫发无损。")
