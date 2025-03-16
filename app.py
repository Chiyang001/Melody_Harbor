# 音乐分享平台/app.py
from flask import Flask, render_template, request, redirect, session
from user_manager import register_user, login_user
from music_manager import upload_music, get_all_music_info, delete_music, like_music

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def index():
    if "username" not in session:
        return redirect("/login")
    music_list = get_all_music_info()
    return render_template("index.html", music_list=music_list)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if register_user(username, password):
            return redirect("/login")
        else:
            return "用户名已存在。"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if login_user(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return "用户名或密码无效。"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect("/login")
    if request.method == "POST":
        file = request.files["file"]
        title = request.form.get("title")
        artist = request.form.get("artist")
        lyrics = request.form.get("lyrics")
        cover_file = request.files.get("cover")
        username = session["username"]
        if upload_music(file, title, artist, username, lyrics, cover_file):
            return redirect("/")
        else:
            return "上传失败，请检查文件格式。"
    return render_template("upload.html")

@app.route("/delete_music/<filename>")
def delete(filename):
    if "username" not in session:
        return redirect("/login")
    username = session["username"]
    if delete_music(filename, username):
        return redirect("/")
    else:
        return "删除失败。"

@app.route("/like_music/<filename>")
def like(filename):
    if "username" not in session:
        return redirect("/login")
    if like_music(filename):
        return redirect("/")
    else:
        return "点赞失败。"

if __name__ == "__main__":
    app.run(debug=True)
