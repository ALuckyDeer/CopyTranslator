import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QTextBrowser, QDialog
from PyQt5 import QtGui, QtCore, Qt
from translator import Translater
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import QTimer

app = QApplication(sys.argv)


class tUI(QWidget):
    def __init__(self,):
        super().__init__()

        self.timer = QTimer(self)

        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.change_deal)
        self.initUI()

    def initUI(self):
        try:
            self.setGeometry(300, 300, 300, 200)
            self.width = 250 #宽
            self.height = 200 #高
            self.baseB=20 #增间距
            self.baseTime=5 #设置的时间
            self.timerStart=True #True 开启计时器
            self.setFixedWidth(self.width)
            self.setFixedHeight(self.height)

            self.text_browser = QTextBrowser(self)
            self.text_browser.move(0, 0)
            self.text_browser.resize(self.width, self.height)

            self.setWindowTitle('复制翻译器')
            # 去掉所有按钮
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
            self.translater = Translater()
            self.hide()
        except Exception as e:
            print(e)

    def setBaseTime(self,baseTime):
        try:
            self.baseTime = baseTime
        except Exception as e:
            print(e)


    def setTimerStart(self,timeStart):
        try:
            self.timerStart = timeStart
        except Exception as e:
            print(e)


    def leaveEvent(self,e):
        try:
            self.hide()
        except Exception as e:
            print(e)


    def keyPressEvent(self, e):
        try:
            keyEvent = QKeyEvent(e)
            ctrl = e.modifiers() & Qt.ControlModifier
            shift = e.modifiers() & Qt.ShiftModifier
            if keyEvent.key() == QtCore.Qt.Key_Escape:
                self.hide()
            # ctrl+c 粘贴处理过的字符串，ctrl+shift+c处理原生选择的数据
            elif ctrl and keyEvent.key() == QtCore.Qt.Key_C:
                self.clipboard.setText(self.query.word.text)
            elif ctrl and keyEvent.key() == QtCore.Qt.Key_C and shift:
                self.clipboard.setText(self.query.word.raw_text)
        except Exception as e:
            print(e)


    def focusOutEvent(self, event):
        """窗口焦点不在当前的翻译窗口时，窗口隐藏起来"""
        try:
            self.hide()
            pass
        except Exception as e:
            print(e)


    def refresh_window(self, text):
        try:
            """更新翻译的显示"""
            # 设置位置和大小
            self.setFixedSize(self.width, self.height)
            cur = QtGui.QCursor.pos()
            self.x = cur.x() - self.baseB
            self.y = cur.y() - self.baseB
            # 如果超出了屏幕边界，便显示在里面
            window_h = QDesktopWidget().screenGeometry().height()
            window_w = QDesktopWidget().screenGeometry().width()
            if self.x + self.width > window_w:
                self.x = window_w - self.width
            if self.y + self.height > window_h:
                self.y = window_h - self.height
            if self.x + self.height > window_h and self.y + self.width > window_w:
                # self.x -= self.baseB + self.width
                # self.y -= self.baseB + self.height
                self.x = window_w - self.width
                self.y = window_h - self.height
            self.move(self.x, self.y)
            self.show()

            if self.timerStart == True:
                print(self.baseTime * 1000)
                # 计时自动关闭窗口
                self.timer.timeout.connect(self.hide)  # 每次计时到时间时发出信号
                self.timer.start(self.baseTime * 1000)  # 设置计时间隔并启动；单位毫秒

            base_info = ''
            for x in self.translater.word.props:
                base_info += x + self.translater.word.props[x] + '\n\n'
            # print(base_info)
            if base_info is '':
                self.text_browser.append("翻译:" + '\n\n' + "无结果")
            else:
                self.text_browser.append("翻译:" + '\n\n' + base_info)
        except Exception as e:
            print(e)


    # 当剪切板变动会执行该方法
    def change_deal(self):
        try:
            data = self.clipboard.mimeData()
            if data.text is None:
                return
            #print(data.text())
            translate_results = self.translater.get(data.text())

            self.text_browser.clear()
            self.text_browser.setText("原词:"+'\n\n'+data.text()+'\n')
            self.refresh_window(translate_results)
            #print(translate_results);
        except Exception as e:
            print(e)


# if __name__ == '__main__':
#     # 监听剪切板变动
#     window = Window()
#     sys.exit(app.exec_())
