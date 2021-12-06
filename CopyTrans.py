import sys
# 从PyQt库导入QtWidget通用窗口类,基本的窗口集在PyQt5.QtWidgets模块里.
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu, QMessageBox,QVBoxLayout,QLabel,QSpinBox,QPushButton,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt
from tui import tUI
import urllib3
import queue


class Trans(QWidget):
    def __init__(self, parent=None):
        super(Trans, self).__init__(parent)
        self.initUI()
        self.initArg()
        self.child = tUI()


    def initUI(self):
        self.setWindowTitle('复制翻译器')
        self.setFixedSize(300, 100)
        self.setWindowIcon(QIcon("./logo.ico"))
        # show()方法将窗口显示在屏幕上.一个窗口是先在内存中被创建,然后显示在屏幕上的.
        self.tpMenu = QMenu()


        self.layout = QVBoxLayout(self)
        self.label = QLabel("翻译框最长显示时间:")
        self.label.setAlignment(Qt.AlignVCenter)
        self.layout.addWidget(self.label)

        self.helpButton=QPushButton(self)
        self.helpButton.setText("不懂点我")
        self.helpButton.clicked.connect(self.message)
        self.helpButton.move(200,17)
        self.helpButton.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")


        self.sp = QSpinBox(self)
        self.sp.setMaximum(20)#最长20秒
        self.sp.setMinimum(1)#最小1秒
        self.sp.setValue(5)#默认5秒
        self.layout.addWidget(self.sp)
        self.sp.valueChanged.connect(self.changedValue)
        self.setLayout(self.layout)



    def initArg(self):
        try:
            # 在系统托盘处显示图标
            self.tp = QSystemTrayIcon(self)
            self.tp.setIcon(QIcon('./logo.ico'))
            # 设置系统托盘图标的菜单
            self.a1 = QAction('&显示(Show)', triggered=self.show)
            self.a2 = QAction('&退出(Exit)', triggered=self.quitApp)  # 直接退出可以用qApp.quit
            self.tpMenu.addAction(self.a1)
            self.tpMenu.addAction(self.a2)
            self.tp.setContextMenu(self.tpMenu)
            # 不调用show不会显示系统托盘
            self.tp.show()
            # 信息提示
            # 参数1：标题
            # 参数2：内容
            # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标

            self.tp.showMessage('复制翻译器', '已经启动啦！', icon=0)
            #self.tp.messageClicked.connect(self.message)
            self.tp.activated.connect(self.act)
        except Exception as e:
                print(e)



    def changedValue(self):
        try:
             self.child.setBaseTime(self.sp.value())
             self.label.setText("翻译框最长显示时间:" + str(self.sp.value()))
            # 监听剪切板变动
        except Exception as e:
            print(e)


    def act(self,reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.show()
        # print("系统托盘的图标被点击了")

    def message(self):
        self.msgBox=QMessageBox()
        self.msgBox.information(self,'帮助','使用说明: \n'
                                          '①启动后点击关闭按钮在右下角进行托盘，\n②选中文本后复制即可跟随鼠标查看翻译\n(ctrl+c '
                                          '或鼠标右键都可以)\n③可以更改翻译框的显示时间.\n④翻译框会在鼠标移入之后移出消失，\n⑤也会在设置的时间过了之后消失')
    def quitApp(self):
        try:
            if self.child is not None:
                self.child.close()
            self.show()  # w.hide() #隐藏
            re = QMessageBox.question(self, "提示", "退出系统?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
            if re == QMessageBox.Yes:
                # 关闭窗体程序
                QCoreApplication.instance().quit()
                # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
                # 直到你的鼠标移动到上面去后，才会消失，
                # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
                # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
                self.tp.setVisible(False)
        except Exception as e:
            print(e)
if __name__ == '__main__':
    # pyqt窗口必须在QApplication方法中使用 
    # 每一个PyQt5应用都必须创建一个应用对象.sys.argv参数是来自命令行的参数列表.Python脚本可以从shell里运行.这是我们如何控制我们的脚本运行的一种方法.
    app = QApplication(sys.argv)
    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)
    m=Trans()
    m.show()


    # sys为了调用sys.exit(0)退出程序
    # 最后,我们进入应用的主循环.事件处理从这里开始.主循环从窗口系统接收事件,分派它们到应用窗口.如果我们调用了exit()方法或者主窗口被销毁,则主循环结束.sys.exit()方法确保一个完整的退出.环境变量会被通知应用是如何结束的.
    # exec_()方法是有一个下划线的.这是因为exec在Python中是关键字.因此,用exec_()代替.
    sys.exit(app.exec_())