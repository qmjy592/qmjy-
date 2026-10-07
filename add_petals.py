import os, re
p = os.path.expanduser('~/portal_project/index.html')
with open(p, 'r', encoding='utf-8') as f: html = f.read()

# 1. 清理之前可能存在的残留花瓣代码（防止重复叠加）
html = re.sub(r'<style>\s*/\* 花瓣飘落特效 \*/[\s\S]*?</style>', '', html)
html = re.sub(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{[\s\S]*?花瓣飘落[\s\S]*?</script>', '', html)

# 2. 定义花瓣的 CSS 与 JS
css = """
<style>
/* 花瓣飘落特效 */
.petal {
    position: fixed;
    top: -10vh;
    z-index: 99999;
    pointer-events: none; /* 关键：不干扰任何点击操作 */
    background: linear-gradient(135deg, #ffb7c5, #ff8fa3);
    border-radius: 50% 0 50% 50%;
    transform: rotate(45deg);
    box-shadow: 0 2px 8px rgba(255, 183, 197, 0.4);
    animation: fall linear infinite;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); opacity: 1; }
    100% { transform: translateY(120vh) rotate(360deg); opacity: 0; }
}
</style>
"""

js = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    const petalCount = 10; // 花瓣数量，控制为10片以保证手机流畅
    for (let i = 0; i < petalCount; i++) {
        const petal = document.createElement('div');
        petal.className = 'petal';
        const size = Math.random() * 12 + 8; // 花瓣大小 8px - 20px
        petal.style.width = size + 'px';
        petal.style.height = size + 'px';
        petal.style.left = Math.random() * 100 + 'vw';
        petal.style.animationDuration = (Math.random() * 5 + 6) + 's'; // 持续 6-11 秒
        petal.style.animationDelay = Math.random() * 5 + 's'; // 错落有致地出现
        document.body.appendChild(petal);
    }
});
</script>
"""

# 3. 安全注入到 HTML 中
if '/* 花瓣飘落特效 */' not in html:
    html = html.replace('</head>', css + '\n</head>')
    html = html.replace('</body>', js + '\n</body>')

with open(p, 'w', encoding='utf-8') as f: f.write(html)
print("✅ 浪漫的花瓣飘落特效已注入！")
