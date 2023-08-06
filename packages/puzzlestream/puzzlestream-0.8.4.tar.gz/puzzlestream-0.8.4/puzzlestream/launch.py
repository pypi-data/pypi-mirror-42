import ctypes
import sys
from multiprocessing import current_process
from os import mkdir, name, path
from time import time

import matplotlib
import pkg_resources
from appdirs import user_config_dir

matplotlib.use("Qt5Agg")

if current_process().name == "MainProcess":
    import sys
    from PyQt5 import QtCore, QtGui, QtWidgets


def setStdout():
    if name == "nt":
        configDir = user_config_dir()
    else:
        configDir = user_config_dir("Puzzlestream")
    if not path.exists(path.join(configDir, "pslogs")):
        mkdir(path.join(configDir, "pslogs"))
    sys.stdout = open(path.join(configDir, "pslogs/%d.log" % (time())), "w")
    sys.stderr = open(path.join(configDir, "pslogs/%d.log" % (time())), "w")
    print("--- Starting Puzzlestream at %d on %s ---" % (time(), name))
    print("Package set:")
    pkg_resources._initialize_master_working_set()
    for p in pkg_resources.working_set:
        print(p.key, "(%s)" % (p.version))
    print("\n--- Output ---")
    sys.stdout.flush()
    sys.stderr.flush()


def main():
    """ Create Application and MainWindow. """
    global app, psMainWindow

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_CompressHighFrequencyEvents
    )
    app = QtWidgets.QApplication(sys.argv)
    currentDir = path.dirname(__file__)

    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "puzzlestream")
    desktopWidget = app.desktop()
    desktopGeometry = desktopWidget.screenGeometry()

    app.setWindowIcon(QtGui.QIcon(
        path.join(currentDir, "icons/Puzzlestream.png")))
    app.setApplicationName("Puzzlestream")
    app.setApplicationDisplayName("Puzzlestream")

    splash_pix = QtGui.QPixmap(
        path.join(currentDir, "icons/Puzzlestream.png"))

    splash_pix = splash_pix.scaled(
        0.5*splash_pix.width()*desktopGeometry.width()/1080,
        0.5*splash_pix.height()*desktopGeometry.width()/1080,
        transformMode=QtCore.Qt.SmoothTransformation)
    splash = QtWidgets.QSplashScreen(
        splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(
        QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.show()
    app.processEvents()
    from puzzlestream.ui.main import PSMainWindow
    psMainWindow = PSMainWindow()
    splash.finish(psMainWindow)
    return app.exec_()


if __name__ == "__main__":
    setStdout()
    sys.exit(main())
