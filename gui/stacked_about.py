from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices, QFont, QPalette
from PyQt5.QtWidgets import *

from config import qss_cfg, config
from config import qss_cfg
from gui.dialog import DiaLog, Notice
from utils.systemer import get_abs_path


class AboutPage(object):
    def __init__(self):
        super(AboutPage, self).__init__()
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.dialog = DiaLog(self.widget)
        self.notice = Notice()

        self.widget.setObjectName('right_widget')
        self.widget.setStyleSheet(qss_cfg.RIGHT_STYLE)

        self.init_ui()

    def init_ui(self):
        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setFrameShape(QFrame.NoFrame)  # 设置无边框
        self.scroll_area.viewport().setStyleSheet("background-color:transparent;")
        self.scroll_area.setWidgetResizable(True)  # 设置滚动区域的小部件可以调整大小
        self.layout.addWidget(self.scroll_area)

        # 创建滚动区域的小部件
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # 创建滚动区域的小部件的布局
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        # logo
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap(get_abs_path("favicon.ico")))
        self.logo_label.setAlignment(Qt.AlignHCenter)
        self.scroll_layout.addWidget(self.logo_label)

        # 程序名
        self.label_name = QLabel(f"程序名：{config.APP_NAME}")
        self.label_name.setContentsMargins(0, 30, 0, 0)
        self.scroll_layout.addWidget(self.label_name)

        # 程序版本
        self.label_version = QLabel(f"版本: {config.APP_VERSION}")
        self.scroll_layout.addWidget(self.label_version)

        # 程序介绍
        self.label_desc = QLabel(f"描述: {config.APP_DESCRIPTION}")
        self.label_desc.setWordWrap(True)
        self.scroll_layout.addWidget(self.label_desc)

        # 开源协议
        self.label_license = QLabel("License: <a href='https://github.com/VergilWu/ADBTools/blob/main/LICENSE'>Apache"
                                    "-2.0 license</a>")
        self.label_license.setContentsMargins(0, 20, 0, 0)
        self.label_license.setTextFormat(Qt.RichText)
        self.label_license.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label_license.setOpenExternalLinks(True)
        self.label_license.linkActivated.connect(self.open_url)
        self.scroll_layout.addWidget(self.label_license)

        # 开源地址
        self.label_github = QLabel("Github: <a href='https://github.com/VergilWu/ADBTools.git'>https://github.com"
                                   "/VergilWu/ADBTools.git</a>")
        self.label_github.setTextFormat(Qt.RichText)
        self.label_github.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label_github.setOpenExternalLinks(True)
        self.label_github.linkActivated.connect(lambda: self.open_url)
        self.scroll_layout.addWidget(self.label_github)

        # 邮箱
        self.label_email = QLabel("Email: <a href='mailto:vergilcat@gmail.com'>vergilcat@gmail.com</a>")
        self.label_email.setOpenExternalLinks(True)
        self.label_email.linkActivated.connect(self.send_email)
        self.scroll_layout.addWidget(self.label_email)

        # 捐赠二维码
        self.label_desc_donate = QLabel("如果您觉得本软件对您有帮助，欢迎打赏！")
        self.label_desc_donate.setContentsMargins(0, 20, 0, 0)
        self.btn_show_donate = QPushButton("显示二维码")
        self.btn_show_donate.setFont(QFont("Microsoft YaHei UI"))
        self.btn_show_donate.setStyleSheet(qss_cfg.BTN_DONATE)
        self.btn_show_donate.setCheckable(True)
        self.btn_show_donate.setChecked(False)
        self.btn_show_donate.clicked.connect(self.show_donate)

        self.layout_donate = QHBoxLayout()
        self.layout_collapsible_donate = QGroupBox()
        self.layout_collapsible_donate.setCheckable(False)
        self.layout_collapsible_donate.setChecked(False)
        self.layout_collapsible_donate.setVisible(False)
        self.layout_collapsible_donate.setLayout(self.layout_donate)
        self.layout_donate_wechat = QVBoxLayout()
        self.layout_donate_alipay = QVBoxLayout()

        self.label_donate_wechat = QLabel()
        self.label_donate_wechat.setPixmap(
            QPixmap(get_abs_path("qr_wechat.jpg")).scaled(150, 150))
        self.layout_donate_wechat.setAlignment(Qt.AlignHCenter)
        self.layout_donate_wechat.addWidget(self.label_donate_wechat)
        self.layout_donate.addLayout(self.layout_donate_wechat)

        self.label_desc_donate_wechat = QLabel("微信")
        self.label_desc_donate_wechat.setAlignment(Qt.AlignHCenter)
        self.layout_donate_wechat.addWidget(self.label_desc_donate_wechat)
        self.layout_donate.addLayout(self.layout_donate_alipay)

        self.label_donate_alipay = QLabel()
        self.label_donate_alipay.setPixmap(
            QPixmap(get_abs_path("qr_alipay.jpg")).scaled(150, 150))
        self.layout_donate_alipay.setAlignment(Qt.AlignHCenter)
        self.layout_donate_alipay.addWidget(self.label_donate_alipay)

        self.label_desc_donate_alipay = QLabel("支付宝")
        self.label_desc_donate_alipay.setAlignment(Qt.AlignHCenter)
        self.layout_donate_alipay.addWidget(self.label_desc_donate_alipay)

        self.scroll_layout.addWidget(self.label_desc_donate)
        self.scroll_layout.addWidget(self.btn_show_donate)
        self.scroll_layout.addWidget(self.layout_collapsible_donate)

        self.scroll_layout.setAlignment(Qt.AlignCenter)

        # 设置滚动条策略
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @staticmethod
    def open_url(url):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        QDesktopServices.openUrl(QUrl(url))

    @staticmethod
    def send_email(email):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        QDesktopServices.openUrl(QUrl("mailto:" + email))

    def show_donate(self):
        if self.btn_show_donate.isChecked():
            self.btn_show_donate.setText("隐藏二维码")
            self.layout_collapsible_donate.setChecked(True)
            self.layout_collapsible_donate.setVisible(True)
        else:
            self.btn_show_donate.setText("显示二维码")
            self.layout_collapsible_donate.setChecked(False)
            self.layout_collapsible_donate.setVisible(False)
