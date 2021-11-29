from PyQt5.QtWidgets import *
import os
import sys
import plotly
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import Qt


class HistogramViewer(QMainWindow):
    def __init__(self, dataset, var_names):
        super().__init__()
        self.view = QWebEngineView()
        fig = dataset[var_names].hist()
        html = '<html><head><meta charset="utf-8" />'
        html += '<body>'
        html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn',
                                    config={"displaylogo": False, 'modeBarButtonsToRemove': ['toImage']})
        html += '</body></html>'
        self.view.setHtml(html)

        self.setCentralWidget(self.view)
        self.setGeometry(300, 300, 1000, 600)
        self.show()

    def show(self):
        super().show()