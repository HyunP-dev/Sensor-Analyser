from PyQt5.QtWidgets import *
import os
import sys


class SelectHistogramVariablesDialog(QDialog):
    def __init__(self, var_names):
        super().__init__()
        self.variablesList: QListWidget
        self.var_names = var_names
        self.initUI()
        self.result = []

    def initUI(self):
        self.setGeometry(500, 500, 300, 200)
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        label = QLabel(self)
        label.setText("Variables")
        self.variablesList = QListWidget(self)
        for var_name in self.var_names:
            item = QListWidgetItem()
            item.setCheckState(False)
            item.setText(var_name)
            self.variablesList.addItem(item)

        layout.addWidget(label)
        layout.addWidget(self.variablesList)
        lower_layout = QHBoxLayout()
        lower_layout.addStretch()
        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        lower_layout.addWidget(btnOK)
        lower_layout.addWidget(btnCancel)
        layout.addLayout(lower_layout)

    def onOKButtonClicked(self):
        items = [self.variablesList.item(i) for i in range(self.variablesList.count())]
        items = [item.text() for item in items if item.checkState() == 2]
        self.result = items
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = SelectHistogramVariablesDialog(["var 1", "var 2"])
    ex.show()
    sys.exit(app.exec_())
