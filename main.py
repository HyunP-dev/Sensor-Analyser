import sys
from typing import Union

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QLineEdit, QMainWindow, QTextBrowser, QToolBar,
                             QVBoxLayout, QWidget,
                             QHBoxLayout, QFrame, QSplitter, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import Qt
import os
import plotly
import pandas as pd
import re

from widgets import FileTreeWidget

pd.options.plotting.backend = "plotly"


def convert_bytes(num: float):
    """
    this function will convert bytes to MB.... GB... etc

    https://stackoverflow.com/questions/2104080/how-can-i-check-file-size-in-python
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


class SensorAnalyserView(QWidget):
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.initUI()

    def onItemClicked(self):
        selectedItem = self.treeWidget.selectedItems()[0]
        filepath = selectedItem.filepath
        print(filepath)

        if filepath.endswith(".csv"):
            self.dataset = pd.read_csv(filepath)
            print("selectedItem.text(0):", selectedItem.text(0))
            try:
                if re.fullmatch("(sc)\d(_)(ss|lg)(.csv)", selectedItem.text(0)) is not None:
                    print("matched!")
                    fig = self.dataset[["Gx", "Gy", "Gz"]].plot()
                else:
                    fig = self.dataset[["gx", "gy", "gz"]].plot()

                html = '<html><head><meta charset="utf-8" />'
                html += '<body>'
                html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn',
                                            config={"displaylogo": False, 'modeBarButtonsToRemove': ['toImage']})
                html += '</body></html>'
                self.view.setHtml(html)
            except KeyError:
                print("KeyError Occured.")

    def showFileDetail(self):
        self.tb.clear()
        selectedItem = self.treeWidget.selectedItems()[0]
        filepath = selectedItem.filepath
        if os.path.isdir(filepath):
            self.tb.setText(SensorAnalyserView.fileDetail(selectedItem.text(0), os.path.getsize(filepath), "folder"))
        else:
            self.tb.setText(
                SensorAnalyserView.fileDetail(selectedItem.text(0), os.path.getsize(filepath), filepath.split(".")[-1]))
        pass

    def fileDetail(filename: str, size: int, type: str) -> str:
        return f"<p align='center'><br><b>filename</b><br>{filename}<br><br><b>size</b><br>{convert_bytes(size)}<br><br><b>type</b><br>{type}</p>"

    def refresh(root_dir: str, parentItem: Union[QTreeWidgetItem, QTreeWidget]):
        files = os.listdir(root_dir)
        for file in files:
            fitem = QTreeWidgetItem(parentItem)
            path = os.path.join(root_dir, file)
            fitem.filepath = path
            fitem.setText(0, file)
            if os.path.isdir(path):
                SensorAnalyserView.refresh(path, fitem)

    def initUI(self):
        hbox = QHBoxLayout()
        self.treeWidget = FileTreeWidget(self, "./")
        self.treeWidget.itemDoubleClicked.connect(self.onItemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.showFileDetail)

        # SensorAnalyserView.refresh("./", self.treeWidget)

        leftPanel = QFrame()
        leftPanel.setFrameShape(QFrame.WinPanel)
        leftPanel.setFrameShadow(QFrame.Sunken)
        leftHBox = QHBoxLayout()
        leftHBox.setContentsMargins(0, 0, 0, 0)
        leftHBox.setSpacing(0)

        leftPanel.setLayout(leftHBox)
        leftSplitter = QSplitter(Qt.Vertical)
        leftHBox.addWidget(leftSplitter)

        lupFrame = QFrame()

        lbtFrame = QFrame()
        lbtFrame.setFrameShape(QFrame.WinPanel)
        lbtFrame.setFrameShadow(QFrame.Sunken)

        leftSplitter.addWidget(lupFrame)
        leftSplitter.addWidget(lbtFrame)

        lbtHBox = QHBoxLayout()
        lbtHBox.setContentsMargins(0, 0, 0, 0)
        lbtHBox.setSpacing(0)

        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)

        self.tb.append("")
        self.tb.append("")

        lbtHBox.addWidget(self.tb)
        lbtFrame.setLayout(lbtHBox)

        lupHBox = QVBoxLayout()
        lupHBox.setContentsMargins(0, 0, 0, 0)
        lupHBox.setSpacing(0)

        lupFrame.setLayout(lupHBox)
        self.edit = QLineEdit()
        self.edit.setFrame(True)
        self.edit.setText(os.path.abspath("./"))
        lupHBox.addWidget(self.edit)
        lupHBox.addWidget(self.treeWidget)

        rightPanel = QFrame()

        rightPanel.setFrameShape(QFrame.WinPanel)
        rightPanel.setFrameShadow(QFrame.Sunken)

        self.view = QWebEngineView()

        self.view.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.view.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)

        rightHBox = QHBoxLayout()

        rightHBox.setContentsMargins(0, 0, 0, 0)
        rightHBox.setSpacing(0)
        rightHBox.addWidget(self.view)

        rightPanel.setLayout(rightHBox)

        html = '<html><head><meta charset="utf-8" />'
        html += '<body>'
        html += "<h1>Welcome to Sensor Analyser</h1>"
        html += "This program is writen by Park Hyun to study about pedometer algorithm."
        html += '</body></html>'
        self.view.setHtml(html)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(leftPanel)
        splitter1.addWidget(rightPanel)

        print(splitter1.sizes())
        splitter1.setSizes([int(1000 * 2 / 10), int(1000 * 8 / 10)])
        print(splitter1.sizes())

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Analyser")
        self.initUI()

    def initUI(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(toolbar)

        low_pass_filter_btn = QAction(QIcon("icons/lpf.png"), "Low Pass Filter", self)
        low_pass_filter_btn.triggered.connect(lambda self: print("Button Clicked"))

        hist_btn = QAction(QIcon("icons/hist.png"), "Histogram", self)
        hist_btn.triggered.connect(lambda self: print("Button Clicked"))

        toolbar.addAction(low_pass_filter_btn)
        toolbar.addAction(hist_btn)

        self.setGeometry(300, 300, 1000, 600)
        centralWidget = SensorAnalyserView()
        self.setCentralWidget(centralWidget)

    def show(self):
        super().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
