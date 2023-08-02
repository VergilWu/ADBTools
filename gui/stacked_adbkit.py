# -*- coding:utf-8 -*-
import functools
import logging
import os
import subprocess
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from adbutils import adb

from config import qss_cfg, config
from gui.dialog import DiaLog, Notice
from utils import common
from utils import systemer
from utils.adbkit import AdbKit


def check_device(func):
    """设备检测，判断仅有设备时继续执行"""

    @functools.wraps(func)
    def wrapper(*args, **kw):
        if len(AdbKit.device_list()) == 0:
            Notice().error("当前设备为空，AdbKit 初始化失败！")
            return
        return func(*args, **kw)

    return wrapper


class AdbKitPage:
    def __init__(self):
        self.widget = QWidget()  # 创建页面布局
        self.widget.setObjectName('right_widget')
        self.widget.setStyleSheet(qss_cfg.RIGHT_STYLE)  # 设置右侧部件美化

        self.layout = QVBoxLayout(self.widget)
        self.dialog = DiaLog(self.widget)
        self.notice = Notice()

        self.init_ui()
        self.add_event()

    def init_ui(self):
        """设备选择区域"""
        self.label_device_choose = QLabel("请选择设备：")
        self.label_device_choose.setFont(QFont("Microsoft YaHei UI"))

        self.cmb_device_choose = QComboBox()
        self.cmb_device_choose.setFixedSize(200, 30)
        self.cmb_device_choose.addItems(AdbKit.device_list())  # 下拉框添加数据

        self.btn_refresh_device = QPushButton('刷新')
        self.btn_refresh_device.setFixedSize(40, 20)
        self.btn_refresh_device.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)

        self.layout_device_choose = QHBoxLayout()
        self.layout_device_choose.addWidget(self.label_device_choose)
        self.layout_device_choose.addWidget(self.cmb_device_choose)
        self.layout_device_choose.addWidget(self.btn_refresh_device)
        self.layout_device_choose.addStretch(1)

        """按钮区域"""
        # 标签
        self.label_device = QLabel("设备操作")
        self.label_device.setObjectName('right_label')
        self.layout.addWidget(self.label_device)

        # 设备信息
        self.btn_device_info = QPushButton('设备信息')
        self.btn_wifi_connect = QPushButton('无线连接')
        self.btn_kill_adb = QPushButton('Kill adbd')

        self.edit_ip = QLineEdit()
        self.edit_port = QLineEdit()
        self.edit_ip.setPlaceholderText('IP')
        self.edit_port.setPlaceholderText('5555')
        self.edit_port.setFixedSize(50, 25)
        self.edit_ip.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_port.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_ip.setInputMask('000.000.000.000;')  # 校验 IP
        self.edit_port.setInputMask('00000;')
        self.edit_port.setMaxLength(5)  # 最大为5位

        self.btn_device_info.setFixedSize(100, 30)
        self.btn_wifi_connect.setFixedSize(100, 30)
        self.btn_kill_adb.setFixedSize(100, 30)

        self.btn_device_info.setStyleSheet(qss_cfg.BTN_COLOR_GREEN_NIGHT)
        self.btn_wifi_connect.setStyleSheet(qss_cfg.BTN_COLOR_GREEN_NIGHT)
        self.btn_kill_adb.setStyleSheet(qss_cfg.BTN_COLOR_GREEN_NIGHT)

        layout_00 = QHBoxLayout()
        layout_00.addWidget(self.btn_device_info)
        layout_00.addWidget(self.btn_kill_adb)
        layout_00.addWidget(self.btn_wifi_connect)
        layout_00.addWidget(self.edit_ip)
        layout_00.addWidget(QLabel(":"))
        layout_00.addWidget(self.edit_port)
        layout_00.addStretch(1)

        # 手机代理
        self.btn_open_proxy = QPushButton('开启代理')
        self.btn_close_proxy = QPushButton('关闭代理')
        self.edit_hostname_port = QLineEdit()
        self.edit_hostname_port.setPlaceholderText('hostname:port')
        self.edit_hostname_port.setFixedSize(200, 25)
        self.edit_hostname_port.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_port.setMaxLength(20)  # 最大为5位

        layout_proxy = QHBoxLayout()
        layout_proxy.addWidget(self.btn_open_proxy)
        layout_proxy.addWidget(self.btn_close_proxy)
        layout_proxy.addWidget(self.edit_hostname_port)
        layout_proxy.addStretch(1)

        # 安装APK
        self.btn_install = QPushButton('安装应用')
        self.btn_choose_apk = QPushButton('选择APK')
        self.btn_choose_dir = QPushButton('选择文件夹')
        self.btn_qrcode = QPushButton('生成二维码')
        self.edit_apk_path = QLineEdit()

        self.edit_apk_path.setPlaceholderText('请粘贴安装包下载链接 或 选择路径～')
        self.edit_apk_path.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_apk_path.setFixedSize(300, 25)

        self.btn_install.setToolTip('复制需要安装的「 APK URL 」点击文本框。\n安装过程见IDE内的 DEBUG 日志。')
        self.btn_choose_apk.setFixedSize(90, 20)
        self.btn_choose_dir.setFixedSize(90, 20)
        self.btn_qrcode.setFixedSize(100, 20)

        self.btn_install.setStyleSheet(qss_cfg.BTN_COLOR_GREEN)
        self.btn_choose_apk.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)
        self.btn_choose_dir.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)
        self.btn_qrcode.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)

        layout_01 = QHBoxLayout()
        layout_01.addWidget(self.btn_install)
        layout_01.addWidget(self.edit_apk_path)
        layout_01.addWidget(self.btn_choose_apk)
        layout_01.addWidget(self.btn_choose_dir)
        layout_01.addWidget(self.btn_qrcode)
        layout_01.addStretch(1)

        # 打开网页
        self.btn_open_browser = QPushButton('打开网页')

        self.edit_open_url = QLineEdit()
        self.edit_open_url.setFixedSize(500, 25)
        self.edit_open_url.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_open_url.setPlaceholderText('请输入链接')

        layout_02 = QHBoxLayout()
        layout_02.addWidget(self.btn_open_browser)
        layout_02.addWidget(self.edit_open_url)
        layout_02.addStretch(1)

        # 发送文本
        self.btn_send_text = QPushButton('发送文本')
        self.btn_send_text.setToolTip('不支持中文')

        self.edit_send_text = QLineEdit()
        self.edit_send_text.setFixedSize(500, 25)
        self.edit_send_text.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_send_text.setPlaceholderText('请输入内容')

        layout_03 = QHBoxLayout()
        layout_03.addWidget(self.btn_send_text)
        layout_03.addWidget(self.edit_send_text)
        layout_03.addStretch(1)

        # 删除设备上的指定文件夹
        self.btn_del_folder = QPushButton('删除文件夹')
        self.btn_insert = QPushButton('添加')
        self.btn_delete = QPushButton('删除')

        self.btn_insert.setFixedSize(70, 20)
        self.btn_delete.setFixedSize(70, 20)
        self.btn_insert.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)
        self.btn_delete.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)

        self.edit_insert_folder = QLineEdit()
        self.edit_insert_folder.setFixedSize(100, 20)
        self.edit_insert_folder.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)

        self.combox_choose_folder = QComboBox()  # 设置文件下拉框
        self.combox_choose_folder.setFixedSize(150, 30)
        self.combox_choose_folder.addItems(config.DEL_FOLDER_NAME)  # 添加数据到下拉框

        layout_04 = QHBoxLayout()
        layout_04.addWidget(self.btn_del_folder)
        layout_04.addWidget(self.combox_choose_folder)
        layout_04.addWidget(self.btn_delete)
        layout_04.addWidget(self.btn_insert)
        layout_04.addWidget(self.edit_insert_folder)
        layout_04.addStretch(1)

        # 文件传输操作
        self.btn_pull = QPushButton('拉取文件')
        self.btn_pull.setToolTip('拉取文件到电脑')

        self.btn_push = QPushButton('推送文件')
        self.btn_push.setToolTip('推送文件到设备')

        self.edit_device_path = QLineEdit()
        self.edit_device_path.setFixedSize(150, 25)
        self.edit_device_path.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_device_path.setPlaceholderText('请输入设备路径')

        self.edit_local_path = QLineEdit()
        self.edit_local_path.setFixedSize(150, 25)
        self.edit_local_path.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_local_path.setPlaceholderText('请输入本地路径')

        self.btn_choose_path_transfer = QPushButton('选择本地路径')
        self.btn_choose_path_transfer.setFixedSize(100, 20)
        self.btn_choose_path_transfer.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)

        layout_10 = QHBoxLayout()
        layout_10.addWidget(self.btn_pull)
        layout_10.addWidget(self.btn_push)
        layout_10.addWidget(self.edit_device_path)
        layout_10.addWidget(self.edit_local_path)
        layout_10.addWidget(self.btn_choose_path_transfer)
        layout_10.addStretch(1)

        # 动态设置 prop 参数
        self.btn_get_prop = QPushButton('获取prop')
        self.btn_get_prop.setToolTip('获取prop参数')
        self.btn_set_prop = QPushButton('设置prop')
        self.btn_set_prop.setToolTip('设置prop参数，重启后生效')

        self.btn_set_prop.setFixedSize(70, 20)

        self.combox_choose_prop_key = QComboBox()  # 设置prop key下拉框
        self.combox_choose_prop_key.setFixedSize(250, 30)
        self.combox_choose_prop_key.addItems(config.PROP_KEY)  # 添加prop key到下拉框

        self.edit_prop_value = QLineEdit()  # 设置prop value输入框
        self.edit_prop_value.setFixedSize(100, 20)
        self.edit_prop_value.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)

        layout_09 = QHBoxLayout()
        layout_09.addWidget(self.btn_get_prop)
        layout_09.addWidget(self.btn_set_prop)
        layout_09.addWidget(self.combox_choose_prop_key)
        layout_09.addWidget(self.edit_prop_value)
        layout_09.addStretch(1)

        # 针对当前包的操作
        self.btn_get_package_info = QPushButton('应用包详情')
        self.btn_get_package_name = QPushButton('应用包名')
        self.btn_reset_app = QPushButton('重置当前应用')
        self.btn_uninstall_app = QPushButton('卸载当前应用')

        layout_05 = QHBoxLayout()
        layout_05.addWidget(self.btn_get_package_info)
        layout_05.addWidget(self.btn_get_package_name)
        layout_05.addWidget(self.btn_reset_app)
        layout_05.addWidget(self.btn_uninstall_app)
        layout_05.addStretch(1)

        # 滑动操作 line 6
        self.btn_swipe_up = QPushButton('上滑')
        self.btn_swipe_down = QPushButton('下滑')
        self.btn_swipe_left = QPushButton('左滑')
        self.btn_swipe_right = QPushButton('右滑')
        self.btn_swipe_stop = QPushButton('停止')

        self.check_box = QCheckBox('是否连续')  # 复选框

        self.btn_swipe_stop.setFixedSize(70, 20)
        self.btn_swipe_stop.setStyleSheet(qss_cfg.BTN_COLOR_YELLOW)

        layout_06 = QHBoxLayout()
        layout_06.addWidget(self.btn_swipe_up)
        layout_06.addWidget(self.btn_swipe_down)
        layout_06.addWidget(self.btn_swipe_left)
        layout_06.addWidget(self.btn_swipe_right)
        layout_06.addWidget(self.check_box)
        layout_06.addWidget(self.btn_swipe_stop)
        layout_06.addStretch(1)

        # 获取日志 line 7
        self.btn_clear_log = QPushButton('清空日志')
        self.btn_logcat = QPushButton('获取日志')
        self.btn_open_log_path = QPushButton('打开目录')

        self.edit_logcat_filename = QLineEdit()
        self.edit_logcat_filename.setFixedSize(275, 25)
        self.edit_logcat_filename.setStyleSheet(qss_cfg.TEXT_EDIT_STYLE)
        self.edit_logcat_filename.setPlaceholderText('日志名称（获取成功后在该处展示名称）')
        self.edit_logcat_filename.setReadOnly(True)

        layout_07 = QHBoxLayout()
        layout_07.addWidget(self.btn_clear_log)
        layout_07.addWidget(self.btn_logcat)
        layout_07.addWidget(self.btn_open_log_path)
        layout_07.addWidget(self.edit_logcat_filename)
        layout_07.addStretch(1)

        # 截图 line 8
        self.btn_screenshot = QPushButton('截图')
        self.btn_open_screenshot = QPushButton('打开截图')
        self.btn_open_screenshot_dir = QPushButton('打开目录')

        layout_08 = QHBoxLayout()
        layout_08.addWidget(self.btn_screenshot)
        layout_08.addWidget(self.btn_open_screenshot)
        layout_08.addWidget(self.btn_open_screenshot_dir)
        layout_08.addStretch(1)

        """设置页面通用按钮大小和颜色"""
        btn_list = [
            self.btn_install,
            self.btn_open_browser,
            self.btn_send_text,
            self.btn_del_folder,
            self.btn_get_package_info, self.btn_get_package_name,
            self.btn_swipe_up, self.btn_swipe_down, self.btn_swipe_left, self.btn_swipe_right,
            self.btn_clear_log, self.btn_logcat, self.btn_open_log_path,
            self.btn_screenshot, self.btn_open_screenshot, self.btn_open_screenshot_dir,
            self.btn_open_proxy, self.btn_close_proxy, self.btn_get_prop, self.btn_set_prop,
            self.btn_pull, self.btn_push,
        ]
        btn_list_2 = [self.btn_reset_app, self.btn_uninstall_app]
        for btn in btn_list:
            btn.setFixedSize(100, 30)
            btn.setStyleSheet(qss_cfg.BTN_COLOR_GREEN_NIGHT)
        for btn in btn_list_2:
            btn.setFixedSize(120, 30)
            btn.setStyleSheet(qss_cfg.BTN_COLOR_GREEN_NIGHT)

        '''添加各部件到主布局'''
        self.layout.addStretch(2)
        self.layout.addLayout(self.layout_device_choose)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label_device)
        self.layout.addLayout(layout_00)  # 设备信息
        self.layout.addLayout(layout_proxy)  # 设置代理
        self.layout.addLayout(layout_01)  # 安装
        self.layout.addLayout(layout_05)  # 获取信息
        self.layout.addLayout(layout_04)  # 删除文件夹
        self.layout.addLayout(layout_10)  # 文件传输
        self.layout.addLayout(layout_09)  # 设置prop属性
        self.layout.addLayout(layout_02)  # 打开网页
        self.layout.addLayout(layout_03)  # 发送文本
        self.layout.addLayout(layout_07)  # 清空日志
        self.layout.addLayout(layout_08)  # 截图
        self.layout.addLayout(layout_06)  # 滑动
        self.layout.addStretch(2)

    def add_event(self):
        # 设备选择框
        self.cmb_device_choose.currentIndexChanged.connect(lambda: self.current_device())
        self.btn_refresh_device.clicked.connect(lambda: self.clicked_devices_check())

        # 设备信息 无线连接
        self.btn_device_info.clicked.connect(lambda: self.clicked_get_device_info())
        self.btn_wifi_connect.clicked.connect(lambda: self.clicked_connect_wifi())
        self.btn_kill_adb.clicked.connect(lambda: self.clicked_server_kill())

        # 设置代理
        self.btn_open_proxy.clicked.connect(lambda: self.clicked_open_proxy())
        self.btn_close_proxy.clicked.connect(lambda: self.clicked_close_proxy())

        # 安装应用
        self.btn_install.clicked.connect(lambda: self.clicked_btn_install())
        self.btn_choose_apk.clicked.connect(lambda: self.clicked_btn_choose_local_path(True, config.PATH_USE_INSTALL))
        self.btn_choose_dir.clicked.connect(lambda: self.clicked_btn_choose_local_path(False, config.PATH_USE_INSTALL))
        self.btn_qrcode.clicked.connect(lambda: self.clicked_btn_qrcode())

        # 打开网页
        self.btn_open_browser.clicked.connect(lambda: self.clicked_btn_open_browser())

        # 发送文本
        self.btn_send_text.clicked.connect(lambda: self.clicked_btn_send_text())

        # 删除文件夹
        self.btn_del_folder.clicked.connect(lambda: self.clicked_btn_del_folder())
        self.btn_delete.clicked.connect(lambda: self.clicked_btn_delete())
        self.btn_insert.clicked.connect(lambda: self.clicked_btn_insert())

        # 文件传输
        self.btn_pull.clicked.connect(lambda: self.clicked_btn_pull_or_push(True))
        self.btn_push.clicked.connect(lambda: self.clicked_btn_pull_or_push(False))
        self.btn_choose_path_transfer.clicked.connect(
            lambda: self.clicked_btn_choose_local_path(True, config.PATH_USE_TRANSFER))

        # 获取/设置prop属性
        self.btn_get_prop.clicked.connect(lambda: self.clicked_btn_get_prop())
        self.btn_set_prop.clicked.connect(lambda: self.clicked_btn_set_prop())

        # 设备相关的其他操作 - 获取包名版本号等
        self.btn_get_package_info.clicked.connect(lambda: self.clicked_btn_get_pkg_info())
        self.btn_get_package_name.clicked.connect(lambda: self.clicked_btn_get_package_name())
        self.btn_reset_app.clicked.connect(lambda: self.clicked_btn_reset_current_app())
        self.btn_uninstall_app.clicked.connect(lambda: self.clicked_btn_uninstall_current_app())

        # 日志操作
        self.btn_clear_log.clicked.connect(lambda: self.clicked_btn_logcat_c())
        self.btn_logcat.clicked.connect(lambda: self.clicked_btn_logcat())
        self.btn_open_log_path.clicked.connect(lambda: self.clicked_btn_open_log_path())

        # 截图
        self.btn_screenshot.clicked.connect(lambda: self.clicked_btn_screenshot())
        self.btn_open_screenshot.clicked.connect(lambda: self.clicked_btn_open_screenshot_path())
        self.btn_open_screenshot_dir.clicked.connect(lambda: self.clicked_btn_open_screenshot_dir())

        # 滑动
        self.btn_swipe_up.clicked.connect(lambda: self.clicked_btn_swipe2up())
        self.btn_swipe_down.clicked.connect(lambda: self.clicked_btn_swipe2down())
        self.btn_swipe_left.clicked.connect(lambda: self.clicked_btn_swipe2left())
        self.btn_swipe_right.clicked.connect(lambda: self.clicked_btn_swipe2right())
        self.btn_swipe_stop.clicked.connect(lambda: self.clicked_btn_swipe_stop())

    @check_device
    def adb(self):
        try:
            return AdbKit(self.current_device())
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)
            return None

    def current_device(self):
        """获取当前列表选中的设备"""
        try:
            device = self.cmb_device_choose.currentText()
            # logging.info(f"current device: {None if not device else device}")
            return device
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)
            return None

    def clicked_devices_check(self):
        """刷新设备列表"""
        try:
            devices_list = AdbKit.device_list()
            self.cmb_device_choose.clear()
            self.cmb_device_choose.addItems(devices_list)
            self.cmb_device_choose.setCurrentIndex(0)
            logging.info(f"Device checking... Now device list: {devices_list}")
            # self.dialog.info(f"Now device list: \n{devices_list}")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_get_device_info(self):
        """获取设备信息"""
        try:
            if self.adb():
                output = self.adb().device_info_complete()
                self.dialog.info(output)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_connect_wifi(self):
        # 首先获取 LineEdit 写入的值
        try:
            edit_ip_value = self.edit_ip.text()
            edit_port_value = self.edit_port.text()
            if edit_ip_value == '...':
                self.notice.error('请输入IP地址')
                return
            port = "5555" if not edit_port_value else edit_port_value
            # output = self.adb().connect(edit_ip_value, port)
            process = subprocess.Popen("adb connect %s:%s" % (edit_ip_value, port), shell=True, stdout=subprocess.PIPE)
            output = process.stdout.read().decode("utf-8")

            if "connected to %s:%s" % (edit_ip_value, port) in output:
                self.clicked_devices_check()
                self.edit_ip.setText(self.adb().ip())
            self.notice.info(output)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_server_kill(self):
        try:
            output = adb.server_kill()
            self.notice.info(f"success: adb server killed.")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_open_proxy(self):
        try:
            content = self.edit_hostname_port.text().strip()
            host, port = content.split(":") if content else (common.get_pc_ip(), 8888)

            if self.adb():
                self.adb().open_proxy(host, port)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_close_proxy(self):
        try:
            if self.adb():
                self.adb().close_proxy()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def get_apk_path_choose_text(self):
        """获取安装apk文本框的内容"""
        try:
            text = self.edit_apk_path.text().strip()
            if text:
                logging.info(f"安装链接：{text}")
                return self.edit_apk_path.text()
            raise ValueError
        except ValueError:
            self.notice.warn("给一下安装路径或链接呗～")
            logging.warning('安装路径或链接为空')
        except Exception as e:
            self.notice.error("完蛋了，走到异常分支了！")
            logging.error('获取 apk 文本框内容失败～ %s' % e)

    def clicked_btn_install(self):
        """点击 安装应用 按钮，如果路径为文件则直接安装，如果为文件夹则遍历目录下apk文件"""
        try:
            if self.adb() and self.get_apk_path_choose_text():
                selected_path = self.get_apk_path_choose_text()

                if os.path.isfile(selected_path):
                    self.thread_install_apk(selected_path, "")
                elif os.path.isdir(selected_path):
                    apk_files = [file for file in os.listdir(selected_path) if file.endswith('.apk')]
                    if len(apk_files) == 1:
                        self.thread_install_apk(selected_path, apk_files[0])
                    elif len(apk_files) > 1:
                        self.notice.warn(f"当前目录下存在多个apk文件，请选择一个安装！")
                        selected_apk = str(self.show_apk_selection_dialog(apk_files))
                        if selected_apk != "":
                            self.thread_install_apk(selected_path, selected_apk)
                    else:
                        self.notice.error(f"当前目录下不存在apk文件！")
                else:
                    self.notice.error(f"路径无效！")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def thread_install_apk(self, apk_path, apk_file):
        """安装apk"""
        try:
            t = threading.Thread(
                target=self.adb().install,
                args=(os.path.join(apk_path), apk_file)
            )
            t.start()
        except Exception as e:
            self.notice.error(f"安装失败\n{e}")

    def show_apk_selection_dialog(self, apk_files) -> str:
        """显示apk选择对话框"""
        try:
            selected_apk = ""
            dialog = QDialog()
            dialog.setWindowTitle("选择安装包")
            dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowMinMaxButtonsHint)
            dialog.setWindowIcon(QIcon('favicon.ico'))
            dialog.resize(300, 200)

            layout = QVBoxLayout(dialog)

            combo_box = QComboBox(dialog)
            layout.addWidget(combo_box)

            # 将 apk 文件添加到列表框
            for apk_file in apk_files:
                combo_box.addItems([apk_file])

            # 添加垂直间距
            layout.addSpacing(50)

            hbox = QHBoxLayout()

            # 添加左侧空白区域
            hbox.addStretch(1)

            # 添加按钮
            ok_button = QPushButton("确定", dialog)
            ok_button.clicked.connect(lambda: on_ok_button_click())
            hbox.addWidget(ok_button)

            # 添加右侧空白区域
            hbox.addStretch(1)

            # 添加水平布局
            layout.addLayout(hbox)

            def on_ok_button_click():
                nonlocal selected_apk
                selected_apk = combo_box.currentText()
                dialog.accept()

            dialog.exec_()
            return selected_apk

        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_choose_dir_path(self):
        """点击 选择文件夹 按钮，通过 文件夹 选择安装路径，"""
        try:
            open_path = QFileDialog()
            path = open_path.getExistingDirectory()
            self.edit_apk_path.setText(path)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_qrcode(self):
        """点击生成二维码"""
        text = self.get_apk_path_choose_text()
        if text:
            try:
                os.system(f'open {AdbKit().qr_code(text)}')
            except Exception:
                os.system(f'start explorer {AdbKit().qr_code(text)}')
        else:
            logging.info("文本为空，不生成二维码！")
            # self.notice.error("文本框内容为空，不生成二维码！")

    def clicked_btn_open_browser(self):
        """点击【打开网页】"""
        try:
            if self.adb():
                url = self.edit_open_url.text()
                logging.info(f"当前输入框内链接为：{None if not url else url}")
                if not url:
                    logging.info("打开网页：链接为空，请输入后再试...")
                    self.notice.error('不给链接怎么打的开呀～')
                    return
                # self.adb().start_web_page(url)
                self.adb().adb_device.open_browser(url)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_send_text(self):
        """点击【发送文本】"""
        try:
            if self.adb():
                text = self.edit_send_text.text().strip()
                if not text:
                    logging.info("输入文本：文本为空，请输入后再试...")
                    self.notice.warn('文本框得有内容的呀～')
                    return
                logging.info(f"当前文本输入框内容为：{text}")
                self.adb().adb_device.send_keys(text)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_del_folder(self):
        """点击【删除文件夹】"""
        try:
            if self.adb():
                folder_name = self.combox_choose_folder.currentText()
                self.adb().delete_folder(folder_name)
                logging.info(f"删除文件夹：{folder_name}")
                self.notice.info(f"删除文件夹成功：{folder_name}")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_pull_or_push(self, is_pull: bool):
        """文件传输操作"""
        try:
            if self.adb():
                device_path = self.edit_device_path.text()
                local_path = self.edit_local_path.text()
                if device_path and local_path:
                    if is_pull:
                        self.adb().pull(device_path, local_path)
                        logging.info(f"拉取文件：{device_path} -> {local_path}")
                        self.notice.info(f"拉取文件成功：{device_path} -> {local_path}")
                    else:
                        self.adb().push(local_path, device_path)
                        logging.info(f"推送文件：{local_path} -> {device_path}")
                        self.notice.info(f"推送文件成功：{local_path} -> {device_path}")
                else:
                    logging.info("请检查路径后再试...")
                    self.notice.warn('路径不能为空的呀～')
                    return
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_choose_local_path(self, is_file: bool, use: str):
        """点击【选择本地路径】"""
        try:
            open_path = QFileDialog()
            if is_file:
                if use == config.PATH_USE_INSTALL:
                    path = open_path.getOpenFileName(filter='APK Files(*.apk);;All Files(*)')
                elif use == config.PATH_USE_TRANSFER:
                    path = open_path.getOpenFileName(filter='All Files(*)')
            else:
                path = open_path.getExistingDirectory()

            if use == config.PATH_USE_INSTALL:
                if is_file:
                    self.edit_apk_path.setText(path[0])
                else:
                    self.edit_apk_path.setText(path)
            elif use == config.PATH_USE_TRANSFER:
                self.edit_local_path.setText(path)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_delete(self):
        """删除下拉框内的文件名称数据"""
        try:
            folder_name = self.combox_choose_folder.currentText()
            config.DEL_FOLDER_NAME.remove(folder_name)
            self.combox_choose_folder.clear()
            self.combox_choose_folder.addItems(config.DEL_FOLDER_NAME)
            logging.info(f"Delete folder name：{folder_name}")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_insert(self):
        """增加下拉框内的文件名称数据"""
        try:
            folder_name = self.edit_insert_folder.text()
            config.DEL_FOLDER_NAME.append(folder_name)
            self.combox_choose_folder.clear()
            self.combox_choose_folder.addItems(config.DEL_FOLDER_NAME)
            logging.info(f"Insert folder name：{folder_name}")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_get_prop(self):
        """点击【获取当前prop信息】"""
        try:
            if self.adb():
                prop_key = self.combox_choose_prop_key.currentText()
                prop_value = self.adb().get_prop(prop_key)
                self.edit_prop_value.setText(prop_value)
                output = f"当前prop信息：\n{prop_key}={prop_value}"
                logging.info(f"Get Prop: {prop_key}\n{prop_value}")
                self.notice.success(output)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_set_prop(self):
        """点击【设置prop信息】"""
        try:
            if self.adb():
                prop_key = self.combox_choose_prop_key.currentText()
                prop_value = self.edit_prop_value.text()
                if not prop_value:
                    logging.info(f"获取prop值失败，prop值不能为空！")
                    self.notice.error("prop值不能为空！")
                    return
                self.adb().set_prop(prop_key, prop_value)
                output = f"设置prop信息成功，重启生效：\n{prop_key}: {prop_value}"
                logging.info(f"Set Prop: {prop_key}: {prop_value}")
                self.notice.success(output)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_get_pkg_info(self):
        """点击【获取当前包信息】"""
        try:
            if self.adb():
                info_dict = self.adb().current_app_info()
                output = f"版本名: {info_dict['version_name']}\n" \
                         f"版本号: {info_dict['version_code']}\n\n" \
                         f"首次安装时间: {info_dict['first_install_time']}\n" \
                         f"最后更新时间: {info_dict['last_update_time']}"
                logging.info(f"Get Package Info...")
                self.dialog.info(output, "当前包信息")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_get_package_name(self):
        """点击【获取当前包名和activity】"""
        try:
            if self.adb():
                current_app = self.adb().current_app()
                activity = f"{current_app[0]}/{current_app[-1]}"
                logging.info(f"Activity ==> {activity}")
                self.dialog.info(activity)
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_reset_current_app(self):
        """点击【重置当前应用】"""
        try:
            self.adb().current_app_reset()
        except Exception as e:
            self.notice.error(f"重置当前应用出错了：{e}")

    def clicked_btn_uninstall_current_app(self):
        """点击【卸载当前应用】"""
        try:
            pkg = self.adb().current_app()[0]
            self.adb().uninstall(pkg)
            logging.info(f'卸载当前应用 >> {pkg}')
        except Exception as e:
            self.notice.error(f"卸载当前应用出错了：{e}")

    def _swipe(self, func):
        """判断是否连续滑动，供调用拉起线程"""
        try:
            if self.check_box.isChecked():
                while True:
                    func()
            else:
                func()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_swipe2up(self):
        """点击【上滑】如果勾选框为勾选状态，则连续上滑"""
        try:
            if self.adb():
                self.t = threading.Thread(target=self._swipe, args=(self.adb().swipe_to_up,))
                self.t.start()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_swipe2down(self):
        """点击【下拉】如果勾选框为勾选状态，则连续下拉"""
        try:
            if self.adb():
                self.t = threading.Thread(target=self._swipe, args=(self.adb().swipe_to_down,))
                self.t.start()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_swipe2left(self):
        """点击【左滑】如果勾选框为勾选状态，则连续下拉"""
        try:
            if self.adb():
                self.t = threading.Thread(target=self._swipe, args=(self.adb().swipe_to_left,))
                self.t.start()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_swipe2right(self):
        """点击【左滑】如果勾选框为勾选状态，则连续下拉"""
        try:
            if self.adb():
                self.t = threading.Thread(target=self._swipe, args=(self.adb().swipe_to_right,))
                self.t.start()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_swipe_stop(self):
        """点击【停止】结束连续滑动"""
        try:
            common.stop_thread(self.t)
            logging.info("已停止连续滑动")
            self.notice.success("已停止连续滑动")
        except Exception as e:
            logging.error(f"停止连续滑动线程失败: {e}")
            self.dialog.error(f"当前无运行中线程\n停止连续滑动线程失败: {e}")

    def clicked_btn_logcat_c(self):
        """logcat -c"""
        try:
            if self.adb():
                self.adb().logcat_c()
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_logcat(self):
        """获取日志"""
        try:
            log_path = config.LOGCAT_PATH
            # filename = self.adb().gen_file_name("log")
            # file_path = os.path.join(log_path, filename)
            # self.adb().logcat(file_path)
            if self.adb():
                self.edit_logcat_filename.setText(self.adb().dump_crash_log(log_path))
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_open_log_path(self):
        """打开log路径"""
        log_path = config.LOGCAT_PATH
        systemer.open_path(log_path)

    def clicked_btn_screenshot(self):
        """截图"""
        try:
            if self.adb():
                t = threading.Thread(target=self.adb().screenshot, args=(config.SCREEN_PATH,))
                t.start()
                t.join()
                self.notice.info('截图完成')
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_open_screenshot_path(self):
        """打开截图"""
        try:
            filename = systemer.get_latest_file(config.SCREEN_PATH)
            if not systemer.open_path(filename):
                self.notice.warn("打开失败，当前目录为空！")
        except Exception as e:
            logging.error(e)
            self.dialog.error(e)

    def clicked_btn_open_screenshot_dir(self):
        """打开截图目录"""
        systemer.open_path(config.SCREEN_PATH)
