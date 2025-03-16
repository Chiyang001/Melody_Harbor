import os
import json

# 用户数据存储路径
USER_DATA_DIR = r"D:\Website_Data\users"
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

def register_user(username, password):
    """
    注册新用户
    :param username: 用户名
    :param password: 密码
    :return: 注册成功返回True，失败返回False
    """
    user_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    if os.path.exists(user_file):
        return False
    user_data = {
        "username": username,
        "password": password
    }
    with open(user_file, "w") as f:
        json.dump(user_data, f)
    return True

def login_user(username, password):
    """
    用户登录
    :param username: 用户名
    :param password: 密码
    :return: 登录成功返回True，失败返回False
    """
    user_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    if not os.path.exists(user_file):
        return False
    with open(user_file, "r") as f:
        user_data = json.load(f)
    return user_data["password"] == password
