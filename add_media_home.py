import os
p = os.path.expanduser('~/portal_project/index.html')
with open(p, 'r', encoding='utf-8') as f: html = f.read()

# 1. 替换原来的渲染逻辑，把“其他”改成你指定的 QQ 信息
old_other = '''<div class="social-item"><div class="icon">🔗</div><div class="info"><span>其他</span><span>${p.other || '未添加'}</span></div></div>`
new_other = '''<div class="social-item"><div class="icon">🔗</div><div class="info"><span>QQ 邮箱与 QQ 号</span><span style="white-space: pre-wrap; font-size:0.8rem;">2114006874 / 2114006874@qq.com\nQQ小号: 2271705989 / 2271705989@qq.com</span></div></div>`'''
html = html.replace(old_other, new_other)

# 2. 注入 JS，动态把媒体账号克隆到首页底部
js_code = """
<script>
function cloneMediaToHome() {
    const home = document.getElementById('home');
    const socialGrid = document.getElementById('social-links');
    if (!home || !socialGrid) return;
    
    // 防止重复克隆
    if (document.getElementById('home-social-container')) return;
    
    // 创建首页的媒体账号卡片
    const newCard = document.createElement('div');
    newCard.id = 'home-social-container';
    newCard.className = 'section-card';
    newCard.innerHTML = '<h3>🔗 我的媒体账号</h3><div class="social-grid" id="home-social-grid"></div>';
    
    // 克隆媒体账号网格
    const clonedGrid = socialGrid.cloneNode(true);
    clonedGrid.id = 'home-social-grid-cloned';
    newCard.querySelector('#home-social-grid').replaceWith(clonedGrid);
    
    // 把新卡片插入到首页的“个人经历”或“HRT用药记录”卡片之后
    const hrtCard = Array.from(home.querySelectorAll('.section-card')).find(c => c.querySelector('#title-hrt'));
    const expCard = Array.from(home.querySelectorAll('.section-card')).find(c => c.querySelector('#title-exp'));
    const targetCard = hrtCard || expCard;
    
    if (targetCard) {
        targetCard.parentNode.insertBefore(newCard, targetCard.nextSibling);
    } else {
        home.appendChild(newCard); // 兜底
    }
}

// 在页面加载及切换页面时调用，确保数据渲染后立即克隆
const originalInitPage = window.initPage;
window.initPage = function() {
    if (originalInitPage) originalInitPage();
    setTimeout(cloneMediaToHome, 500); // 延迟执行，等社交链接渲染完毕
};
</script>
"""

if 'function cloneMediaToHome()' not in html:
    html = html.replace('</body>', js_code + '\n</body>')

with open(p, 'w', encoding='utf-8') as f: f.write(html)
print("✅ 媒体账号已成功添加到首页底部，且“其他”已替换为QQ信息！")
