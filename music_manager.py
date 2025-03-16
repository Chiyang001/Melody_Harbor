import os
import json
from PIL import Image

# 音乐数据存储路径，确保这些路径是 static 目录的子目录
MUSIC_DATA_DIR = r"static/music"
COVER_DATA_DIR = r"static/music_covers"
if not os.path.exists(MUSIC_DATA_DIR):
    os.makedirs(MUSIC_DATA_DIR)
if not os.path.exists(COVER_DATA_DIR):
    os.makedirs(COVER_DATA_DIR)

ALLOWED_MUSIC_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_music(file, title, artist, username, lyrics=None, cover_file=None):
    """
    上传音乐文件并保存相关信息
    :param file: 音乐文件对象
    :param title: 音乐标题
    :param artist: 音乐艺术家
    :param username: 上传者用户名
    :param lyrics: 音乐歌词
    :param cover_file: 音乐封面文件对象
    :return: 上传成功返回True，失败返回False
    """
    if not allowed_file(file.filename, ALLOWED_MUSIC_EXTENSIONS):
        return False
    try:
        music_filename = f"{title}_{artist}.{file.filename.rsplit('.', 1)[1].lower()}"
        music_path = os.path.join(MUSIC_DATA_DIR, music_filename)
        file.save(music_path)

        cover_filename = None
        if cover_file:
            if allowed_file(cover_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                cover_filename = f"{title}_{artist}.{cover_file.filename.rsplit('.', 1)[1].lower()}"
                cover_path = os.path.join(COVER_DATA_DIR, cover_filename)
                cover_file.save(cover_path)
                # 裁剪图片到合适大小
                with Image.open(cover_path) as img:
                    img.thumbnail((100, 100))
                    img.save(cover_path)

        music_info = {
            "title": title,
            "artist": artist,
            "username": username,
            "filename": music_filename,
            "lyrics": lyrics,
            "cover_filename": cover_filename,
            "likes": 0
        }
        info_filename = f"{title}_{artist}.json"
        info_path = os.path.join(MUSIC_DATA_DIR, info_filename)
        with open(info_path, "w") as f:
            json.dump(music_info, f)
        return True
    except Exception as e:
        print(f"Upload error: {e}")
        return False

def get_all_music_info():
    """
    获取所有音乐的信息
    :return: 包含所有音乐信息的列表
    """
    music_info_list = []
    for filename in os.listdir(MUSIC_DATA_DIR):
        if filename.endswith(".json"):
            info_path = os.path.join(MUSIC_DATA_DIR, filename)
            with open(info_path, "r") as f:
                music_info = json.load(f)
                music_info_list.append(music_info)
    return music_info_list

def delete_music(filename, username):
    """
    删除指定用户上传的音乐
    :param filename: 音乐文件名
    :param username: 用户名
    :return: 删除成功返回True，失败返回False
    """
    info_filename = filename.rsplit('.', 1)[0] + '.json'
    info_path = os.path.join(MUSIC_DATA_DIR, info_filename)
    if os.path.exists(info_path):
        with open(info_path, "r") as f:
            music_info = json.load(f)
        if music_info["username"] == username:
            music_path = os.path.join(MUSIC_DATA_DIR, music_info["filename"])
            if os.path.exists(music_path):
                os.remove(music_path)
            # 检查 cover_filename 键是否存在
            if "cover_filename" in music_info and music_info["cover_filename"]:
                cover_path = os.path.join(COVER_DATA_DIR, music_info["cover_filename"])
                if os.path.exists(cover_path):
                    os.remove(cover_path)
            os.remove(info_path)
            return True
    return False

def like_music(filename):
    info_filename = filename.rsplit('.', 1)[0] + '.json'
    info_path = os.path.join(MUSIC_DATA_DIR, info_filename)
    if os.path.exists(info_path):
        with open(info_path, "r") as f:
            music_info = json.load(f)
        music_info["likes"] += 1
        with open(info_path, "w") as f:
            json.dump(music_info, f)
        return True
    return False
