import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from models.user import User


class LoginScreen(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CashCounter - Log In")
        self.resize(400, 300)
        self.setMinimumSize(400, 300)
        self.init_ui()

    def init_ui(self) -> None:
        # Vertical Layout
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("vertical_layout")
        self.setLayout(self.vertical_layout)

        # Title
        self.title = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setText("Log In")
        self.title.setObjectName("title")
        self.vertical_layout.addWidget(self.title)

        # Username Field
        self.username_field = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_field.sizePolicy().hasHeightForWidth())
        self.username_field.setSizePolicy(sizePolicy)
        self.username_field.setMinimumSize(QtCore.QSize(350, 30))
        self.username_field.setMaximumSize(QtCore.QSize(16777215, 30))
        self.username_field.setPlaceholderText("Username")
        self.username_field.setObjectName("username_field")
        self.vertical_layout.addWidget(self.username_field)

        # Password Field
        self.password_field = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_field.sizePolicy().hasHeightForWidth())
        self.password_field.setSizePolicy(sizePolicy)
        self.password_field.setMinimumSize(QtCore.QSize(350, 30))
        self.password_field.setMaximumSize(QtCore.QSize(16777215, 30))
        self.password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setObjectName("password_field")
        self.vertical_layout.addWidget(self.password_field)

        # Login Button
        self.login_button = QtWidgets.QPushButton()
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(self.login)
        self.login_button.setText("Login")
        self.vertical_layout.addWidget(self.login_button)

    def login(self) -> None:
        # Cleaning the inputs
        username: str = self.username_field.text().strip()
        password: str = self.password_field.text().strip()

        # Checking none of the fields are blank
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter both a username and a password.")
            return
        
        # Trying to login
        user = User.login(username, password)

        if user:
            QtWidgets.QMessageBox.information(self, "Login Successful", f"Welcome, {user.first_name} {user.last_name}!")
        else:
            QtWidgets.QMessageBox.critical(self, "Login Failed", "Your username or password is not correct. Please contact your administrator or try again.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = LoginScreen()
    window.show()
    sys.exit(app.exec())