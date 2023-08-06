import json
import sys
from distutils.version import LooseVersion
from os import cpu_count, path
from subprocess import PIPE, Popen
from threading import Lock, Thread
from time import time
from urllib.request import urlopen

import pkg_resources
from bs4 import BeautifulSoup
from puzzlestream.ui.outputtextedit import PSOutputTextEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ListModel(QAbstractTableModel):
    def __init__(self, data, parent=None, *args):
        """ data: a list where each item is a row """
        QAbstractListModel.__init__(self, parent, *args)
        self.setData(data)

    def setData(self, data):
        self.listData = data

    def rowCount(self, parent=QModelIndex()):
        return len(self.listData)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listData[index.row()])
        else:
            return QVariant()


class PSPipGUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1000, 600)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.__layout = QGridLayout()
        self.widget.setLayout(self.__layout)

        self.lblAvailable = QLabel("Available")
        self.lblInstalled = QLabel("Installed")
        self.lblUpdates = QLabel("Updates")

        for l in [self.lblAvailable, self.lblInstalled, self.lblUpdates]:
            l.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.listAvailable = QTableView()
        self.listInstalled = QTableView()
        self.listUpdate = QTableView()

        for l in [self.listAvailable, self.listInstalled, self.listUpdate]:
            l.horizontalHeader().setStretchLastSection(True)
            l.horizontalHeader().hide()
            l.verticalHeader().hide()

        self.btnInstall = QPushButton("install ->")
        self.btnUninstall = QPushButton("<- uninstall")
        self.btnUpdate = QPushButton("<- update")
        self.btnInstall.clicked.connect(self.installSelectedPackages)
        self.btnUninstall.clicked.connect(self.uninstallSelectedPackages)
        self.btnUpdate.clicked.connect(self.updateSelectedPackages)
        # for btn in [self.btnInstall, self.btnUpdate]:
        #     btn.setEnabled(False)

        self.pipOutput = PSOutputTextEdit()
        self.pipOutput.setStyleSheet(
            "QTextEdit { min-height: 12em; max-height: 12em; }")

        self.__layout.addWidget(self.lblAvailable, 0, 0)
        self.__layout.addWidget(self.listAvailable, 1, 0, 4, 1)
        self.__layout.addWidget(self.btnInstall, 2, 1)
        self.__layout.addWidget(self.btnUninstall, 3, 1)
        self.__layout.addWidget(self.lblInstalled, 0, 2)
        self.__layout.addWidget(self.listInstalled, 1, 2, 4, 1)
        self.__layout.addWidget(self.btnUpdate, 2, 3, 2, 1)
        self.__layout.addWidget(self.lblUpdates, 0, 4)
        self.__layout.addWidget(self.listUpdate, 1, 4, 4, 1)
        self.__layout.addWidget(self.pipOutput, 5, 0, 1, 5)

        self.__updateThreads = []
        self.__updateTimer = QTimer()
        self.__updateTimer.setInterval(2000)
        self.__updateTimer.timeout.connect(self.__updateListWidgets)

        self.__currentProcess = None
        self.__newOutput = ""
        self.__currentlyRunning = ""
        self.__updateBackgroudThread = None
        self.__threadLock = Lock()
        self.__outputTimer = QTimer()
        self.__outputTimer.setInterval(100)
        self.__outputTimer.timeout.connect(self.__updateOutput)

        self.updateAvailable()
        self.updateInstalled()
        self.updateUpdates()

    def updateAvailable(self):
        self.__available = []
        thr = Thread(target=self.__updateAvailableBG)
        thr.start()
        currentDir = path.dirname(__file__)
        mov = QMovie(path.join(currentDir, "../icons/loading.gif"))
        mov.start()
        self.lblAvailable.setMovie(mov)
        self.__updateThreads.append(thr)
        self.__updateTimer.start()

    def __updateAvailableBG(self):
        with urlopen('https://pypi.python.org/simple/') as source:
            soup = BeautifulSoup(source.read(), 'lxml')

        l = []
        for i in soup.find_all('a'):
            l.append(i['href'])

        self.__available = [s[8:-1] for s in l]

    def updateInstalled(self):
        pkg_resources._initialize_master_working_set()
        installed = ["%s (%s)" % (p.key, p.version)
                     for p in pkg_resources.working_set]

        m = ListModel(sorted(installed))
        self.listInstalled.setModel(m)

    def updateUpdates(self):
        self.__updates = []
        self.listUpdate.setModel(ListModel([]))
        thr = Thread(target=self.__checkUpdatesBG)
        thr.start()
        currentDir = path.dirname(__file__)
        mov = QMovie(path.join(currentDir, "../icons/loading.gif"))
        mov.start()
        self.lblUpdates.setMovie(mov)
        self.__updateThreads.append(thr)
        self.__updateTimer.start()

    def __checkUpdatesBG(self):
        threads = []
        for p in pkg_resources.working_set:
            thr = Thread(target=self.__checkUpdate, args=(p,))
            thr.start()
            threads.append(thr)

            while len(threads) > cpu_count() - 1:
                threads.pop(0).join()

        for thr in threads:
            thr.join()

    def __checkUpdate(self, p):
        try:
            with urlopen("https://pypi.org/pypi/%s/json" % (p.key)) as res:
                version = json.loads(res.read())["info"]["version"]
                if LooseVersion(version) > LooseVersion(p.version):
                    self.__updates.append((p, version))
        except Exception as e:
            print(p.key, e)

    def __updateListWidgets(self):
        for t in self.__updateThreads:
            if not t.isAlive():
                self.__updateThreads.pop(self.__updateThreads.index(t))

        if len(self.__updateThreads) > 0:
            self.__updates.sort(key=lambda x: x[0].key)
            m = ["%s (%s)" % (p[0].key, p[1]) for p in self.__updates]
            self.listUpdate.model().setData(m)
            self.listUpdate.model().layoutChanged.emit()

        if len(self.__updateThreads) == 0:
            self.lblUpdates.setText("Updates")
            self.__updateTimer.stop()
            self.__available = sorted(self.__available)
            m = ListModel(self.__available)
            self.listAvailable.setModel(m)
            self.lblAvailable.setText("Available")

    def installSelectedPackages(self):
        packages = [self.__available[ind.row()]
                    for ind in
                    self.listAvailable.selectionModel().selectedIndexes()]
        self.__currentlyRunning = "install"
        self.__runPipCommand(
            [sys.executable, "-m", "pip", "install", "--user"] + packages)

    def uninstallSelectedPackages(self):
        installed = sorted([p.key for p in pkg_resources.working_set])
        packages = [installed[ind.row()] for ind in
                    self.listInstalled.selectionModel().selectedIndexes()]
        self.__currentlyRunning = "uninstall"
        self.__runPipCommand(
            [sys.executable, "-m", "pip", "uninstall", "-y"] + packages)

    def updateSelectedPackages(self):
        packages = [self.__updates[ind.row()][0].key for ind in
                    self.listUpdate.selectionModel().selectedIndexes()]
        self.__currentlyRunning = "update"
        self.__runPipCommand(
            [sys.executable, "-m", "pip", "install", "--user", "--upgrade"] +
            packages
        )

    def __updateOutput(self):
        if self.__currentProcess is not None:
            if self.__newOutput == "":
                Thread(target=self.__getNewOutput).start()

            if self.__currentProcess.poll() is not None:
                self.updateInstalled()

                if self.__currentlyRunning == "update":
                    self.updateUpdates()

                self.__currentProcess = None
                self.__currentlyRunning = ""
                self.__outputTimer.stop()

        self.__threadLock.acquire()
        if self.__newOutput != "":
            self.pipOutput.insertPlainText(self.__newOutput)
            self.__newOutput = ""
        self.__threadLock.release()

    def __runPipCommand(self, command: list):
        self.pipOutput.setPlainText("")
        self.__newOutput = ""
        self.__outputTimer.start()
        self.__currentProcess = Popen(command, stdout=PIPE, stderr=PIPE)

    def __getNewOutput(self):
        t = self.__currentProcess.stdout.readline().decode("utf-8")
        self.__threadLock.acquire()
        self.__newOutput += t
        self.__threadLock.release()
