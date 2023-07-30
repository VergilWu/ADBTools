# 按钮颜色设置
BTN_COLOR_GREEN = 'QPushButton{background:#6DDF6D;border-radius:5px;font-family:"Microsoft YaHei UI", Arial, ' \
                  'sans-serif;}QPushButton:hover{background:green;} '
BTN_COLOR_GREEN_NIGHT = 'QPushButton{background:#7079c2;border-radius:5px;color:white;font-family:"Microsoft YaHei ' \
                        'UI", Arial, sans-serif;font-weight:regular;}QPushButton:hover{' \
                        'background:#868dc2;}QPushButton:pressed {background-color: #3a3f64;} '
BTN_COLOR_RED = 'QPushButton{background:#F76677;border-radius:5px;font-family:"Microsoft YaHei UI", Arial, ' \
                'sans-serif;}QPushButton:hover{background:red;} '
BTN_COLOR_YELLOW = 'QPushButton{background:#d6be6f;border-radius:5px;font-family:"Microsoft YaHei UI", Arial, ' \
                   'sans-serif;}QPushButton:hover{background:#d8c78c;} '
BTN_COLOR_BLUE = 'QPushButton{background:#6699FF;border-radius:5px;font-family:"Microsoft YaHei UI", Arial, ' \
                 'sans-serif;}QPushButton:hover{background:blue;} '
BTN_COLOR_GRAY = 'QPushButton{background:#CFCFCF;border-radius:5px;font-family:"Microsoft YaHei UI", Arial, ' \
                 'sans-serif;}QPushButton:hover{background:#9DF7DA;} '
BTN_DONATE = 'QPushButton {background-color: #7079c2;color: white;border-radius: 5px;padding: 10px;}QPushButton:hover ' \
             '{background-color: #868dc2;}QPushButton:pressed {background-color: #3a3f64;} '

# TextEdit
TEXT_EDIT_STYLE = 'background-color: rgb(255, 255, 255);border-radius: 8px; border: 1px groove gray;border-style: outset;'

# 左侧边栏美化
LEFT_STYLE = '''
QWidget#left_widget{
    /* 设置背景色 */
    background:#344286;
    
    /* 设置上、下、左三面白边展示 */
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-left:1px solid white;
    
    /* 设置左上、左下角圆边展示*/
    border-top-left-radius:10px;
    border-bottom-left-radius:10px;
}

/* 设置按钮无边框，白色展示*/
QPushButton{
    border:none;color:white;
}

/* 设置左侧边栏 文本展示*/
QPushButton#left_label{
    border:none;
    border-bottom:1px solid white;
    font-size:16px;
    font-weight:600;
    font-family: "Microsoft YaHei UI", Arial, sans-serif;
}

QPushButton#left_button:hover{
    border-left:4px solid red;
    font-weight:600;
}
'''

# 右侧边栏美化
RIGHT_STYLE = '''
QWidget#right_widget{
    color:#232C51;
    background:white;
    border-top:1px solid white;
    border-bottom:1px solid white;
    border-right:1px solid white;
    border-top-right-radius:10px;
    border-bottom-right-radius:10px;
}
QLabel#right_label{
    border:none;
    font-size:16px;
    font-weight:700;
    font-family: "Microsoft YaHei UI", Arial, sans-serif;
}

QToolButton{
    border:none;
}
QToolButton:hover{
    border-bottom:2px solid #F76677;
}
'''

RIGHT_OTHER_WEBSITE_STYLE = '''
QPushButton{
    border:none;
    color:gray;
    font-size:12px;
    height:40px;
    padding-left:5px;
    padding-right:10px;
    text-align:left;
}
QPushButton:hover{
    color:black;
    border:1px solid #F3F3F5;
    border-radius:10px;
    background:LightGray;
}
'''
