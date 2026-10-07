import os

base_dir = os.path.expanduser('~/portal_project/music')
# 需要删除的文件
to_delete = ['song2.mp3', 'song4.mp3']
# 需要重命名的文件和新的名字
to_rename = {'song1.mp3': '春風とアルメリア(feat.花隈千冬).mp3'}

found_files = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file in to_delete or file in to_rename:
            found_files.append(os.path.join(root, file))

if not found_files:
    print("❌ 没在 music 文件夹里找到 song1.mp3 / song2.mp3 / song4.mp3")
else:
    for filepath in found_files:
        filename = os.path.basename(filepath)
        if filename in to_delete:
            os.remove(filepath)
            print(f"✅ 已删除: {filepath}")
        elif filename in to_rename:
            new_name = to_rename[filename]
            new_path = os.path.join(os.path.dirname(filepath), new_name)
            # 如果新名字已经存在，先删掉旧的避免冲突
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(filepath, new_path)
            print(f"✅ 已重命名: {filepath} -> {new_path}")
    print("🎵 音乐盒清理完毕！刷新网页即可看到新列表。")
