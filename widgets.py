from typing import Union

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
import os


class FileTreeWidget(QTreeWidget):
    def __init__(self, parent, path):
        super().__init__()
        self.parent = parent
        self.setAlternatingRowColors(True)
        self.header().setVisible(False)
        self.setPath(path)

    def getPath(self):
        return self._path

    def _refresh(self, path):
        def refresh(root_dir: str, parentItem: Union[FileTreeWidget, FileTreeWidgetItem]):
            files = os.listdir(root_dir)
            for file in files:
                fitem = FileTreeWidgetItem(parentItem)
                path = os.path.join(root_dir, file)
                fitem.filepath = path
                fitem.setText(0, file)
                if os.path.isdir(path):
                    refresh(path, fitem)
        self.clear()
        refresh(path, self)

    def setPath(self, path):
        self._path = path
        self._refresh(path)

class FileTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepath: str
