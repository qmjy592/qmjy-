import json, os, requests, base64, urllib.parse, re, subprocess, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_FILE = os.path.join(BASE_DIR, "profile.json")
FORUM_FILE = os.path.join(BASE_DIR, "forum.json")
AVATAR_FILE = os.path.join(BASE_DIR, "avatar.png")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
if not os.path.exists(FORUM_FILE):
    with open(FORUM_FILE, 'w', encoding='utf-8') as f: json.dump([], f)
if not os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"nickname": "芊茗静语", "cn_name": "卢清茗", "jp_name": "せんめいせいご", "gender": "女", "birth": "2009-10-30", "mbti": "INFP", "location": "广西南宁市兴宁区", "motto": "我们活着，就是对恶意最大的反抗！", "exp": "暂无记录...", "hrt": "暂无记录...", "bilibili": "点击修改添加", "twitter": "点击修改添加", "google": "点击修改添加", "other": "点击修改添加"}, f, ensure_ascii=False)

class AI(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path = self.path.split("?")[0]
        if self.path == '/avatar':
            if os.path.exists(AVATAR_FILE):
                self.send_response(200); self.send_header('Content-Type', 'image/png'); self.end_headers()
                self.wfile.write(open(AVATAR_FILE, 'rb').read())
            else: self.send_response(404); self.end_headers()
        elif self.path == '/profile/get':
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(open(PROFILE_FILE, 'rb').read())
        elif self.path == '/forum/get':
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(open(FORUM_FILE, 'rb').read())
        elif self.path == '/stats/get':
            stats = {"days": 0, "songs": 0, "posts": 0}
            try:
                profile = json.load(open(PROFILE_FILE, 'r', encoding='utf-8'))
                birth = profile.get('birth', '2009-10-30')
                stats["days"] = (datetime.datetime.now() - datetime.datetime.strptime(birth, "%Y-%m-%d")).days
                if os.path.exists(MUSIC_DIR):
                    for cat in os.listdir(MUSIC_DIR):
                        cat_dir = os.path.join(MUSIC_DIR, cat)
                        if os.path.isdir(cat_dir):
                            stats["songs"] += len([f for f in os.listdir(cat_dir) if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a'))])
                if os.path.exists(FORUM_FILE):
                    stats["posts"] = len(json.load(open(FORUM_FILE, 'r', encoding='utf-8')))
            except Exception as e: print(f"Stats error: {e}")
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        elif self.path == '/music/list':
            musics = []
            if os.path.exists(MUSIC_DIR):
                for cat in os.listdir(MUSIC_DIR):
                    cat_dir = os.path.join(MUSIC_DIR, cat)
                    if os.path.isdir(cat_dir):
                        for f in sorted(os.listdir(cat_dir), reverse=True):
                            if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                                musics.append({"name": f, "file": f"{cat}/{f}", "category": cat})
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(musics, ensure_ascii=False).encode())
        elif self.path.startswith('/music/file/'):
            filename = urllib.parse.unquote(self.path.replace('/music/file/', ''))
            filepath = os.path.join(MUSIC_DIR, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                content_type = 'audio/mpeg'
                if filename.lower().endswith('.wav'): content_type = 'audio/wav'
                elif filename.lower().endswith('.ogg'): content_type = 'audio/ogg'
                elif filename.lower().endswith('.m4a'): content_type = 'audio/mp4'
                range_header = self.headers.get('Range', None)
                if range_header:
                    match = re.search(r'bytes=(\d+)-(\d*)', range_header)
                    start = int(match.group(1)); end = int(match.group(2)) if match.group(2) else file_size - 1
                    length = end - start + 1
                    self.send_response(206); self.send_header('Content-Type', content_type); self.send_header('Accept-Ranges', 'bytes'); self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}'); self.send_header('Content-Length', str(length)); self.end_headers()
                    try:
                        with open(filepath, 'rb') as f:
                            f.seek(start); chunk = f.read(1024 * 64)
                            while chunk: self.wfile.write(chunk); chunk = f.read(1024 * 64)
                    except: pass
                else:
                    self.send_response(200); self.send_header('Content-Type', content_type); self.send_header('Content-Length', str(file_size)); self.send_header('Accept-Ranges', 'bytes'); self.end_headers()
                    try:
                        with open(filepath, 'rb') as f: self.wfile.write(f.read())
                    except: pass
            else: self.send_response(404); self.end_headers()
        else:
            try:
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers()
                with open(os.path.join(BASE_DIR, 'index.html'), 'rb') as f: self.wfile.write(f.read())
            except (BrokenPipeError, ConnectionResetError): pass
    def do_POST(self):
        l = int(self.headers['Content-Length']); raw = self.rfile.read(l)
        if self.path == '/upload_avatar':
            try:
                img_data = raw.decode('utf-8').split(',')[1]
                with open(AVATAR_FILE, 'wb') as f: f.write(base64.b64decode(img_data))
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/profile/update':
            try:
                data = json.loads(raw); json.dump(data, open(PROFILE_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/forum/post':
            try:
                data = json.loads(raw); posts = json.load(open(FORUM_FILE, 'r', encoding='utf-8')); posts.insert(0, {"content": data['content'], "time": datetime.datetime.now().strftime("%m月%d日 %H:%M")}); json.dump(posts, open(FORUM_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/music/upload':
            try:
                data = json.loads(raw); cat = data.get('category', '未分类').strip(); cat_dir = os.path.join(MUSIC_DIR, cat)
                if not os.path.exists(cat_dir): os.makedirs(cat_dir)
                filename = data['name']; safe_name = "".join([c for c in filename if c.isalnum() or c in "._-()[] "])
                if not safe_name.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')): safe_name += ".mp3"
                filepath = os.path.join(cat_dir, safe_name); audio_data = data['data'].split(',')[1]
                if len(audio_data) > 20 * 1024 * 1024: raise Exception("文件过大")
                with open(filepath, 'wb') as f: f.write(base64.b64decode(audio_data))
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/ai/start':
            try:
                os.system("pkill -9 llama-server")
                subprocess.Popen("cd ~/llama.cpp-master && nohup ./build/bin/llama-server -m qwen2.5-1.5b-instruct-q4_k_m.gguf -c 1024 -t 4 --host 0.0.0.0 --port 8080 > /dev/null 2>&1 &", shell=True)
                self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
                self.wfile.write(json.dumps({"status": "starting"}).encode())
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/chat':
            data = json.loads(raw); is_owner = data.get('isOwner', False)
            try:
                if is_owner:
                    prompt_text = "你是芊茗静语的专属AI伙伴。芊茗静语是一个跨性别女性。你说话要温柔、真诚、可爱，一定要记得她的名字，让她感到温暖和陪伴。请用简短的话回答，不要废话。"
                else:
                    prompt_text = "你是一个客观、中立的通用AI助手。用户是普通访客，你不是他们的私人陪伴。严禁称呼用户为'芊茗静语'，严禁提及任何有关主人的私人信息。请保持礼貌、专业、简洁地回答问题。"
                p = f"{prompt_text}\n用户：{data['message']}\nAI："
                r = requests.post("http://127.0.0.1:8080/v1/chat/completions", 
                                  json={"messages": [{"role":"user","content":p}], 
                                        "temperature": 0.3, "frequency_penalty": 1.2, 
                                        "presence_penalty": 0.8, "max_tokens": 48,
                                        "stop": ["用户：", "AI：", "\n\n"]}, timeout=600).json()
                reply = r['choices'][0]['message']['content']
            except: reply = "大脑反应有点慢，请再试一次。"
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}, ensure_ascii=False).encode())

if __name__ == '__main__':
    print("🔥 静语的专属空间后端服务器（终极修复版）已启动！")
    ThreadingHTTPServer(('0.0.0.0', 8001), AI).serve_forever()
