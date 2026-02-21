import database.database as db
import helpers.helpers as hlp
from datetime import date
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QLabel,
    QMessageBox,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QDoubleSpinBox,
    QSpinBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt, QDate


class AddTransactionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Transaction")
        self.resize(300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Transaction Name")
        form_layout.addRow("Transaction Name:", self.name_input)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, float("inf"))
        self.amount_input.setDecimals(2)
        form_layout.addRow("Amount:", self.amount_input)

        self.type_input = QComboBox()
        self.type_input.addItems(["income", "expense"])
        form_layout.addRow("Transaction Type:", self.type_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Transaction Date:", self.date_input)

        submit_button = QPushButton("Add Transaction")
        submit_button.clicked.connect(self.submit_transaction)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(submit_button)

    def submit_transaction(self):
        name = self.name_input.text()
        amount = self.amount_input.value()
        transaction_type = self.type_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        print(name, amount, transaction_type, date)

        if not name or not amount:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        db.add_transaction(name, transaction_type, amount, date)
        QMessageBox.information(
            self, "Success", f"Transaction added: {name}"
        )


class ViewTransactionTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Transactions")
        self.resize(600, 400)

        self.is_loading = False
        self.modified_rows = set()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.itemChanged.connect(self.handle_item_changed)
        self.layout.addWidget(self.table)

        button_layout = QVBoxLayout()

        self.plot_button = QPushButton("Plot Balance")
        self.plot_button.clicked.connect(self.plot_balance)
        button_layout.addWidget(self.plot_button)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        self.discard_button = QPushButton("Discard Changes")
        self.discard_button.setEnabled(False)
        self.discard_button.clicked.connect(self.load_data)
        button_layout.addWidget(self.discard_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_transaction)
        button_layout.addWidget(self.delete_button)

        self.reset_button = QPushButton("Reset Database")
        self.reset_button.clicked.connect(self.reset_db)
        button_layout.addWidget(self.reset_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        self.layout.addLayout(button_layout)

        self.load_data()

    def load_data(self):
        self.is_loading = True
        self.modified_rows.clear()

        self.save_button.setEnabled(False)
        self.discard_button.setEnabled(False)

        data = hlp.get_data()
        self.table.setRowCount(0)

        if not data:
            QMessageBox.information(self, "Info", "No transactions found.")
            self.is_loading = False
            return

        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Transaction Name",
                "Transaction Type",
                "Amount",
                "Transaction Date",
            ]
        )

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                table_item = QTableWidgetItem(str(item))
                if col_idx == 0:
                    table_item.setFlags(
                        Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
                    )
                self.table.setItem(row_idx, col_idx, table_item)

        self.table.resizeColumnsToContents()
        self.is_loading = False

    def handle_item_changed(self, item):
        if self.is_loading:
            return

        self.modified_rows.add(item.row())
        self.save_button.setEnabled(True)
        self.save_button.setText("Save Changes")
        self.discard_button.setEnabled(True)

    def save_changes(self):
        try:
            for row in self.modified_rows:
                transaction_id = self.table.item(row, 0).text()
                transaction_name = self.table.item(row, 1).text()
                transaction_type = self.table.item(row, 2).text()
                amount = self.table.item(row, 3).text()
                date = self.table.item(row, 4).text()
                if transaction_type not in ["income", "expense"]:
                    raise ValueError(f"Row {row+1}: Type must be 'income' or 'expense'")
                if not hlp.is_valid_date(date):
                    raise ValueError(
                        f"Row {row+1}: Invalid date format, should be YYYY-MM-DD"
                    )
                amount = float(amount)
                if amount < 0:
                    raise ValueError(f"Row {row+1}: Amount must be a positive number")
                db.update_transactions(
                    transaction_id, transaction_name, transaction_type, amount, date
                )
            QMessageBox.information(self, "Success", "All changes saved!")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    def delete_transaction(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Error", "No row selected.")
            return
        transaction_id = self.table.item(current_row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete transaction ID {transaction_id}?",
        )
        if confirm == QMessageBox.StandardButton.Yes:
            db.delete_transaction(transaction_id)
            QMessageBox.information(
                self, "Deleted", f"Transaction ID {transaction_id} deleted."
            )
            self.load_data()
            self.modified_rows.discard(current_row)

    def reset_db(self):
        confirm = QMessageBox.question(
            self, "Reset Database", "Are you sure you want to reset the database?"
        )
        if confirm == QMessageBox.StandardButton.Yes:
            db.delete_all_transactions()
            self.load_data()

    def plot_balance(self):
        self.plot_window = BalancePlotWindow()
        self.plot_window.show()


class BalancePlotWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Balance Plot")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        fig = db.plot_balance()
        print(fig)
        if fig:
            canvas = FigureCanvas(fig)
            self.layout.addWidget(canvas)
        else:
            label = QLabel("No data to plot.")
            self.layout.addWidget(label)


class InterestSetup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interest Calculation Setup")
        self.resize(300, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.interest_form_layout = QFormLayout()

        self.principal_input = QDoubleSpinBox()
        self.principal_input.setRange(0, 1e12)
        self.principal_input.setDecimals(2)
        self.principal_input.setValue(1000)
        self.interest_form_layout.addRow("Principal Amount:", self.principal_input)

        self.rate_input = QDoubleSpinBox()
        self.rate_input.setRange(0, 100)
        self.rate_input.setDecimals(2)
        self.rate_input.setSuffix(" %")
        self.rate_input.setValue(0.2)
        self.interest_form_layout.addRow("Interest Rate:", self.rate_input)

        self.years_input = QSpinBox()
        self.years_input.setRange(1, 100)
        self.years_input.setValue(5)
        self.interest_form_layout.addRow("Number of Years:", self.years_input)

        self.monthly_contribution_input = QDoubleSpinBox()
        self.monthly_contribution_input.setRange(0, 1e12)
        self.monthly_contribution_input.setDecimals(2)
        self.interest_form_layout.addRow(
            "Monthly Contribution:", self.monthly_contribution_input
        )

        self.compounds_per_year_input = QSpinBox()
        self.compounds_per_year_input.setRange(1, 365)
        self.interest_form_layout.addRow(
            "Compounds Per Year:", self.compounds_per_year_input
        )

        self.layout.addLayout(self.interest_form_layout)
        self.calculate_button = QPushButton("Calculate and Plot")
        self.calculate_button.clicked.connect(self.calculate_interest)
        self.layout.addWidget(self.calculate_button)
        self.current_fig = None

    def calculate_interest(self):
        if self.current_fig is not None:
            self.layout.removeWidget(self.current_fig)
            self.current_fig.deleteLater()
            self.current_fig = None
        data = hlp.calc_interest(
            self.principal_input.value(),
            self.rate_input.value(),
            self.years_input.value(),
            self.monthly_contribution_input.value() or 0,
            self.compounds_per_year_input.value(),
        )
        fig = db.plot_interest(data)
        if fig:
            canvas = FigureCanvas(fig)
            self.layout.addWidget(canvas)
            self.current_fig = canvas
        else:
            label = QLabel("No data to plot.")
            self.layout.addWidget(label)
            self.current_fig = label


class FinanceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Manager")
        self.resize(600, 400)
        self.setWindowIcon(QIcon("src/logo.png"))

        center_widget = QWidget()
        self.setCentralWidget(center_widget)

        self.layout = QVBoxLayout()
        center_widget.setLayout(self.layout)

        title = QLabel("Finance Manager")
        self.layout.addWidget(title)
        init_button = QPushButton("Initialize Database", self)
        self.layout.addWidget(init_button)
        init_button.clicked.connect(self.init_db)

        add_button = QPushButton("Add Transaction", self)
        self.layout.addWidget(add_button)
        add_button.clicked.connect(self.add_transaction)

        view_button = QPushButton("View Transactions", self)
        self.layout.addWidget(view_button)
        view_button.clicked.connect(self.view_transactions)

        plot_interest_button = QPushButton("Plot Interest", self)
        self.layout.addWidget(plot_interest_button)
        plot_interest_button.clicked.connect(self.plot_interest)

    def init_db(self):
        try:
            db.init_db()
            QMessageBox.information(
                self, "Success", "Database initialized successfully."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize database: {e}")

    def add_transaction(self):
        self.add_form = AddTransactionForm()
        self.add_form.show()

    def view_transactions(self):
        self.view_table = ViewTransactionTable()
        self.view_table.show()

    def plot_interest(self):
        self.interest_ui = InterestSetup()
        self.interest_ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceManager()
    window.show()
    sys.exit(app.exec())
