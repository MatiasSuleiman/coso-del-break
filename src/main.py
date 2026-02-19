import sys
from PyQt6.QtWidgets import QApplication
from src.gui import Gui
from src.ventana_de_login import Ventana_de_login


class Controlador_de_aplicacion:
    def __init__(self):
        self.interfaz_principal = Ventana_de_login()
        self.interfaz_principal.senal_de_login_exitoso.connect(self.al_iniciar_sesion_exitoso)
        self.interfaz_principal.ventana.show()

    def al_iniciar_sesion_exitoso(self, sistema):
        interfaz_anterior = self.interfaz_principal
        self.interfaz_principal = Gui(sistema)
        interfaz_anterior.ventana.close()


def main():
    aplicacion = QApplication(sys.argv)
    controlador_de_aplicacion = Controlador_de_aplicacion()
    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    main()
