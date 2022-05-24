## build

~~~~shell
git clone https://github.com/GavinTan/checkinbot.git

pip install SQLAlchemy==1.4.36 PyQt5==5.15.6 APScheduler==3.9.1 PyAutoGUI==0.9.53 pyinstaller==5.1

cd checkinbot

pyinstaller -Fw --noupx --clean -y -i .\icon\icon.ico --add-data ".\\ui\\*;ui" --add-data ".\\icon\*;icon" checkinbot.py
~~~~

