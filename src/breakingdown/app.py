import sys

from PyQt6.QtWidgets import QApplication

from main import Controlador_de_aplicacion


def main() -> int:
    app = QApplication(sys.argv)
    app.controlador_de_aplicacion = Controlador_de_aplicacion()
    return app.exec()
