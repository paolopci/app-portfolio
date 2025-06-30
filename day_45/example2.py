from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QDate
import sys
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calcolatore Età")
        self.init_ui()

    def init_ui(self):
        # Create the main layout
        grid = QGridLayout()

        # Create widgets
        name_label = QLabel("Nome:")
        self.name_line_edit = QLineEdit()

        data_birth_label = QLabel("Data di nascita DD/MM/YYYY:")
        # con self diventa una variabile di istanza
        # quindi la posso usare anche  def calculate_age(self):
        self.data_birth_line_edit = QLineEdit()
        self.data_birth_line_edit.setPlaceholderText("DD/MM/YYYY")

        calculate_button = QPushButton("Calcola Età")
        calculate_button.clicked.connect(self.calculate_age)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-weight: bold; color: blue;")

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(data_birth_label, 1, 0)
        grid.addWidget(self.data_birth_line_edit, 1, 1)
        # Span across 2 columns, Span across 2 columns, 1 su una riga 2 su due colonne
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.result_label, 3, 0, 1, 2)  # Span across 2 columns

        # Set the layout for the widget
        self.setLayout(grid)

    def calculate_age(self):
        try:
            name = self.name_line_edit.text().strip()
            birth_date_str = self.data_birth_line_edit.text().strip()

            if not name:
                self.result_label.setText("Please enter a name.")
                return

            if not birth_date_str:
                self.result_label.setText("Please enter a birth date.")
                return

            # Parse the birth date (formato italiano DD/MM/YYYY)
            birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y")
            today = datetime.now()

            # Calculate age
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1

            if age < 0:
                self.result_label.setText(
                    "Birth date cannot be in the future.")
            else:
                self.result_label.setText(f"{name} is {age} years old.")

        except ValueError:
            self.result_label.setText(
                "Formato data non valido. Usa DD/MM/YYYY.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    age_calculator = AgeCalculator()
    age_calculator.resize(400, 200)
    age_calculator.show()
    sys.exit(app.exec())
