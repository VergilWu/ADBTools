# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import *

from gui.stacked_about import AboutPage
from gui.stacked_adbkit import AdbKitPage
from gui.stacked_fastbot import Fastbot
from gui.stacked_tidevice import TiDevicePage


class RightStacked(object):
    def __init__(self):
        self.right_stacked = QStackedWidget()

        stack1 = AdbKitPage()
        stack2 = TiDevicePage()
        stack3 = Fastbot()
        stack4 = AboutPage()

        self.right_stacked.addWidget(stack1.widget)
        self.right_stacked.addWidget(stack2.widget)
        self.right_stacked.addWidget(stack3.widget)
        self.right_stacked.addWidget(stack4.widget)

        self.right_stacked.setCurrentIndex(0)  # 设置默认界面
