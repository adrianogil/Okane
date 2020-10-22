from .qmlapp import QMLApp


class OkaneApp():
    def __init__(self, *args, **kwargs):
        self.qml_app = QMLApp()
        self.qml_app.main_qml = 'okane/app/qml/okane/main.qml'

    def show(self):
        self.qml_app.execute()
