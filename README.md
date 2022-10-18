## build

~~~~shell
git clone https://github.com/GavinTan/checkinbot.git

pip install SQLAlchemy==1.4.36 PyQt5==5.15.6 APScheduler==3.9.1 PyAutoGUI==0.9.53 pyinstaller==5.1

cd checkinbot

#python3.9已经不支持win7，win7环境下需要使用3.9以下版本打包
pyinstaller -Fw --clean -y -i .\icon\icon.ico --add-data ".\\ui\\*;ui" --add-data ".\\icon\*;icon" checkinbot.py
~~~~

## 使用
修改checkinbot.py脚本里的aimg为钉钉群名称截图对应的base64，还需设置屏幕不锁定和睡眠不然无法正常工作。开启自动签到后会自动切换钉钉对应群里开始检测签到消息匹配到自动点击。
