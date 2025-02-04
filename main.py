from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Calculator
import sys

if __name__ == "__main__":
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Calculator()
    mainWindow.show()
    sys.exit(app.exec_())



# pyinstaller --add-data 'db:db'-F  -w -i D:\Project\Python\Calculator1999\images\logo_yellow.ico -n "暴雨科算v3.0" main.py