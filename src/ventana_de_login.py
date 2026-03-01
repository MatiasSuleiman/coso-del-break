from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox

try:
    from src.errores import CredencialesInvalidasError
    from src.system_facade import System_Facade
except ModuleNotFoundError:
    from errores import CredencialesInvalidasError
    from system_facade import System_Facade


class Ventana_de_login(QObject):
    senal_de_login_exitoso = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle("Login - Build n' Breakdown")
        self.ventana.setGeometry(500, 250, 520, 220)

        etiqueta_de_bienvenida = QLabel("Iniciar sesion de Gmail", self.ventana)
        etiqueta_de_bienvenida.setGeometry(170, 20, 220, 30)

        etiqueta_de_correo = QLabel("Correo:", self.ventana)
        etiqueta_de_correo.setGeometry(70, 70, 70, 30)

        self.barra_de_correo = QLineEdit(self.ventana)
        self.barra_de_correo.setPlaceholderText("usuario@gmail.com")
        self.barra_de_correo.setGeometry(140, 70, 300, 30)

        etiqueta_de_contrasena = QLabel("Contrasena:", self.ventana)
        etiqueta_de_contrasena.setGeometry(50, 110, 90, 30)

        self.barra_de_contrasena = QLineEdit(self.ventana)
        self.barra_de_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.barra_de_contrasena.setGeometry(140, 110, 300, 30)

        self.boton_de_login = QPushButton("Entrar", self.ventana)
        self.boton_de_login.setGeometry(220, 160, 80, 30)
        self.boton_de_login.clicked.connect(self.iniciar_sesion)

        self.barra_de_correo.returnPressed.connect(self.iniciar_sesion)
        self.barra_de_contrasena.returnPressed.connect(self.iniciar_sesion)

    def iniciar_sesion(self):
        correo = self.barra_de_correo.text().strip()
        contrasena = self.barra_de_contrasena.text().strip()

        if not correo or not contrasena:
            QMessageBox.warning(self.ventana, "Datos incompletos", "Complete correo y contrasena.")
            return

        self.boton_de_login.setEnabled(False)
        try:
            sistema = System_Facade.login(correo, contrasena)
        except CredencialesInvalidasError:
            QMessageBox.critical(
                self.ventana,
                "Login fallido",
                "Credenciales Invalidas. Chequee que el mail y la contraseña sean correctos",
            )
            self.boton_de_login.setEnabled(True)
            return
        except Exception as error:
            QMessageBox.critical(self.ventana, "Login fallido", f"No se pudo iniciar sesion.\n{error}")
            self.boton_de_login.setEnabled(True)
            return

        self.senal_de_login_exitoso.emit(sistema)
