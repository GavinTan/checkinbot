## build

~~~~shell
git clone https://github.com/GavinTan/checkinbot.git

pip install SQLAlchemy==1.4.36 PyQt5==5.15.6 APScheduler==3.9.1 PyAutoGUI==0.9.53 pyinstaller==5.1

cd checkinbot

#python3.9已经不支持win7，win7环境下需要使用3.9以下版本打包
pyinstaller -Fw --clean -y -i .\icon\icon.ico --add-data ".\\ui\\*;ui" --add-data ".\\icon\*;icon" checkinbot.py
~~~~

