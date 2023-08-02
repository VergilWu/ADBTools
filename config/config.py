# -*- coding:utf-8 -*-
from utils.systemer import get_abs_path, mkdir

# 绝对路径
LOGCAT_PATH = get_abs_path("logcat")  # 日志路径
SCREEN_PATH = get_abs_path("screen")  # 截图路径
FASTBOT_PATH = get_abs_path("config/fastbot")

# 使用 pyinstall 打包，必须使用绝对路径才能显示出图片来
APP_ICON = get_abs_path("favicon.ico")  # APP ICON
APP_NAME = "移动测试工具"  # APP 名称
APP_VERSION = "0.1.1"  # APP 版本
APP_DESCRIPTION = "用 PyQt5 编写的桌面工具应用程序，封装了移动端测试常用功能（adb、tidevice、fastbot）"  # APP 描述

mkdir(LOGCAT_PATH)
mkdir(SCREEN_PATH)

# fastbot 填写待测包名
PKG_NAME = [
    "com.example.application",
]

# 删除文件夹名称列表
DEL_FOLDER_NAME = [
    "baidu",
]

# prop key
PROP_KEY = [
    "ro.product.brand",
    "ro.product.model",
    "ro.product.name",
    "ro.build.version.release",
    "ro.build.version.sdk",
]

# 执行 fastbot 事件间隔
THROTTLE_LIST = [
    '100',
    '200',
    '300',
    '400',
    '500',
]

# 选取路径的用途
PATH_USE_INSTALL = 'install'
PATH_USE_TRANSFER = 'transfer'
