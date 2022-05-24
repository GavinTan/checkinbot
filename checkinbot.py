import os
import sys
import base64
import tempfile
import pyautogui
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.qt import QtScheduler
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore


def autocheckin():
    aimg = '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'
    # aimg = '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'
    
    bimg = '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'

    os.chdir(tempfile.gettempdir())
    with open('a.png', 'wb') as f:
        f.write(base64.b64decode(aimg))
        
    with open('b.png', 'wb') as f:
        f.write(base64.b64decode(bimg))
        

    win = pyautogui.getWindowsWithTitle('钉钉')
    if win:
        win[0].restore()
        try:
            win[0].activate()
        except:
            win[0].minimize()
            win[0].restore()
            
        win[0].moveTo(100, 200)
        while not pyautogui.locateCenterOnScreen('a.png'):
            pyautogui.moveTo(200, 300)
            pyautogui.scroll(10)
            
    pyautogui.sleep(1)  
    pyautogui.click(pyautogui.locateCenterOnScreen('a.png'))
    pyautogui.sleep(1)
    while not pyautogui.locateCenterOnScreen('b.png'):
        if pyautogui.locateCenterOnScreen('b.png'):
            pyautogui.click(pyautogui.locateCenterOnScreen('b.png'))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        if getattr(sys, 'frozen', False):
            # 打包后的资源路径
            bundle_dir = sys._MEIPASS
        else:
            # 直接运行脚本资源路径
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        loadUi(bundle_dir + '/ui/main.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())

        self.setWindowIcon(QIcon(bundle_dir + '/icon/icon.ico'))
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon(bundle_dir + '/icon/icon.ico'))
        self.tray_icon.setToolTip('签到神器')

        show_action = QAction("打开", self)
        quit_action = QAction("退出", self)
        show_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(lambda: (self.stop(), qApp.quit()))
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated[QSystemTrayIcon.ActivationReason].connect(self.iconActivated)
        
        self.runing_label = QLabel("运行中。。")
        self.runing_label.setStyleSheet("margin-left: 5px;color: green")

        self.timer = QtCore.QTimer()
        self.datetime_label = QLabel()
        # self.datetime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.statusbar.addPermanentWidget(self.datetime_label, 0)
        self.datetime_label.setText(QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd'))
        self.timer.timeout.connect(lambda: self.datetime_label.setText(QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd')))
        self.timer.start(1000)

        self.input_datetime.setDate(self.calendar_widget.selectedDate())
        self.calendar_widget.clicked[QtCore.QDate].connect(lambda date: self.input_datetime.setDate(date))
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        
        
        jobstores = {
            'default': SQLAlchemyJobStore(url=f"sqlite:///{os.path.join(os.path.expanduser('~'), 'checkinbot.db')}")
            }
        self.sched = QtScheduler(jobstores=jobstores, timezone='Asia/Shanghai', daemon=True)
        self.sched.start()
        
        if self.sched.get_job('autosign'):
            self.input_datetime.setDateTime(self.sched.get_job('autosign').next_run_time)
            self.statusbar.addWidget(self.runing_label, 1)
        else:
            self.input_datetime.setTime(QtCore.QTime.fromString("10:00:00", "hh:mm:ss"))
        
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()
                self.tray_icon.showMessage(
                    "提示",
                    "签到程序已在后台运行，点击系统托盘图标打开！",
                    QSystemTrayIcon.Information,
                    2000
                )
                
    def closeEvent(self, event):
        event.accept()
        self.tray_icon.hide()
        os._exit(0)

    def iconActivated(self, reason):
        if reason == self.tray_icon.Trigger & QSystemTrayIcon.DoubleClick:
            self.setWindowState(QtCore.Qt.WindowActive)
            self.showNormal()

    def start(self):
        if self.sched.get_job('autosign'):
            QMessageBox.warning(self, '提示', '自动签到已经开启！')
        else:
            self.sched.add_job(autocheckin, 'cron', day_of_week=str(self.input_datetime.dateTime().date().dayOfWeek() - 1), hour=self.input_datetime.dateTime().time().hour(), minute=self.input_datetime.dateTime().time().minute(), id='autosign')
            QMessageBox.information(self, '提示', '开启成功！')
            self.statusbar.addWidget(self.runing_label, 1)
            self.runing_label.show()

    def stop(self):
        if self.sched.get_job('autosign'):
            self.sched.remove_job('autosign')
            QMessageBox.information(self, '提示', '关闭成功！')
            self.statusbar.removeWidget(self.runing_label)
        else:
            QMessageBox.warning(self, '提示', '未开启自动签到！')
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
