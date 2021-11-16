import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame, QSplitter, QSizePolicy, QTreeWidget, QTreeWidgetItem, QFileSystemModel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
import os
from plotly.graph_objects import Figure, Scatter
import plotly
import numpy as np
import pandas as pd
import re

pd.options.plotting.backend = "plotly"

class SensorAnalyserView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Analyser")
        self.setGeometry(300, 300, 1000, 600)
        
        self.initUI()
    def onItemClicked(self):
        selectedItem = self.treeWidget.selectedItems()[0]
        filepath = selectedItem.filepath
        print(filepath)
        if filepath.endswith(".csv"):
            dataset = pd.read_csv(filepath)
            print("selectedItem.text(0):", selectedItem.text(0))
            try:
                if re.fullmatch("(sc){1}\d(_){1}(ss|lg){1}(.csv){1}", selectedItem.text(0)) != None:
                    print("matched!")
                    fig = dataset[["Gx", "Gy", "Gz"]].plot()  
                else:
                    fig = dataset[["gx", "gy", "gz"]].plot()  
                
                html = '<html><head><meta charset="utf-8" />'
                html += '<body>'
                html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn', config={"displaylogo": False, 'modeBarButtonsToRemove': ['toImage']})
                html += '</body></html>'
                self.view.setHtml(html)
            except KeyError:
                print("KeyError Occured.")

    def showFileDetail(self):
        pass

    def initUI(self):
        hbox = QHBoxLayout()
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.itemDoubleClicked.connect(self.onItemClicked)
        
        def refresh(root_dir, parentItem):
            files = os.listdir(root_dir)
            for file in files:
                fitem = QTreeWidgetItem(parentItem)
                path = os.path.join(root_dir, file)
                fitem.filepath = path
                fitem.setText(0, file)
                if os.path.isdir(path):
                    refresh(path, fitem)

        refresh("./", self.treeWidget)

        leftPanel = QFrame()
        leftPanel.setFrameShape(QFrame.WinPanel)
        leftPanel.setFrameShadow(QFrame.Sunken)
        leftHBox = QHBoxLayout()
        leftHBox.setContentsMargins(0,0,0,0);
        leftHBox.setSpacing(0);
        
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
        lbtHBox.setContentsMargins(0,0,0,0);
        lbtHBox.setSpacing(0);



        
        lupHBox = QHBoxLayout()
        lupHBox.setContentsMargins(0,0,0,0);
        lupHBox.setSpacing(0);
        
        lupFrame.setLayout(lupHBox)
        lupHBox.addWidget(self.treeWidget)

        rightPanel = QFrame()
        
        rightPanel.setFrameShape(QFrame.WinPanel)
        rightPanel.setFrameShadow(QFrame.Sunken)
        

        self.view = QWebEngineView()
        print("view.maximumSize:", self.view.maximumSize())
        print(self.view.frameSize())
        

        
        rightHBox = QHBoxLayout()
        
        
        rightHBox.setContentsMargins(0,0,0,0);
        rightHBox.setSpacing(0);
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
        splitter1.setSizes([int(1000*2/10), int(1000*8/10)])
        print(splitter1.sizes())


        hbox.addWidget(splitter1)
        self.setLayout(hbox)

        
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = SensorAnalyserView()
    sys.exit(app.exec_())
