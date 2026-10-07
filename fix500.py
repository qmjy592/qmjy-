import os
p = os.path.expanduser('~/portal_project/my_ultimate_portal.py')
c = open(p, 'r', encoding='utf-8').read()

old = '''except Exception as e:
                    self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())'''
new = '''except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": f"后端异常: {str(e)}"}).encode())'''

c = c.replace(old, new)
open(p, 'w', encoding='utf-8').write(c)
print("✅ 异常捕获已升级！")
