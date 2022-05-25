import os
import sys
import base64
import tempfile
import pyautogui
import win32gui
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.qt import QtScheduler
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore


def autocheckin():
    aimg = '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'
    
    bimg = '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'

    os.chdir(tempfile.gettempdir())
    with open('a.png', 'wb') as f:
        f.write(base64.b64decode(aimg))
        
    with open('b.png', 'wb') as f:
        f.write(base64.b64decode(bimg))
        

    win = pyautogui.getWindowsWithTitle('钉钉')
    if win:
        win[0].restore()
        # win[0].activate()
        win32gui.SetForegroundWindow(win[0]._hWnd)
        win[0].moveTo(100, 200)
        pyautogui.moveTo(200, 300)
        while not pyautogui.locateCenterOnScreen('a.png') and not globals().get('stop_job'):
            pyautogui.scroll(10)
            
    pyautogui.sleep(1)  
    pyautogui.click(pyautogui.locateCenterOnScreen('a.png'))
    pyautogui.sleep(1)
    while not pyautogui.locateCenterOnScreen('b.png') and not globals().get('stop_job'):
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
        
        self.setWindowState(QtCore.Qt.WindowActive)

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
        
        self.runing_label = QLabel("运行中")
        self.runing_label.setStyleSheet("margin-left: 5px;color: green")
        self.statusbar.addWidget(self.runing_label, 1)
        self.runing_label.hide()

        self.timer = QtCore.QTimer()
        self.datetime_label = QLabel()
        # self.datetime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.statusbar.addPermanentWidget(self.datetime_label, 0)
        self.datetime_label.setText(QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd'))
        self.timer.timeout.connect(self.show_statusbar_message)
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
        
        if self.sched.get_job('checkin'):
            self.input_datetime.setDateTime(self.sched.get_job('checkin').next_run_time)
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
    
    def show_statusbar_message(self):
        self.datetime_label.setText(QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd'))
        if self.sched.get_job('checkin'):
            if self.runing_label.isHidden():
                self.runing_label.show()
            else:
                self.runing_label.hide()

    def start(self):
        if self.sched.get_job('checkin'):
            QMessageBox.warning(self, '提示', '自动签到已经开启！')
        else:
            globals()['stop_job'] = False
            self.sched.add_job(autocheckin, 'cron', day_of_week=str(self.input_datetime.dateTime().date().dayOfWeek() - 1), hour=self.input_datetime.dateTime().time().hour(), minute=self.input_datetime.dateTime().time().minute(), id='checkin')
            QMessageBox.information(self, '提示', '开启成功！')
            self.runing_label.show()

    def stop(self):
        if self.sched.get_job('checkin'):
            globals()['stop_job'] = True
            self.sched.remove_job('checkin')
            QMessageBox.information(self, '提示', '关闭成功！')
            self.runing_label.hide()
        else:
            QMessageBox.warning(self, '提示', '未开启自动签到！')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
