import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from models.user import User
from models.currency import Currency
from models.denomination import Denomination
from models.count import Count
from models.count_record import CountRecord


class BeginNewCountScreen(QtWidgets.QDialog):
    def __init__(self, user: User, currency: Currency, denominations: list[Denomination], parent=None) -> None:
        super().__init__()
        self.user: User = user
        self.currency: Currency = currency
        self.denominations: list[Denomination] = denominations

        self.setWindowTitle("CashCounter - Begin a New Count")
        self.resize(600, 450)
        self.setMinimumSize(600, 450)

        self.denomination_labels: list[QtWidgets.QLabel] = []
        self.quantity_inputs: list[QtWidgets.QSpinBox] = []
        self.total_labels: list[QtWidgets.QLabel] = []

        self.init_ui()

    def init_ui(self) -> None:
        # Vertical Layout
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("vertical_layout")

        # Title
        self.title = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setText("Begin a New Count")
        self.title.setObjectName("title")
        self.vertical_layout.addWidget(self.title)

        # Input Form
        self.input_form = QtWidgets.QWidget()
        self.input_form.setObjectName("input_form")

        # Grid Layout
        self.grid_layout = QtWidgets.QGridLayout(self.input_form)
        self.grid_layout.setObjectName("grid_layout")

        # Denomination Title (Input Form Heading)
        self.denomination_title = QtWidgets.QLabel(parent=self.input_form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.denomination_title.setFont(font)
        self.denomination_title.setText("Denomination")
        self.denomination_title.setObjectName("denomination_title")
        self.grid_layout.addWidget(self.denomination_title, 0, 0, 1, 1)

        # Quantity Title (Input Form Heading)
        self.quantity_title = QtWidgets.QLabel(parent=self.input_form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.quantity_title.setFont(font)
        self.quantity_title.setText("Quantity")
        self.quantity_title.setObjectName("quantity_title")
        self.grid_layout.addWidget(self.quantity_title, 0, 1, 1, 1)

        # Total Title (Input Form Heading)
        self.total_title = QtWidgets.QLabel(parent=self.input_form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.total_title.setFont(font)
        self.total_title.setText("Total")
        self.total_title.setObjectName("total_title")
        self.grid_layout.addWidget(self.total_title, 0, 2, 1, 1)

        for index, denomination in enumerate(self.denominations):
            # Denomination Value
            self.denomination_labels.append(QtWidgets.QLabel(parent=self.input_form))
            self.denomination_labels[-1].setObjectName(f"denomination_value_{index}")
            self.denomination_labels[-1].setText(f"{denomination.currency.symbol}{denomination.value}")
            self.grid_layout.addWidget(self.denomination_labels[-1], index + 1, 0, 1, 1)

            # Quantity Input
            self.quantity_inputs.append(QtWidgets.QSpinBox(parent=self.input_form))
            self.quantity_inputs[-1].setObjectName(f"quantity_value_{index}")
            self.quantity_inputs[-1].valueChanged.connect(self.update_totals)
            self.grid_layout.addWidget(self.quantity_inputs[-1], index + 1, 1, 1, 1)

            # Total Value
            self.total_labels.append(QtWidgets.QLabel(parent=self.input_form))
            self.total_labels[-1].setObjectName(f"total_value_{index}")
            self.total_labels[-1].setText(f"{denomination.currency.symbol}0.00")
            self.grid_layout.addWidget(self.total_labels[-1], index + 1, 2, 1, 1)

        self.vertical_layout.addWidget(self.input_form)

        # Total Sum Label
        self.total_sum_label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.total_sum_label.setFont(font)
        self.total_sum_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.total_sum_label.setText(f"Total: {self.currency.symbol}0.00")
        self.total_sum_label.setObjectName("total_sum_label")
        self.vertical_layout.addWidget(self.total_sum_label)

        # Button Box
        self.button_box = QtWidgets.QDialogButtonBox()
        self.button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button_box.setObjectName("button_box")
        self.vertical_layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject) # type: ignore

        self.setLayout(self.vertical_layout)

    def accept(self) -> None:
        # Creating a new count
        count: Count = Count(self.user, self.currency)
        count.save()

        # Creating count records based on the user inputs
        for index, denomination in enumerate(self.denominations):
            quantity: int = self.quantity_inputs[index].value()
            count_record: CountRecord = CountRecord(denomination, count, quantity)
            count_record.save()


        QtWidgets.QMessageBox.information(self, "Success", "Count has been saved successfully.")
        super().accept()

    def reject(self) -> None:
        reply: QtWidgets.QMessageBox = QtWidgets.QMessageBox.question(
            self,
            "Cancel Confirmation",
            "Are you sure you want to cancel? Unsaved data will be lost.",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            super().reject()

    def update_totals(self) -> None:
        grand_total: float = 0.0

        for index, denomination in enumerate(self.denominations):
            quantity: int = self.quantity_inputs[index].value()
            total: float = float(quantity * denomination.value)
            grand_total += total
            self.total_labels[index].setText(f"{denomination.currency.symbol}{total:.2f}")
        
        # Updating the grand total
        self.total_sum_label.setText(f"Total: {self.currency.symbol}{grand_total:.2f}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    user: User = User.load_by_user_id(1)
    currency: Currency = Currency.load_by_currency_id(1)
    denominations: list[Denomination] = Denomination.get_denomination_by_currency(currency)

    window = BeginNewCountScreen(user, currency, denominations)
    window.exec()

    sys.exit(app.exec())