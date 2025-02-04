from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QComboBox

from new_calculatorUI import Ui_MainWindow
import data_func

from decimal import Decimal
import random
import math

class MyComboBox(QComboBox):
    clicked = pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数,"弹出下拉列表"
        self.clicked.emit()  # 弹出前发送信号
        super(MyComboBox, self).showPopup()  # 调用父类的showPopup()


class MyLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()

    # 可在外部与槽函数连接
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


class Calculator(QtWidgets.QMainWindow, Ui_MainWindow):
    _startPos = None
    _endPos = None
    _isTracking = None

    # 鼠标移动事件
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            # 移动窗口
            self.move(self.pos() + self._endPos)

    # 鼠标按下事件
    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        # 根据鼠标按下时的位置判断是否在QFrame范围内
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "top_frame":
            # 判断鼠标按下的是左键
            if a0.button() == QtCore.Qt.LeftButton:
                self._isTracking = True
                # 记录初始位置
                self._startPos = QtCore.QPoint(a0.x(), a0.y())

    # 鼠标松开事件
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.all_zip = self.e_zip = self.i_zip = []

        self.c_values = self.h_values = self.r_values = []
        self.ATK = self.HP = self.tDEF = self.mDEF = self.rPOW = self.mPOW = self.CRT = self.CRT_D = self.DMG = self.h_HP_P = self.h_DMG = self.h_CRT_D = self.h_CRT = self.h_ATK_P = self.h_mPOW = self.h_rPOW = self.h_mDEF = self.h_tDEF = self.h_HP = self.h_ATK = self.c_CRT_D = self.c_CRT = self.c_mDEF = self.c_tDEF = self.c_HP = self.c_ATK = self.r_HP = self.r_ATK = self.r_tDEF = self.r_mDEF = self.r_CRT = self.r_CRT_D = self.r_DMG = self.r_HP_P = self.r_ATK_P = self.r_tDEF_P = self.r_mDEF_P = Decimal(
            0)

        self.i_ATK_buff = self.i_CRT = self.i_CRT_D = self.i_DMG = self.i_PTT_buff = Decimal(0)

        self.e_tDEF = self.e_mDEF = self.e_rDMG = self.e_rCRT = Decimal(0)

        self.enemy_flag = 0
        self.type = ''
        self.match_up = Decimal(0)
        self.skill1_ratio = self.skill2_ratio = self.skill3_ratio = Decimal(0)

        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏窗口边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 隐藏窗口背景

        # 输入限制为数字
        self.skill1_ratio_input.setValidator(QRegExpValidator(QRegExp("[0-9]*$"), self))
        self.skill2_ratio_input.setValidator(QRegExpValidator(QRegExp("[0-9]*$"), self))
        self.skill3_ratio_input.setValidator(QRegExpValidator(QRegExp("[0-9]*$"), self))
        self.enemy_tDEF_input.setValidator(QRegExpValidator(QRegExp("[0-9]*$"), self))
        self.enemy_mDEF_input.setValidator(QRegExpValidator(QRegExp("[0-9]*$"), self))
        self.enemy_rDMG_input.setValidator(QRegExpValidator(QRegExp("[0-9.]*"), self))
        self.enemy_rCRT_input.setValidator(QRegExpValidator(QRegExp("[0-9.]*"), self))

        self.insight_spinbox.setMaximum(0)
        self.level_spinbox.setMaximum(0)
        self.heart_level_spinbox.setMaximum(0)
        self.skill2_ratio_input.setPlaceholderText("默认为0")
        self.skill3_ratio_input.setPlaceholderText("默认为0")
        self.skill1_ratio_input.setPlaceholderText("默认为0")
        self.enemy_tDEF_input.setPlaceholderText("默认为0")
        self.enemy_mDEF_input.setPlaceholderText("默认为0")
        self.enemy_rCRT_input.setPlaceholderText("默认为0")
        self.enemy_rDMG_input.setPlaceholderText("默认为0")
        self.tips_text.setReadOnly(True)
        self.tips_text.setText('1989年6月5日 暴雨科算研究笔记\n\n我是暴雨科算计算器的作者膝盖，非常感谢你下载了这个计算器。\n\n我希望做一款让小白也可以用得上的1999计算器。\n多回合循环的伤害、伤害曲线、心相增幅、导出excel和伤害曲线将在未来更新。\n目前已经实现了上个版本中说过的角色、心相、共鸣的自选，未来还会越来越好。\n\n计算器的制作付出了相当的心血，同时也感谢为我提供帮助的人\n\n特别鸣谢：\n\n美工：海马姐\n\n数据支持：灰机 重返未来1999wiki\n\n思路提供及游戏机制解析：NGA 风焰大佬\n\nBUG测试：海马姐、飞鱼、MistEO、欲明、狼群、忌廉汽水、飞鱼游戏1999交流群、灰机1999wiki交流群、千禧咖啡厅粉丝群\n\n软件设计及制作：我自己\n\n\n目前计算器仍然可能有BUG，如果有思路或BUG，可以加下面的游戏交流群向我提交，万分感谢。\n\n后续如果我没有被暴雨淋到的话，肯定还是会继续更新的。\n\n项目已经开源到github了，使用了python+sqlite3+pyqt5制作，感兴趣的司辰也可以去看看\n\n如果觉得软件做得还不错，可以去给发布视频下面点点赞，评评论，投个硬币。\n所有收益都将用来更新新版本和买生发洗发水。\n\n游戏交流群：930796326\n\ngithub地址：https://github.com/XigaiMax/Calculator1999\n\n再次感谢你的使用！司辰，祝你好运！')

        self.resonate_level_spinbox.setMaximum(0)
        self.info_full_table.hide()  # 隐藏完整角色面板显示
        # 隐藏敌人数据输入区
        self.verticalLayoutWidget_11.setVisible(True)
        self.verticalLayoutWidget_13.setVisible(False)
        self.verticalLayoutWidget_8.setVisible(False)
        self.verticalLayoutWidget_9.setVisible(False)
        self.verticalLayoutWidget_10.setVisible(False)

        self.pushbutton_max.toggled.connect(self.maximize_button)  # 最大化按钮
        self.pushbutton_tips.toggled.connect(self.tips_button)  # 提示按钮（未实现）

        self.info_change_button.toggled.connect(self.change_info_widget)  # 切换角色完整/简易面板显示区

        self.enemy_change_button.toggled.connect(self.change_enemy_layout)  # 切换敌人选择/输入区

        self.attribute_choice_combobox.clicked.connect(self.attribute_click)  # 单次点击属性选择栏时更新选择栏内容并链接槽（纯是为了好看，麻烦死了）
        self.attribute_choice_combobox.activated.connect(self.update_character_list)  # 单次点击属性选择栏时更新角色选择列表

        self.insight_spinbox.valueChanged.connect(self.update_level)  #
        self.level_spinbox.valueChanged.connect(self.update_character)  # 选择等级时更新角色数据并修改角色数据显示面板

        self.heart_choice_combobox.clicked.connect(self.heart_click)  # 单次点击心相栏更新心相栏内容
        self.heart_choice_combobox.activated.connect(self.update_heart_img)  # 单次点击心相栏后立刻更新心相图片

        self.enemy_choice_combobox.clicked.connect(self.enemy_click)  # 单次点击敌人栏更新敌人栏内容
        # self.enemy_choice_combobox.activated.connect(self.update_enemy)

        self.heart_level_spinbox.valueChanged.connect(self.update_heart)  # 选择心相等级后更新心相数据并修改角色数据显示面板

        self.resonate_level_spinbox.valueChanged.connect(self.update_all_resonate_level)  # 选择共鸣等级时更新所有共鸣当前等级

        # 每当选择共鸣块数量后更新共鸣数据并修改角色数据显示面板
        self.Re_main_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_T_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_I_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_O_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_S_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_Z_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_L_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_J_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_3_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_2_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_atk_spinbox.valueChanged.connect(self.update_resonate)
        self.Re_def_spinbox.valueChanged.connect(self.update_resonate)

        self.insight_effect_choice_combobox.currentIndexChanged.connect(self.update_combat_value)
        self.restraint_choice_combobox.currentIndexChanged.connect(self.update_combat_value)
        self.damage_choice_combobox.currentIndexChanged.connect(self.update_combat_value)
        self.skill3_ratio_input.editingFinished.connect(self.update_combat_value)
        self.skill1_ratio_input.editingFinished.connect(self.update_combat_value)
        self.skill2_ratio_input.editingFinished.connect(self.update_combat_value)
        # self.enemy_choice_combobox.currentIndexChanged.connect(self.update_enemy)

        # self.calculation_button.button_clicked_signal.connect(self.calculation_all)

    def tips_button(self, checked):
        if checked:
            self.main_stackedWidget.setCurrentIndex(1)
        else:
            self.main_stackedWidget.setCurrentIndex(0)

    # 没啥用的最大化按钮切换
    def maximize_button(self, checked):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(':resources/images/max.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(':resources/images/return.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if checked:
            self.pushbutton_max.setIcon(icon4)
        else:
            self.pushbutton_max.setIcon(icon1)

    # 切换角色信息显示面板
    def change_info_widget(self, checked):
        if checked:
            self.info_change_label.setText('完整面板显示')
            self.info_easy_text.hide()
            self.info_full_table.show()
        else:
            self.info_change_label.setText('简易面板显示')
            self.info_full_table.hide()
            self.info_easy_text.show()

    # 属性单次点击事件
    def attribute_click(self):
        self.attribute_choice_combobox.clicked.disconnect(self.attribute_click)  # 断开单次点击事件
        self.attribute_choice_combobox.clear()  # 清除原有选择项
        self.attribute_choice_combobox.addItems(data_func.attribute_list)  # 添加新的选择项

        self.character_choice_combobox.activated.connect(self.update_character_img)  # 选择角色时更新角色图片
        self.character_choice_combobox.activated.connect(self.update_insight)  # 选择角色时更新洞悉等级上限
        self.character_choice_combobox.activated.connect(self.update_resonate_main)  # 选择角色时更新角色共鸣主块
        self.level_spinbox.setMaximum(30)  # 设置角色等级上限为30，后续由洞悉等级选择时触发更改

    # 心相单次点击事件
    def heart_click(self):
        self.heart_choice_combobox.clicked.disconnect(self.heart_click)
        self.heart_choice_combobox.clear()
        self.heart_choice_combobox.addItems(data_func.heart_list)
        self.heart_level_spinbox.setMaximum(60)
        self.heart_level_spinbox.setValue(1)
        self.heart_choice_combobox.activated.connect(self.update_heart_img)

    def enemy_click(self):
        self.enemy_choice_combobox.clicked.disconnect(self.enemy_click)
        self.enemy_choice_combobox.clear()
        self.enemy_choice_combobox.addItems(data_func.enemy_list)
        self.enemy_choice_combobox.activated.connect(self.update_enemy)  # 单次点击后立刻连接到敌人选择

    # 在单次点击时更新属性对应的角色列表和角色图片
    def update_character_list(self, index):
        self.character_choice_combobox.clear()
        self.character_choice_combobox.addItems(data_func.choice_attribute(index))

        self.character_img.setPixmap(
            QtGui.QPixmap(f":/resources/images/{self.character_choice_combobox.currentText()}.png"))
        self.rare_img.setPixmap(
            QtGui.QPixmap(
                f":/resources/images/{data_func.choice_rare_bg(self.character_choice_combobox.currentText())}star.png"))
        self.insight_spinbox.setMaximum(data_func.choice_insight(self.character_choice_combobox.currentText()))

    # 更新角色图片
    def update_character_img(self):
        skin_list=['红弩箭','苏芙比','百夫长','星锑','柏林以东','X','APPLe','夏利','玛丽莲','挖掘艺术','玛蒂尔达','十四行诗','小春雀儿','莉拉妮','拉拉泉','皮克勒斯','坦南特']
        if self.character_choice_combobox.currentText() in skin_list:
            if random.randint(0,1) == 1:
                self.character_img.setPixmap(
                    QtGui.QPixmap(f":/resources/images/{self.character_choice_combobox.currentText()}2.png"))
            else:self.character_img.setPixmap(QtGui.QPixmap(f":/resources/images/{self.character_choice_combobox.currentText()}.png"))
        else:
            self.character_img.setPixmap(QtGui.QPixmap(f":/resources/images/{self.character_choice_combobox.currentText()}.png"))
        self.rare_img.setPixmap(
            QtGui.QPixmap(
                f":/resources/images/{data_func.choice_rare_bg(self.character_choice_combobox.currentText())}star.png"))

    # 根据角色 更新洞悉上限（2，3星角色洞悉上限为2）
    def update_insight(self):
        self.insight_spinbox.setMaximum(data_func.choice_insight(self.character_choice_combobox.currentText()))
        self.level_spinbox.setMaximum(data_func.choice_level(self.insight_spinbox.value()))

    # 根据洞悉 更新等级上限和共鸣上限（洞1 共鸣上限5，洞2 共鸣上限10，洞3 共鸣上限15）
    def update_level(self):
        self.level_spinbox.setValue(1)
        self.level_spinbox.setMaximum(data_func.choice_level(self.insight_spinbox.value()))
        self.resonate_level_spinbox.setMaximum(data_func.choice_resonate_level(self.insight_spinbox.value()))

    def update_heart_img(self):
        self.heart_img.setPixmap(QtGui.QPixmap(f":/resources/images/h{self.heart_choice_combobox.currentText()}.png"))
        self.update_heart()

    # 更新主共鸣块图片和名字
    def update_resonate_main(self):
        self.Re_main_img.setPixmap(QtGui.QPixmap(
            f":/resources/images/{data_func.choice_main_resonate(self.character_choice_combobox.currentText())}.png"))
        self.Re_main_label.setText(
            f'{data_func.choice_main_resonate(self.character_choice_combobox.currentText())}')

    # 更新共鸣块等级显示和是否可用
    def update_all_resonate_level(self):
        # self.Re_main_spinbox.setMaximum(0)
        # self.Re_L_spinbox.setMaximum(0)
        # self.Re_J_spinbox.setMaximum(0)
        # self.Re_S_spinbox.setMaximum(0)
        # self.Re_Z_spinbox.setMaximum(0)
        # self.Re_I_spinbox.setMaximum(0)
        # self.Re_O_spinbox.setMaximum(0)
        # self.Re_T_spinbox.setMaximum(0)
        # self.Re_3_spinbox.setMaximum(0)
        # self.Re_2_spinbox.setMaximum(0)
        # self.Re_atk_spinbox.setMaximum(0)
        # self.Re_def_spinbox.setMaximum(0)
        r_level = self.resonate_level_spinbox.value()
        c_name = self.character_choice_combobox.currentText()

        r_ava = [0, 16, 16, 20, 20, 25, 25, 30, 30, 36, 49, 49, 49, 49, 49, 49]  # 已经忘了，想起来的时候记得写一下
        number_main = self.Re_main_spinbox.value()
        number_L = self.Re_L_spinbox.value()
        number_J = self.Re_J_spinbox.value()
        number_S = self.Re_S_spinbox.value()
        number_Z = self.Re_Z_spinbox.value()
        number_I = self.Re_I_spinbox.value()
        number_O = self.Re_O_spinbox.value()
        number_T = self.Re_T_spinbox.value()
        number_3 = self.Re_3_spinbox.value()
        number_2 = self.Re_2_spinbox.value()
        number_atk = self.Re_atk_spinbox.value()
        number_def = self.Re_def_spinbox.value()
        number_all = number_main * 5 + (
                number_L + number_J + number_S + number_Z + number_I + number_O + number_T) * 4 + number_3 * 3 + number_2 * 2 + number_def + number_atk
        number_ava = r_ava[r_level]
        if number_all > number_ava:
            text = f'<font color="red">{number_all}</font>/{number_ava}'
        else:
            text = f'{number_all}/{number_ava}'
        self.resonate_ava_label.setText(text)
        results = data_func.choice_resonate_all_level(c_name, r_level)

        for resonate, level, ava in results:

            labels_mapping = {
                '大Z形': self.Re_main_level_label,
                '大T形': self.Re_main_level_label,
                '大U形': self.Re_main_level_label,
                '大十字形': self.Re_main_level_label,
                'L形': self.Re_L_level_label,
                'J形': self.Re_J_level_label,
                'T形': self.Re_T_level_label,
                'O形': self.Re_O_level_label,
                'I形': self.Re_I_level_label,
                'S形': self.Re_S_level_label,
                'Z形': self.Re_Z_level_label,
                '三格形': self.Re_3_level_label,
                '双格形': self.Re_2_level_label,
                '增伤单格形': self.Re_atk_level_label,
                '减防单格形': self.Re_def_level_label
            }
            labels_mapping2 = {
                '大Z形': self.Re_main_spinbox,
                '大T形': self.Re_main_spinbox,
                '大U形': self.Re_main_spinbox,
                '大十字形': self.Re_main_spinbox,
                'L形': self.Re_L_spinbox,
                'J形': self.Re_J_spinbox,
                'T形': self.Re_T_spinbox,
                'O形': self.Re_O_spinbox,
                'I形': self.Re_I_spinbox,
                'S形': self.Re_S_spinbox,
                'Z形': self.Re_Z_spinbox,
                '三格形': self.Re_3_spinbox,
                '双格形': self.Re_2_spinbox,
                '增伤单格形': self.Re_atk_spinbox,
                '减防单格形': self.Re_def_spinbox
            }
            if resonate in labels_mapping:
                label = labels_mapping[resonate]
                label.setText(f'LV.{level}')

            if resonate in labels_mapping2:
                spinbox = labels_mapping2[resonate]

                spinbox.setMaximum(ava)

    # 更新角色数据
    def update_character(self):
        name = self.character_choice_combobox.currentText()
        insight = self.insight_spinbox.value()
        level = self.level_spinbox.value()
        self.c_values = data_func.choice_character(name, insight, level)

        if self.c_values:
            self.c_ATK, self.c_HP, self.c_tDEF, self.c_mDEF, self.c_CRT, self.c_CRT_D = self.c_values
            self.update_info()

    # 更新心相数据
    def update_heart(self):
        h_name = self.heart_choice_combobox.currentText()

        h_level = self.heart_level_spinbox.value()

        self.h_values = data_func.choice_heart(h_name, h_level)

        if self.h_values:
            self.h_ATK, self.h_HP, self.h_tDEF, self.h_mDEF, self.h_rPOW, self.h_mPOW, self.h_ATK_P, self.h_CRT, self.h_CRT_D, self.h_DMG, self.h_HP_P = self.h_values
            self.update_info()

    # 更新共鸣数据
    def update_resonate(self):
        r_ava = [0, 16, 16, 20, 20, 25, 25, 30, 30, 36, 49, 49, 49, 49, 49, 49]
        c_name = self.character_choice_combobox.currentText()
        r_level = self.resonate_level_spinbox.value()
        number_main = self.Re_main_spinbox.value()
        number_L = self.Re_L_spinbox.value()
        number_J = self.Re_J_spinbox.value()
        number_S = self.Re_S_spinbox.value()
        number_Z = self.Re_Z_spinbox.value()
        number_I = self.Re_I_spinbox.value()
        number_O = self.Re_O_spinbox.value()
        number_T = self.Re_T_spinbox.value()
        number_3 = self.Re_3_spinbox.value()
        number_2 = self.Re_2_spinbox.value()
        number_atk = self.Re_atk_spinbox.value()
        number_def = self.Re_def_spinbox.value()

        number_all = number_main * 5 + (
                    number_L + number_J + number_S + number_Z + number_I + number_O + number_T) * 4 + number_3 * 3 + number_2 * 2 + number_def + number_atk
        number_ava = r_ava[r_level]
        if number_all > number_ava:
            text = f'<font color="red">{number_all}</font>/{number_ava}'
        else:
            text = f'{number_all}/{number_ava}'
        self.resonate_ava_label.setText(text)

        self.r_values = data_func.choice_resonate(c_name, r_level, number_main, number_L, number_J, number_S,
                                                  number_Z,
                                                  number_I, number_O,
                                                  number_T, number_3, number_2, number_atk, number_def)
        if self.r_values:
            self.r_HP, self.r_ATK, self.r_tDEF, self.r_mDEF, self.r_CRT, self.r_CRT_D, self.r_DMG, self.r_HP_P, self.r_ATK_P, self.r_tDEF_P, self.r_mDEF_P = self.r_values
            self.update_info()

    # 计算所有角色数据并触发信息显示修改
    def update_info(self):

        if self.h_ATK_P + self.r_ATK_P != 0:

            self.ATK = self.c_ATK * (1 + self.h_ATK_P + self.r_ATK_P) + self.h_ATK + self.r_ATK
        else:

            self.ATK = self.c_ATK + self.h_ATK + self.r_ATK

        if self.h_HP_P + self.r_HP_P != 0:
            self.HP = self.c_HP * (1 + self.h_HP_P + self.r_HP_P) + self.h_HP + self.r_HP
        else:
            self.HP = self.c_HP + self.h_HP + self.r_HP

        if self.r_tDEF_P != 0:
            self.tDEF = self.c_tDEF * (1 + self.r_tDEF_P) + self.h_tDEF + self.r_tDEF
        else:
            self.tDEF = self.c_tDEF + self.h_tDEF + self.r_tDEF

        if self.r_mDEF_P != 0:
            self.mDEF = self.c_mDEF * (1 + self.r_mDEF_P) + self.h_mDEF + self.r_mDEF
        else:
            self.mDEF = self.c_mDEF + self.h_mDEF + self.r_mDEF

        self.rPOW = self.h_rPOW

        self.mPOW = self.h_mPOW

        self.CRT = self.c_CRT + self.h_CRT + self.r_CRT
        self.CRT_D = self.c_CRT_D + self.h_CRT_D + self.r_CRT_D + Decimal(str(1.3))
        self.DMG = self.h_DMG + self.r_DMG

        self.all_zip = [self.ATK, self.rPOW, self.mPOW, self.CRT, self.CRT_D, self.DMG]

        self.update_easy_info()
        self.update_full_info()
        self.calculation_button.button_clicked_signal.connect(self.calculation_all)

    # 修改简易角色信息显示
    def update_easy_info(self):

        data = f"攻击:{math.floor(self.ATK)}\n生命:{math.floor(self.HP)}\n现实防御:{math.floor(self.tDEF)}\n精神防御:{math.floor(self.mDEF)}\n暴击率:{Decimal(self.CRT * 100).normalize()}%\n暴击创伤:{Decimal(self.CRT_D * 100).normalize()}%\n创伤加成:{Decimal(Decimal(self.DMG).normalize() * 100).normalize()}%"

        self.info_easy_text.setPlainText(data)

    # 修改完整角色信息显示
    def update_full_info(self):

        if self.c_values:
            for i in range(6):
                c_item = QtWidgets.QTableWidgetItem(f'{self.c_values[i]}')
                self.info_full_table.setItem(i, 1, c_item)
            c_0_item = QtWidgets.QTableWidgetItem('0.0')
            self.info_full_table.setItem(6, 1, c_0_item)
            c_0_item = QtWidgets.QTableWidgetItem('0.0')
            self.info_full_table.setItem(7, 1, c_0_item)
            c_0_item = QtWidgets.QTableWidgetItem('0.0')
            self.info_full_table.setItem(8, 1, c_0_item)

        if self.h_values:
            h_ATK_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.h_ATK + (self.c_ATK * self.h_ATK_P))}')
            self.info_full_table.setItem(0, 2, h_ATK_item)
            h_HP_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.h_HP + (self.c_HP * self.h_HP_P))}')
            self.info_full_table.setItem(1, 2, h_HP_item)
            h_tDEF_item = QtWidgets.QTableWidgetItem(f'{self.h_tDEF}')
            self.info_full_table.setItem(2, 2, h_tDEF_item)
            h_mDEF_item = QtWidgets.QTableWidgetItem(f'{self.h_mDEF}')
            self.info_full_table.setItem(3, 2, h_mDEF_item)
            h_CRT_item = QtWidgets.QTableWidgetItem(f'{self.h_CRT}')
            self.info_full_table.setItem(4, 2, h_CRT_item)
            h_CRT_D_item = QtWidgets.QTableWidgetItem(f'{self.h_CRT_D}')
            self.info_full_table.setItem(5, 2, h_CRT_D_item)
            h_DMG_item = QtWidgets.QTableWidgetItem(f'{self.h_DMG}')
            self.info_full_table.setItem(6, 2, h_DMG_item)
            h_mPOW_item = QtWidgets.QTableWidgetItem(f'{self.h_mPOW}')
            self.info_full_table.setItem(7, 2, h_mPOW_item)
            h_rPOW_item = QtWidgets.QTableWidgetItem(f'{self.h_rPOW}')
            self.info_full_table.setItem(8, 2, h_rPOW_item)

        if self.r_values:
            r_ATK_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.r_ATK + (self.c_ATK * self.r_ATK_P))}')
            self.info_full_table.setItem(0, 3, r_ATK_item)
            r_HP_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.r_HP + (self.c_HP * self.r_HP_P))}')
            self.info_full_table.setItem(1, 3, r_HP_item)
            r_tDEF_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.r_tDEF + (self.c_tDEF * self.r_tDEF_P))}')
            self.info_full_table.setItem(2, 3, r_tDEF_item)
            r_mDEF_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.r_mDEF + (self.c_mDEF * self.r_mDEF_P))}')
            self.info_full_table.setItem(3, 3, r_mDEF_item)
            r_CRT_item = QtWidgets.QTableWidgetItem(f'{self.r_CRT}')
            self.info_full_table.setItem(4, 3, r_CRT_item)
            r_CRT_D_item = QtWidgets.QTableWidgetItem(f'{self.r_CRT_D}')
            self.info_full_table.setItem(5, 3, r_CRT_D_item)
            r_DMG_item = QtWidgets.QTableWidgetItem(f'{self.r_DMG}')
            self.info_full_table.setItem(6, 3, r_DMG_item)
            r_0_item = QtWidgets.QTableWidgetItem('0.0')
            self.info_full_table.setItem(7, 3, r_0_item)
            r_0_item = QtWidgets.QTableWidgetItem('0.0')
            self.info_full_table.setItem(8, 3, r_0_item)

        ATK_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.ATK)}')
        self.info_full_table.setItem(0, 4, ATK_item)
        HP_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.HP)}')
        self.info_full_table.setItem(1, 4, HP_item)
        tDEF_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.tDEF)}')
        self.info_full_table.setItem(2, 4, tDEF_item)
        mDEF_item = QtWidgets.QTableWidgetItem(f'{math.floor(self.mDEF)}')
        self.info_full_table.setItem(3, 4, mDEF_item)
        CRT_item = QtWidgets.QTableWidgetItem(f'{self.CRT}')
        self.info_full_table.setItem(4, 4, CRT_item)
        CRT_D_item = QtWidgets.QTableWidgetItem(f'{self.CRT_D}')
        self.info_full_table.setItem(5, 4, CRT_D_item)
        DMG_item = QtWidgets.QTableWidgetItem(f'{self.DMG}')
        self.info_full_table.setItem(6, 4, DMG_item)
        mPOW_item = QtWidgets.QTableWidgetItem(f'{self.mPOW}')
        self.info_full_table.setItem(7, 4, mPOW_item)
        rPOW_item = QtWidgets.QTableWidgetItem(f'{self.rPOW}')
        self.info_full_table.setItem(8, 4, rPOW_item)

    # 计算所有己方战斗数据
    def update_combat_value(self):
        # self.i_ATK_buff = self.i_CRT = self.i_CRT_D = self.i_DMG = self.i_PTT_buff = Decimal(0)

        values = data_func.choice_insight2(self.insight_effect_choice_combobox.currentIndex())

        self.i_ATK_buff, self.i_CRT, self.i_CRT_D, self.i_DMG, self.i_PTT_buff = values

        # self.match_up = Decimal(0)
        if self.restraint_choice_combobox.currentIndex() == 0:
            self.match_up = Decimal(0)
        else:
            self.match_up = Decimal(str(0.3))

        # self.type = ''
        self.type = self.damage_choice_combobox.currentText()

        if self.skill1_ratio_input.text() != '':
            self.skill1_ratio = Decimal(self.skill1_ratio_input.text()) / 100
        else:
            self.skill1_ratio = Decimal(0)
        if self.skill2_ratio_input.text() != '':
            self.skill2_ratio = Decimal(self.skill2_ratio_input.text()) / 100
        else:
            self.skill2_ratio = Decimal(0)
        if self.skill3_ratio_input.text() != '':
            self.skill3_ratio = Decimal(self.skill3_ratio_input.text()) / 100
        else:
            self.skill3_ratio = Decimal(0)

        self.i_zip = [self.i_ATK_buff, self.i_CRT, self.i_CRT_D, self.i_DMG, self.i_PTT_buff, self.match_up, self.type,
                      self.skill1_ratio, self.skill2_ratio, self.skill3_ratio]

    def change_enemy_layout(self, checked):

        if checked:
            self.enemy_flag = 1
            self.enemy_change_label.setText('敌人属性')
            self.verticalLayoutWidget_11.setVisible(False)
            self.verticalLayoutWidget_13.setVisible(True)
            self.verticalLayoutWidget_8.setVisible(True)
            self.verticalLayoutWidget_9.setVisible(True)
            self.verticalLayoutWidget_10.setVisible(True)
        else:
            self.enemy_flag = 0
            self.enemy_change_label.setText('敌人选择')
            self.verticalLayoutWidget_11.setVisible(True)
            self.verticalLayoutWidget_13.setVisible(False)
            self.verticalLayoutWidget_8.setVisible(False)
            self.verticalLayoutWidget_9.setVisible(False)
            self.verticalLayoutWidget_10.setVisible(False)

    def update_enemy(self):
        if self.enemy_flag == 0:
            self.e_values = data_func.choice_enemy(self.enemy_choice_combobox.currentIndex())
            if self.e_values:
                self.e_tDEF, self.e_mDEF, self.e_rDMG, self.e_rCRT = self.e_values
            data = f"现实防御：{self.e_tDEF}\n精神防御：{self.e_mDEF}\n受创减免：{self.e_rDMG * 100}%\n暴击防御：{self.e_rCRT * 100}%"
            self.enemy_info_text.setPlainText(data)

        else:
            if self.enemy_tDEF_input.text()!='':
                self.e_tDEF = Decimal(self.enemy_tDEF_input.text())
            else:
                self.e_tDEF = Decimal(0)
            if self.enemy_mDEF_input.text() != '':
                self.e_mDEF = Decimal(self.enemy_mDEF_input.text())
            else:
                self.e_mDEF = Decimal(0)
            if self.enemy_rDMG_input.text() != '':
                self.e_rDMG = Decimal(str(self.enemy_rDMG_input.text())) / 100
            else:
                self.e_rDMG = Decimal(0)
            if self.enemy_rCRT_input.text() != '':
                self.e_rCRT = Decimal(str(self.enemy_rCRT_input.text())) / 100
            else:
                self.e_rCRT = Decimal(0)

        self.e_zip = [self.e_tDEF, self.e_mDEF, self.e_rDMG, self.e_rCRT]  # 打包敌人数据

    def calculation_all(self):

        self.update_combat_value()
        self.update_easy_info()
        self.update_enemy()  # 在点击计算时立刻更新一次敌人数据

        results = data_func.final_damage_calculation(self.all_zip, self.i_zip, self.e_zip)
        skill1_normal_damage, skill1_crit_damage, skill1_expectation_damage, skill2_normal_damage, skill2_crit_damage, skill2_expectation_damage, skill3_normal_damage, skill3_crit_damage, skill3_expectation_damage, DPM = results
        data = f"卡1未暴击伤害：{skill1_normal_damage}\n卡1暴击伤害：{skill1_crit_damage}\n卡1期望伤害：{skill1_expectation_damage}\n\n卡2未暴击伤害：{skill2_normal_damage}\n卡2暴击伤害：{skill2_crit_damage}\n卡2期望伤害：{skill2_expectation_damage}\n\n仪式未暴击伤害：{skill3_normal_damage}\n仪式暴击伤害：{skill3_crit_damage}\n仪式期望伤害：{skill3_expectation_damage}\n\n期望DPM：{DPM}"
        self.result_info_text.setPlainText(data)

