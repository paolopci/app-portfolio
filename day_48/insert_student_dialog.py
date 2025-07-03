from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QWidget, QSpacerItem,
                             QSizePolicy, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from database_manager import db_manager


class InsertStudentDialog(QDialog):
    # Segnale per comunicare i dati del nuovo studente
    student_added = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Carica i corsi disponibili dal database MySQL
        self.available_courses = self.load_courses_from_database()
        self.initUI()

    def load_courses_from_database(self):
        """Carica i corsi disponibili dal database MySQL"""
        try:
            courses = db_manager.get_all_courses()
            if courses:
                print(f"Corsi caricati dal database: {courses}")
                return courses
            else:
                # Se non ci sono corsi nel database, restituisce una lista predefinita
                print("Nessun corso trovato nel database, uso corsi predefiniti")
                return ["Biology", "Math", "Astronomy", "Physics", "Computer Science", "Mathematics", "Chemistry"]
        except Exception as e:
            print(f"Errore durante il caricamento dei corsi: {e}")
            # In caso di errore, restituisce una lista predefinita
            return ["Biology", "Math", "Astronomy", "Physics", "Computer Science", "Mathematics", "Chemistry"]

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

        # ComboBox Corso - popolata con dati dal database
        self.course_combo = QComboBox()
        self.course_combo.addItem("Select Course")  # Opzione placeholder

        # Popola la ComboBox con i corsi dal database
        if self.available_courses:
            self.course_combo.addItems(self.available_courses)
        else:
            # Se non ci sono corsi, mostra un messaggio
            self.course_combo.addItem("No courses available")

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
                           self.course_combo.currentText() != "No courses available" and
                           self.course_combo.currentText() in self.available_courses)
        phone_filled = bool(self.phone_input.text().strip())

        # Abilita il button solo se tutti i campi sono riempiti
        self.submit_button.setEnabled(
            name_filled and course_selected and phone_filled)

    def get_next_id_from_database(self):
        """Ottiene il prossimo ID disponibile dal database MySQL"""
        try:
            next_id = db_manager.get_next_student_id()
            return str(next_id)
        except Exception as e:
            print(f"Errore durante il recupero del prossimo ID: {e}")
            return "1"

    def submit_student(self):
        """Gestisce il submit del nuovo studente"""
        try:
            # Raccoglie i dati dai campi
            next_id = self.get_next_id_from_database()
            name = self.name_input.text().strip()
            course = self.course_combo.currentText()
            phone = self.phone_input.text().strip()

            # Validazione aggiuntiva
            if not name or not course or not phone or course == "Select Course":
                QMessageBox.warning(self, "Dati Mancanti",
                                    "Tutti i campi sono obbligatori!")
                return

            # Crea il nuovo record
            new_student = [next_id, name, course, phone]

            print(f"Preparazione invio dati: {new_student}")

            # Emette il segnale con i dati del nuovo studente
            self.student_added.emit(new_student)

            # Chiude la finestra
            self.accept()

        except Exception as e:
            error_msg = f"Errore durante la preparazione dei dati: {e}"
            print(error_msg)
            QMessageBox.critical(self, "Errore", error_msg)

    def get_student_data(self):
        """Restituisce i dati inseriti (per uso alternativo)"""
        if not self.submit_button.isEnabled():
            return None

        try:
            next_id = self.get_next_id_from_database()
            return [
                next_id,
                self.name_input.text().strip(),
                self.course_combo.currentText(),
                self.phone_input.text().strip()
            ]
        except Exception as e:
            print(f"Errore durante il recupero dei dati: {e}")
            return None

    def refresh_courses(self):
        """Aggiorna la lista dei corsi dal database (metodo utile per future estensioni)"""
        try:
            # Salva la selezione corrente
            current_selection = self.course_combo.currentText()

            # Carica i nuovi corsi
            self.available_courses = self.load_courses_from_database()

            # Pulisce e ripopola la ComboBox
            self.course_combo.clear()
            self.course_combo.addItem("Select Course")

            if self.available_courses:
                self.course_combo.addItems(self.available_courses)

                # Ripristina la selezione se ancora valida
                if current_selection in self.available_courses:
                    self.course_combo.setCurrentText(current_selection)
            else:
                self.course_combo.addItem("No courses available")

        except Exception as e:
            print(f"Errore durante l'aggiornamento dei corsi: {e}")
