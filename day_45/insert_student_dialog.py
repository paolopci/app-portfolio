from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QWidget, QSpacerItem,
                             QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class InsertStudentDialog(QDialog):
    # Segnale per comunicare i dati del nuovo studente
    student_added = pyqtSignal(list)

    def __init__(self, parent=None, sample_data=None):
        super().__init__(parent)
        self.sample_data = sample_data or []
        # Lista dei corsi disponibili
        self.available_courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.initUI()

    def initUI(self):
        # Impostazioni finestra
        self.setWindowTitle("Add New Student")
        self.setFixedSize(400, 300)
        self.setModal(True)

        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Spacer superiore per centrare verticalmente
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                 QSizePolicy.Policy.Expanding)
        main_layout.addItem(top_spacer)

        # Container per i campi input
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setSpacing(15)

        # Campo Nome
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setFixedHeight(40)
        self.name_input.textChanged.connect(self.check_inputs)
        input_layout.addWidget(self.name_input)

        # ComboBox Corso
        self.course_combo = QComboBox()
        self.course_combo.addItem("Select Course")  # Opzione placeholder
        self.course_combo.addItems(self.available_courses)
        self.course_combo.setFixedHeight(40)
        self.course_combo.currentTextChanged.connect(self.check_inputs)
        # Forza lo stile predefinito per evitare problemi con la freccia
        self.course_combo.setStyleSheet("")
        input_layout.addWidget(self.course_combo)

        # Campo Telefono
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.phone_input.setFixedHeight(40)
        self.phone_input.textChanged.connect(self.check_inputs)
        input_layout.addWidget(self.phone_input)

        main_layout.addWidget(input_container)

        # Spacer per distanziare il button
        middle_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum,
                                    QSizePolicy.Policy.Fixed)
        main_layout.addItem(middle_spacer)

        # Button Submit
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedHeight(45)
        self.submit_button.setEnabled(False)  # Inizialmente disabilitato
        self.submit_button.clicked.connect(self.submit_student)
        main_layout.addWidget(self.submit_button)

        # Spacer inferiore per centrare verticalmente
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                    QSizePolicy.Policy.Expanding)
        main_layout.addItem(bottom_spacer)

        # Stile della finestra
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 3px solid #333333;
            }
            QLineEdit {
                border: 2px solid #333333;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
                border-radius: 0px;
                margin: 0px;
                box-sizing: border-box;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
            QComboBox {
                border: 2px solid #333333;
                padding: 8px 12px;
                font-size: 12px;
                background-color: white;
                color: black;
                border-radius: 0px;
                margin: 0px;
            }
            QComboBox:focus {
                border: 2px solid #0078d4;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #333333;
                background-color: white;
                color: black;
                selection-background-color: #e0e0e0;
                selection-color: black;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
                background-color: white;
                color: black;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #e0e0e0;
                color: black;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #d0d0d0;
                color: black;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 2px solid #333333;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 20px;
                margin-top: 5px;
            }
            QPushButton:enabled:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #999999;
                border: 2px solid #cccccc;
            }
        """)

    def check_inputs(self):
        """Controlla se tutti i campi sono valorizzati per abilitare il button Submit"""
        name_filled = bool(self.name_input.text().strip())
        course_selected = (self.course_combo.currentText() != "Select Course" and
                           self.course_combo.currentText() in self.available_courses)
        phone_filled = bool(self.phone_input.text().strip())

        # Abilita il button solo se tutti i campi sono riempiti
        self.submit_button.setEnabled(
            name_filled and course_selected and phone_filled)

    def get_next_id(self):
        """Trova l'ID più alto nei sample_data e restituisce il successivo"""
        if not self.sample_data:
            return "1"

        # Estrae tutti gli ID e trova il massimo
        ids = []
        for record in self.sample_data:
            try:
                ids.append(int(record[0]))
            except (ValueError, IndexError):
                continue

        if ids:
            return str(max(ids) + 1)
        else:
            return "1"

    def submit_student(self):
        """Gestisce il submit del nuovo studente"""
        # Raccoglie i dati dai campi
        new_id = self.get_next_id()
        name = self.name_input.text().strip()
        course = self.course_combo.currentText()
        phone = self.phone_input.text().strip()

        # Crea il nuovo record
        new_student = [new_id, name, course, phone]

        # Emette il segnale con i dati del nuovo studente
        self.student_added.emit(new_student)

        # Chiude la finestra
        self.accept()

    def get_student_data(self):
        """Restituisce i dati inseriti (per uso alternativo)"""
        if not self.submit_button.isEnabled():
            return None

        new_id = self.get_next_id()
        return [
            new_id,
            self.name_input.text().strip(),
            self.course_combo.currentText(),
            self.phone_input.text().strip()
        ]
