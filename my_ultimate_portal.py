# Copyright (c) 2024 卢清茗. All Rights Reserved. 未经授权禁止修改和分发。
import json, os, requests, base64, urllib.parse, re, datetime, threading, time, random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_FILE = os.path.join(BASE_DIR, "profile.json")
FORUM_FILE = os.path.join(BASE_DIR, "forum.json")
AVATAR_FILE = os.path.join(BASE_DIR, "avatar.png")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
CLOUD_API_URL = "https://api.deepseek.com/chat/completions"
CLOUD_API_KEY = "sk-70dda1512a994242b4aec0e16e2adab0"
CLOUD_MODEL_NAME = "deepseek-chat"
CHAT_SEMAPHORE = threading.Semaphore(1)
GOMOKU = {
    "board": [[0]*15 for _ in range(15)],
    "current_player": 0, "status": "waiting", "winner": None,
    "turn_time_limit": 30, "turn_start_time": 0,
    "undo_left": {"black": 3, "white": 3}, "draw_left": {"black": 3, "white": 3},
    "pending_action": None, "requester": None,
    "players": {"p1": None, "p2": None},
    "match_ready": {"p1": False, "p2": False},
    "play_ready": {"p1": False, "p2": False},
    "roles": {"p1": None, "p2": None},
    "last_move": None, "move_count": 0, "last_action_msg": "等待玩家加入..."
}
gomoku_lock = threading.Lock()
def check_win(x, y, player):
    for dx, dy in ([1,0],[0,1],[1,1],[1,-1]):
        cnt = 1
        for s in (1, -1):
            for i in range(1, 5):
                nx, ny = x + dx*i*s, y + dy*i*s
                if 0 <= nx < 15 and 0 <= ny < 15 and GOMOKU["board"][ny][nx] == player: cnt += 1
                else: break
        if cnt >= 5: return True
    return False
if not os.path.exists(MUSIC_DIR): os.makedirs(MUSIC_DIR)
if not os.path.exists(FORUM_FILE):
    with open(FORUM_FILE, 'w', encoding='utf-8') as f: json.dump([], f)
