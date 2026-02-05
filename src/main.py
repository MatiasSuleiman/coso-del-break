import sys
from PyQt6.QtWidgets import QApplication
from src.gui import Gui

def main():
    aplicacion= QApplication(sys.argv)
    interfaz = Gui()
    interfaz.ventana.show()
    sys.exit(aplicacion.exec())

if __name__ == "__main__":
    main()
