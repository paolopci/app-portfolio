from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        grid = QGridLayout()

        name_label = QLabel("Name:")
        name_line_edit = QLineEdit()

        data_birth_label = QLabel("Date of Birth MM/DD/YYYY:")
        data_birth_line_edit = QLineEdit()

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(name_line_edit, 0, 1)
        grid.addWidget(data_birth_label, 1, 0)
        grid.addWidget(data_birth_line_edit, 1, 1)


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
