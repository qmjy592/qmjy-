import os
p = os.path.expanduser('~/portal_project/index.html')
with open(p, 'r', encoding='utf-8') as f: html = f.read()

css = """
<style>
/* 仅在电脑端隐藏导航栏的“媒体账号”按钮 */
@media (min-width: 769px) {
    #nav-accounts {
        display: none !important;
    }
}
</style>
"""
if '/* 仅在电脑端隐藏导航栏的“媒体账号”按钮 */' not in html:
    html = html.replace('</head>', css + '\n</head>')

with open(p, 'w', encoding='utf-8') as f: f.write(html)
print("✅ 电脑端导航栏的“媒体账号”按钮已隐藏，手机端不受影响！")
