import os, re
p = os.path.expanduser('~/portal_project/index.html')
with open(p, 'r', encoding='utf-8') as f: html = f.read()

# 1. 在 fetchGomokuState 函数开头加判断：不在游戏页面就直接返回，不发送请求
old_func = "function fetchGomokuState() { fetch('/api/state')"
new_func = "function fetchGomokuState() { if (typeof currentPage !== 'undefined' && currentPage !== 'games') return; fetch('/api/state')"
html = html.replace(old_func, new_func)

# 2. 增加页面可见性监听，切到后台自动暂停，切回前台自动恢复
js_add = """
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // 切到后台，立刻停止轮询
        if (typeof gomokuTimer !== 'undefined' && gomokuTimer) { clearInterval(gomokuTimer); gomokuTimer = null; }
    } else {
        // 切回前台，如果还在游戏页面，重新启动轮询
        if (typeof currentPage !== 'undefined' && currentPage === 'games') {
            if (typeof gomokuTimer === 'undefined' || !gomokuTimer) {
                gomokuTimer = setInterval(fetchGomokuState, 1000);
                fetchGomokuState();
            }
        }
    }
});
"""

if 'document.hidden' not in html:
    html = html.replace('</script>', js_add + '\n</script>')

with open(p, 'w', encoding='utf-8') as f: f.write(html)
print("✅ 修复成功！不在游戏页面或手机切后台时，将彻底停止 /api/state 请求。")
