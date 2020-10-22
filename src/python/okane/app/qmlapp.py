from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject


import sys


class QMLApp(QObject):
    """
        QMLAppView
        ----------

        Class responsible to run QML App
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create an Qt instance of the application
        self.app = QApplication(sys.argv)
        # Create a QML engine.
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.rootContext().setContextProperty("pyappview", self)

        self.main_qml = None


    def execute(self):
        self.qml_engine.load(self.main_qml)
        self.qml_engine.quit.connect(self.app.quit)
        sys.exit(self.app.exec_())