if not os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"nickname": "芊茗静语", "cn_name": "卢清茗", "jp_name": "せんめいせいご", "gender": "女", "birth": "2009-10-30", "mbti": "INFP", "location": "广西南宁市兴宁区", "motto": "我们活着，就是对恶意最大的反抗！", "exp": "暂无记录...", "hrt": "暂无记录...", "bilibili": "点击修改添加", "twitter": "点击修改添加", "google": "点击修改添加", "other": "点击修改添加"}, f, ensure_ascii=False)
class AI(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status); self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body))); self.send_header('Cache-Control', 'no-store')
        self.end_headers(); self.wfile.write(body)
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
                stats["days"] = (datetime.datetime.now() - datetime.datetime.strptime(profile.get('birth', '2009-10-30'), "%Y-%m-%d")).days
                if os.path.exists(MUSIC_DIR):
                    for cat in os.listdir(MUSIC_DIR):
                        cat_dir = os.path.join(MUSIC_DIR, cat)
                        if os.path.isdir(cat_dir): stats["songs"] += len([f for f in os.listdir(cat_dir) if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a'))])
                if os.path.exists(FORUM_FILE): stats["posts"] = len(json.load(open(FORUM_FILE, 'r', encoding='utf-8')))
            except: pass
            self.send_json(stats)
        elif self.path == '/music/list':
            musics = []
            if os.path.exists(MUSIC_DIR):
                for cat in os.listdir(MUSIC_DIR):
                    cat_dir = os.path.join(MUSIC_DIR, cat)
                    if os.path.isdir(cat_dir):
                        for f in sorted(os.listdir(cat_dir), reverse=True):
                            if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')): musics.append({"name": f, "file": f"{cat}/{f}", "category": cat})
            self.send_json(musics)
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
                    m = re.search(r'bytes=(\d+)-(\d*)', range_header)
                    start = int(m.group(1)); end = int(m.group(2)) if m.group(2) else file_size - 1
                    self.send_response(206); self.send_header('Content-Type', content_type); self.send_header('Accept-Ranges', 'bytes'); self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}'); self.send_header('Content-Length', str(end - start + 1)); self.end_headers()
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
        elif self.path == '/api/state':
            with gomoku_lock:
                if GOMOKU["status"] == "playing" and GOMOKU["pending_action"] is None:
                    time_left = max(0, int(GOMOKU["turn_time_limit"] - (time.time() - GOMOKU["turn_start_time"])))
                    if time_left <= 0:
                        GOMOKU["status"] = "over"; GOMOKU["winner"] = "白棋" if GOMOKU["current_player"] == 1 else "黑棋"; GOMOKU["last_action_msg"] = f"⏰超时！{GOMOKU['winner']}胜利"
                else: time_left = 0
                self.send_json({"board": GOMOKU["board"], "current_player": GOMOKU["current_player"], "status": GOMOKU["status"], "winner": GOMOKU["winner"], "time_left": time_left, "undo_left": GOMOKU["undo_left"], "draw_left": GOMOKU["draw_left"], "pending_action": GOMOKU["pending_action"], "requester": GOMOKU["requester"], "last_action_msg": GOMOKU["last_action_msg"], "players": GOMOKU["players"], "match_ready": GOMOKU["match_ready"], "play_ready": GOMOKU["play_ready"], "roles": GOMOKU["roles"]})
        else:
            try:
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers()
                with open(os.path.join(BASE_DIR, 'index.html'), 'rb') as f: self.wfile.write(f.read())
            except (BrokenPipeError, ConnectionResetError): pass
    def do_POST(self):
        l = int(self.headers['Content-Length']); raw = self.rfile.read(l)
        if self.path == '/upload_avatar':
            try:
                with open(AVATAR_FILE, 'wb') as f: f.write(base64.b64decode(raw.decode('utf-8').split(',')[1]))
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/profile/update':
            try:
                json.dump(json.loads(raw), open(PROFILE_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/forum/post':
            try:
                data = json.loads(raw); posts = json.load(open(FORUM_FILE, 'r', encoding='utf-8'))
                posts.insert(0, {"content": data['content'], "time": datetime.datetime.now().strftime("%m月%d日 %H:%M")})
                json.dump(posts, open(FORUM_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/music/upload':
            try:
                data = json.loads(raw); cat = data.get('category', '未分类').strip(); cat_dir = os.path.join(MUSIC_DIR, cat)
                if not os.path.exists(cat_dir): os.makedirs(cat_dir)
                safe_name = "".join([c for c in data['name'] if c.isalnum() or c in "._-()[] "])
                if not safe_name.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')): safe_name += ".mp3"
                with open(os.path.join(cat_dir, safe_name), 'wb') as f: f.write(base64.b64decode(data['data'].split(',')[1]))
                self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/ai/start':
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({"status": "cloud_ready"}).encode())
        elif self.path == '/api/join':
            try:
                client_id = json.loads(raw).get("client_id")
                with gomoku_lock:
                    if GOMOKU["players"]["p1"] is None: GOMOKU["players"]["p1"] = client_id; role = "p1"
                    elif GOMOKU["players"]["p1"] == client_id: role = "p1"
                    elif GOMOKU["players"]["p2"] is None: GOMOKU["players"]["p2"] = client_id; role = "p2"
                    elif GOMOKU["players"]["p2"] == client_id: role = "p2"
                    else: role = "spectator"
                    if GOMOKU["players"]["p1"] and GOMOKU["players"]["p2"] and GOMOKU["status"] == "waiting":
                        GOMOKU["status"] = "ready_match"; GOMOKU["last_action_msg"] = "双方已连接，请点击开始游戏！"
                    self.send_json({"role": role, "status": GOMOKU["status"]})
            except Exception as e: self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        elif self.path == '/api/action':
            try:
                data = json.loads(raw); role = data.get("role"); action = data.get("action")
                with gomoku_lock:
                    if action == "reset":
                        GOMOKU["board"] = [[0]*15 for _ in range(15)]
                        GOMOKU["current_player"] = 0
                        GOMOKU["status"] = "ready_match" if GOMOKU["players"]["p1"] and GOMOKU["players"]["p2"] else "waiting"
                        GOMOKU["winner"] = None; GOMOKU["move_count"] = 0; GOMOKU["last_move"] = None
                        GOMOKU["undo_left"] = {"black": 3, "white": 3}; GOMOKU["draw_left"] = {"black": 3, "white": 3}
                        GOMOKU["pending_action"] = None; GOMOKU["requester"] = None
                        GOMOKU["match_ready"] = {"p1": False, "p2": False}; GOMOKU["play_ready"] = {"p1": False, "p2": False}
                        GOMOKU["roles"] = {"p1": None, "p2": None}; GOMOKU["last_action_msg"] = "游戏已重置，请重新点击开始游戏！"
                        return self.send_json({"status": "ok"})
                    if action == "ready_match":
                        if GOMOKU["status"] == "ready_match":
                            GOMOKU["match_ready"][role] = True
                            if all(GOMOKU["match_ready"].values()):
                                roles = ["black", "white"]; random.shuffle(roles)
                                GOMOKU["roles"] = {"p1": roles[0], "p2": roles[1]}
                                GOMOKU["status"] = "ready_play"; GOMOKU["last_action_msg"] = "身份已分配，请双方点击准备就绪！"
                        return self.send_json({"status": "ok"})
                    if action == "ready_play":
                        if GOMOKU["status"] == "ready_play":
                            GOMOKU["play_ready"][role] = True
                            if all(GOMOKU["play_ready"].values()):
                                GOMOKU["status"] = "playing"; GOMOKU["current_player"] = 1
                                GOMOKU["turn_start_time"] = time.time(); GOMOKU["last_action_msg"] = "对弈开始，黑棋先手！"
                        return self.send_json({"status": "ok"})
                    if GOMOKU["status"] != "playing": return self.send_json({"error": "游戏未开始或已结束"})
                    my_role = GOMOKU["roles"].get(role)
                    if my_role is None: return self.send_json({"error": "身份未分配或已重置，请等待另一方重连"})
                    if my_role != ("black" if GOMOKU["current_player"] == 1 else "white"): return self.send_json({"error": "未轮到你操作"})
                    if action in ["agree", "reject"]:
                        if GOMOKU["pending_action"] is None: return self.send_json({"error": "没有待处理请求"})
                        if action == "agree":
                            if GOMOKU["pending_action"] == "undo":
                                if GOMOKU["last_move"]:
                                    x, y = GOMOKU["last_move"]; GOMOKU["board"][y][x] = 0
                                    GOMOKU["current_player"] = 1 if GOMOKU["current_player"] == 2 else 2
                                    GOMOKU["move_count"] -= 1
                                    if GOMOKU["requester"] in GOMOKU["undo_left"]: GOMOKU["undo_left"][GOMOKU["requester"]] -= 1
                                    GOMOKU["last_action_msg"] = f"{GOMOKU['requester']} 悔棋成功"
                            elif GOMOKU["pending_action"] == "draw":
                                GOMOKU["status"] = "over"; GOMOKU["winner"] = "和棋"
                                if GOMOKU["requester"] in GOMOKU["draw_left"]: GOMOKU["draw_left"][GOMOKU["requester"]] -= 1
                                GOMOKU["last_action_msg"] = "双方同意和棋"
                            GOMOKU["pending_action"] = None; GOMOKU["requester"] = None
                            GOMOKU["turn_start_time"] = time.time() - (GOMOKU["turn_time_limit"] - GOMOKU.get("paused_time_left", 30))
                        else:
                            GOMOKU["last_action_msg"] = "对方拒绝了请求"; GOMOKU["pending_action"] = None; GOMOKU["requester"] = None
                            GOMOKU["turn_start_time"] = time.time() - (GOMOKU["turn_time_limit"] - GOMOKU.get("paused_time_left", 30))
                        return self.send_json({"status": "ok"})
                    if action == "undo":
                        if GOMOKU["undo_left"].get(my_role, 0) <= 0: return self.send_json({"error": "次数已用完"})
                        GOMOKU["paused_time_left"] = max(0, int(GOMOKU["turn_time_limit"] - (time.time() - GOMOKU["turn_start_time"])))
                        GOMOKU["pending_action"] = "undo"; GOMOKU["requester"] = my_role; GOMOKU["last_action_msg"] = f"{my_role} 请求悔棋"
                        return self.send_json({"status": "ok"})
                    if action == "draw":
                        if GOMOKU["draw_left"].get(my_role, 0) <= 0: return self.send_json({"error": "次数已用完"})
                        GOMOKU["paused_time_left"] = max(0, int(GOMOKU["turn_time_limit"] - (time.time() - GOMOKU["turn_start_time"])))
                        GOMOKU["pending_action"] = "draw"; GOMOKU["requester"] = my_role; GOMOKU["last_action_msg"] = f"{my_role} 请求和棋"
                        return self.send_json({"status": "ok"})
                    if action == "place":
                        x = data.get("x"); y = data.get("y")
                        if x is None or y is None or x < 0 or x >= 15 or y < 0 or y >= 15 or GOMOKU["board"][y][x] != 0: return self.send_json({"error": "位置无效"})
                        player_num = 1 if my_role == "black" else 2
                        GOMOKU["board"][y][x] = player_num; GOMOKU["last_move"] = (x, y); GOMOKU["move_count"] += 1
                        if check_win(x, y, player_num):
                            GOMOKU["status"] = "over"; GOMOKU["winner"] = "黑棋" if my_role == "black" else "白棋"; GOMOKU["last_action_msg"] = f"{GOMOKU['winner']} 胜利！"; return self.send_json({"status": "ok"})
                        if GOMOKU["move_count"] == 225:
                            GOMOKU["status"] = "over"; GOMOKU["winner"] = "和棋"; GOMOKU["last_action_msg"] = "棋盘已满，和棋"; return self.send_json({"status": "ok"})
                        GOMOKU["current_player"] = 2 if my_role == "black" else 1; GOMOKU["turn_start_time"] = time.time(); return self.send_json({"status": "ok"})
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_response(500); self.send_header('Content-Type', 'application/json'); self.end_headers()
                self.wfile.write(json.dumps({"error": f"后端异常: {str(e)}"}).encode())
        elif self.path == '/chat':
            data = json.loads(raw); is_owner = data.get('isOwner', False)
            if not CHAT_SEMAPHORE.acquire(timeout=5): return self.send_json({"reply": "AI 正在被别人占用，请稍后再试~"})
            try:
                prompt_text = "你是芊茗静语的专属AI伙伴。芊茗静语是一个跨性别女性。你说话要温柔、真诚、可爱，一定要记得她的名字，让她感到温暖和陪伴。请用简短的话回答，不要废话。" if is_owner else "你是一个客观、中立的通用AI助手。请保持礼貌、专业、简洁地回答问题。"
                payload = {"model": CLOUD_MODEL_NAME, "messages": [{"role": "user", "content": prompt_text + "\n用户：" + data['message']}], "temperature": 0.7, "max_tokens": 256}
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {CLOUD_API_KEY}"}
                r = requests.post(CLOUD_API_URL, headers=headers, json=payload, timeout=60).json()
                reply = r['choices'][0]['message']['content']
            except Exception as e:
                print(f"云端调用错误: {e}"); reply = "云端AI连接失败，请检查API密钥、地址或网络代理。"
            finally: CHAT_SEMAPHORE.release()
            self.send_json({"reply": reply})
if __name__ == '__main__':
    print("🔥 静语的专属空间后端服务器（完整版）已启动！")
    ThreadingHTTPServer(('0.0.0.0', 8001), AI).serve_forever()
