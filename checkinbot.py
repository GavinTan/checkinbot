import os
import sys
import base64
import tempfile
import pyautogui
import traceback
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.qt import QtScheduler
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore


class _Signals(QtCore.QObject):
    showlog = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__() 
        
trigger =  _Signals()
  
def autocheckin():
    trigger.showlog.emit(f"{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')} 开始自动签到")
    aimg = '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'
    # aimg = 'iVBORw0KGgoAAAANSUhEUgAAAJEAAAAcCAYAAABh9l0lAAAHN0lEQVRoge1af0iVVxh+rpqVmaslIRtlpm7Ma+H6wWKNrmEyw8wYgRIkFzI2s2K4sGCFXPSPKU2itWrk4FIQNvpDW5JbRl7/GqyGpNdYal6NhmyJdhW3THPvOee79373u993f/gVbfA9oN7v/Prec85z3vc579X015ORWRgwoANRr9sAA/9/GCQyoBsGiQzohkEiA7phkMiAbhgkMqAbBokM6EbM6zbAgDoW392PmLE7iJ4cmlP/mbiVmEnIhHvjpZdsWSBMRrLxv4Uljmw8T9yM6aXrMb1kAyfDXMDIF+3uxrzRu4gdbsHo1l9esqU+hE+iwYsoaliFK9VbAEcVMg81h+6TUYGWxhIkB1R04Piaw+j94hquWIMv0qB9D/L7P0M3e68MjhNZOJsavD/rW4mvUIdjyK/vmYOdEHM9l6pZz+1TGdtcQbZtbUfRUaDO25fN+xZyu2ywqIzFCDS+/gJm4tP5c3TfbixCIaLufx4YMhJOYdSyFzN4hDhHA6YtNkxNXELCcDbcaSv8mkY9+5M8WymefnhNew10IPxwllyCA8hCkZ1tnA3d92xSBS1MsQv72ULRghcN7AtJDGALarpO04LuxPGUTtSorSjHEG639mBX2RZFeQduNhXiQJfae3wbtcpjuvUyuq2B9eqvFQTHmWB2+SDGHoK9+BhQexnWZIngvLIEV2rp8BVfRF0tULmjn2xWf+/S25vg/uAH4XmGq7BkohTjrCJ+L8YK9vI20X1VmJ9kw2S8rONEO2IX52IyiI0v5i/nYY2941V4pIg0kaX6GgaKv4fDuo/+7sRJ2QFsWlsvfWpGpvTRXHEa21sP+7Xzg4l+DmWhSVnOPANf9Ho45W1mC/EtI4f9PJpMPfROmTeczcCR62IT9WCQjW2m94dBIEZyu3wdCrJw0lu3E0WtGXD2iMr8AvD5ljObC08HeNappHyN0MU8TRbi3NLj/TOIY+03jsCdBMQ+IC/1GEh87OuReF82rtRudt4b+Hv1p+FMKmJEKKxXwtrIPNAQBuj3rm/YaVX3RCKUrKL2nbCyriwcap5E/5MMqT3M8jAjPAgrr/w6nch0WTaO1F8Twrs0maRHE3wElJOPj02bTgTN9x4KAeWzh9Bifmz880i7LvNEfqE2uPdL/HFZCAF8EO4CG2Y8nmiiCgmsmDxWwjiFtQIW1gga4cyD6aUb+LueFIwEeVfkCJtE9uIsceK4fsjmZU0yL6LuiWQDJGdju7keNx20kMqVHGzHDeShLqQX6cXZo7T5pKXCchR+oE2/xzZRvqFy8lE583y7FF4iXE3ECCrzRGzufnpJRlyulxQh//myzRHPKPYPJybX2wSBwsB0wpqI3xEOwiYRP3F8QdkTeaTaCtzQ8izSwtf5LRT1KStEZlsHeS+FSG6oR3pZp7qw9UM6DjSSB2Ljn8iRbbYLfU4gLdzJqMBxgjyVkkBhgGuiFLKnLUelr0eLhdJhhOgFKoVmTMerFEuYWncV+G2ZXyhj8IUz4cGmQs5CH3TmiZpFjFdDRkVgmWUfjpwjMe2QiVYiRHkvebdqlTGc9YowUohcPo4NLQN7kElh1Och0pGiQw9ZqjvRPce+gwO9tBTkgeVLoaJ7giFm9E6AN4p208lICt5vat0InqyTHkKEs7nmnEJBJ4k8IUIBr8dSQniwoh17YGf6wUXtDoK0hcb1Wk0TSWAeoAWku+zZFBrUrXP1UyhJjWA6XLdJYl6BAE3kJUkHLrSSqXRoPFd5kZa4pa3DqG03tfWAaZSFfad8JCLdM8YFtfBE8k2KebCbPM9tEsw2RAqWvHzZeoiPO6dejouw8w8ReiIGdu29Dtosph+EOI1c30hDEZGu8E8ulVoS/+Qg0ret1KjXsK2rxL8spCY6D+TlAa3KmhzU0Nxq+OfQ4WzBo0b8s7oMs1HzRcFwA2LfLqWr+wpMWQRhouln+p2rcHPPo7i1ySC/nfnyScDCh9/h2VufBFmAuSFyEvVQiGkTp9DqXXBx1e0rCye3IglYcwbMTiLhml79V/NBF0luiFDHc1AiIVruJJLOlaFhwtWfjtxSkvwBJIoMLH/DvuqYeP8MEelXJPyehnGLelgSWIFJy0jQ/JAci5xfYuyjn/QZqYGISORoaxa3s223kLn2cGADZc5n1udpvDcVXtYpnVBIIYS8kknl1qKliZRw9RMpU73JRU7Ug80we29xErFkGCB7yj326NJSNj6Hs0pbCyMfi2WrWdZ68t1KTGz6GC8U9TNptrBJw2B6/hTzSGvFPah7ZQRiiDDZ6BOfvow1g5YnGuKpgfIeQZDueyrJNFkIYUTLXNvjTTZqayJFkg8iZ+VNMbGEIbtpBcmcp/hlsUVupzzINzkBmohB/nWJzFahibTHCoYxSzv/++bP7/GvK/SAJRhH8h5ianmOrnFCwfgC1oBuGP9PZEA3DBIZ0A2DRAZ0wyCRAd0wSGRAN/4FzQIlzhozRLMAAAAASUVORK5CYII='
    
    bimg = 'iVBORw0KGgoAAAANSUhEUgAAAFQAAAAcCAYAAAD/YJjAAAADeklEQVRoge1YvW4aQRAeotSJ5CKYSEhO78gusdxYaaxUTnlUceknQPAERn4Cl3EFXaCyaCIaBGUQ6YmExE9jybwAntm5n+W8e7d3twmKc5+Efdzt7s18+83PUtggIIc1vNq1AS8NOaGWkRNqGTmhlpGZ0GUPoNCyYcrLQGZC988BrmcAX3o2zDHACt91A9CcJHyW4V2jBFMKVtomdKAwAFhcIcERw0ao5JOZ4kEZYFPVPH+zva5ujYsjAGcKUF1r1v+E5NwBdKP8cO3wseI59RpAJWqehNeG4/zFowwq3ajvt76is0W+Jsc758EzShmlh+D71nN3o3xMmMyhwkGxzlsk5EpvX6cmjZ2qBRD1zATmhBYDg3YC2tB7TC+fkUwi+legpvYtK3NYC77/PkVlfVSsg3NLYx5LhAnFQ0iZGZA8h5IzcXklIpd1xzzf+5BzJhj9wD9HLkn4Wezx+oJMvLVAok/weonXDqrrYKB4v7spFDGewis4ufVoL++aK9QDOnONRjV726ErY/mTU4NKIXEhrwM53pG+7x8jyZiCGlLeW8w57ZD6HEXot7+zXd073oQtoE9naO9BvCmRSE4o4hJJaUxZDao808dnlOBNE3lSeCFO4d+RNo06js17Vn544whEsqNZk0KfRHKb0bZUhJI6LjBU+6ug2PiYuM6equeKkA+HednsvX6Fx/GLD6hGVFXjXjGwzBVfR6xnp9yZeBGwzNj+pSKUCpSD7UwV85oTip0RFgtqdS5VBQHSh7xHplzhN5qU44HU2KRc/cBpga4boTFyZ0K27UShhDNUCIy5OMmh3Z+xYbEtBxUI3JAOOmrSCFcixqmqOm1A/5B7yLp7T77W9c5ZFZr6pCTCHv/3pepIxpAC6jHKESiyc0lPWPSO8Bza3MaAc7oA9auP+ij5k0h/9HTDfjQPbn0bszpNi1HlkHOqrmVZzp/fo8JD+VGeIzZ3zTmd0B5wDk/TmIvClrKpJ6QOeYJcNT11to7N5nqVuoWVuo2Fpf0uaFnkXEeVPOycg2QV3DZHbJ506KBQr9KJyUSd6+c5VNcKmsL4LC+Kh2ETHoZnqEcigYjyc5578hniZXNP45TB0VcH8S7gTZAhH4llbBWv8Pk+BnZ+HDGEMDTCQNEL6gj9R/BXCf0fkP9ibxk5oZaRE2oZOaGWkRNqGTmhlvEEbXZFz5mOqJQAAAAASUVORK5CYII='

    os.chdir(tempfile.gettempdir())
    with open('a.png', 'wb') as f:
        f.write(base64.b64decode(aimg))
        
    with open('b.png', 'wb') as f:
        f.write(base64.b64decode(bimg))
        

    win = pyautogui.getWindowsWithTitle('钉钉')
    if win:
        try:
            # win[0].restore()
            # win[0].activate()
            os.startfile("D:\Soft\DingDing\DingtalkLauncher.exe")
            win[0].moveTo(100, 200)
            pyautogui.moveTo(200, 300)
            while not pyautogui.locateCenterOnScreen('a.png') and not globals().get('stop_job'):
                pyautogui.scroll(10)
        except Exception as e:
                trigger.showlog.emit(f"{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')} {traceback.format_exc()}")
    pyautogui.sleep(1)  
    pyautogui.click(pyautogui.locateCenterOnScreen('a.png'))
    pyautogui.sleep(1)
    while not globals().get('stop_job'):
        c = 0
        if pyautogui.locateCenterOnScreen('b.png'):
            pyautogui.click(pyautogui.locateCenterOnScreen('b.png'))
            c += 1
            trigger.showlog.emit(f"{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')} 签到成功【{c}】")
        pyautogui.sleep(1)
        

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
        quit_action.triggered.connect(lambda: (self.tray_icon.hide(), os._exit(0)))
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

        self.input_datetime.setCalendarPopup(True)
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
            self.input_datetime.setTime(QtCore.QTime.fromString("09:00:00", "hh:mm:ss"))

        trigger.showlog.connect(lambda msg: self.show_log.append(msg))
        
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
            self.show_log.clear()
        else:
            QMessageBox.warning(self, '提示', '未开启自动签到！')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
