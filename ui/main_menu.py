import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from models.user import User


class MainMenu(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CashCounter - Main Menu")
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self) -> None:
        # Central Widget
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setObjectName("central_widget")

        # Vertical Layout
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("vertical_layout")

        # Title
        self.title = QtWidgets.QLabel(parent=self.central_widget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setText("Main Menu")
        self.title.setObjectName("title")
        self.vertical_layout.addWidget(self.title)

        # Menu Buttons Widget
        self.menu_buttons_widget = QtWidgets.QWidget(parent=self.central_widget)
        self.menu_buttons_widget.setObjectName("menu_buttons_widget")

        # Grid Layout
        self.grid_layout = QtWidgets.QGridLayout(self.menu_buttons_widget)
        self.grid_layout.setObjectName("gridLayout")

        # New Count Button
        self.new_count_button = QtWidgets.QPushButton(parent=self.menu_buttons_widget)
        self.new_count_button.setMinimumSize(QtCore.QSize(100, 100))
        self.new_count_button.setText("Begin a New Count")
        self.new_count_button.setObjectName("new_count_button")
        self.grid_layout.addWidget(self.new_count_button, 0, 0, 1, 1)

        # Previous Counts Button
        self.previous_counts_button = QtWidgets.QPushButton(parent=self.menu_buttons_widget)
        self.previous_counts_button.setMinimumSize(QtCore.QSize(100, 100))
        self.previous_counts_button.setText("View Previous Counts")
        self.previous_counts_button.setObjectName("previous_counts_button")
        self.grid_layout.addWidget(self.previous_counts_button, 0, 1, 1, 1)

        # Update User Details Button
        self.update_user_details_button = QtWidgets.QPushButton(parent=self.menu_buttons_widget)
        self.update_user_details_button.setMinimumSize(QtCore.QSize(100, 100))
        self.update_user_details_button.setText("Update User Details")
        self.update_user_details_button.setObjectName("update_user_details_button")
        self.grid_layout.addWidget(self.update_user_details_button, 1, 0, 1, 1)

        # Logout Button
        self.logout_button = QtWidgets.QPushButton(parent=self.menu_buttons_widget)
        self.logout_button.setMinimumSize(QtCore.QSize(100, 100))
        self.logout_button.setText("Logout")
        self.logout_button.setObjectName("logout_button")
        self.grid_layout.addWidget(self.logout_button, 1, 1, 1, 1)

        self.vertical_layout.addWidget(self.menu_buttons_widget)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainMenu()
    window.show()
    sys.exit(app.exec())