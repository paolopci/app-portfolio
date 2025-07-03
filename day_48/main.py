import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QMenuBar, QToolBar, QStatusBar,
                             QHeaderView, QFrame, QSpacerItem, QSizePolicy,
                             QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QFont, QPalette, QColor

# Import della finestra modale e del database manager
from insert_student_dialog import InsertStudentDialog
from database_manager import db_manager


class StudentManagementForm(QMainWindow):
    """Form principale per la gestione degli studenti (versione senza dati di esempio)"""

    def __init__(self):
        super().__init__()
        self.students_data = []  # Dati degli studenti caricati dal database
        self.initUI()
        self.load_students_from_database()

    # ---------------------------------------------------------------------
    # Inizializzazione interfaccia utente
    # ---------------------------------------------------------------------
    def initUI(self):
        # Impostazioni finestra principale
        self.setWindowTitle("Student Management System - MySQL")
        self.setGeometry(100, 100, 800, 600)

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Creazione della MenuBar / ToolBar / Tabella / Footer
        self.create_menu_bar()
        self.create_toolbar()
        self.create_table()
        main_layout.addWidget(self.table)
        self.create_footer()
        main_layout.addWidget(self.footer_frame)

        # Impostazione stile generale
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QTableWidget {
                border: 2px solid #333333;
                background-color: white;
                gridline-color: #333333;
                selection-background-color: #0078d4;
            }
            QTableWidget::item {
                border-bottom: 1px solid #333333;
                border-right: 1px solid #333333;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 8px;
                border: 1px solid #333333;
                font-weight: bold;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 2px solid #333333;
                padding: 8px 16px;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover { background-color: #d0d0d0; }
            QPushButton:pressed { background-color: #c0c0c0; }
            QToolBar { background-color: #f0f0f0; spacing: 5px; border: none; }
            QMenuBar { background-color: #f0f0f0; }
            QMenuBar::item { padding: 4px 8px; background-color: transparent; }
            QMenuBar::item:selected { background-color: #e0e0e0; }
        """)

    # ------------------------------------------------------------------
    # CREAZIONE MENU BAR (senza "Initialize Sample Data")
    # ------------------------------------------------------------------
    def create_menu_bar(self):
        menubar = self.menuBar()

        # Menu File
        file_menu = menubar.addMenu('&File')

        # Azioni del menu File
        new_action = QAction('&New', self)
        new_action.triggered.connect(self.new_record)
        file_menu.addAction(new_action)

        refresh_action = QAction('&Refresh', self)
        refresh_action.triggered.connect(self.refresh_data)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Help
        help_menu = menubar.addMenu('&Help')

        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    # ------------------------------------------------------------------
    # CREAZIONE TOOLBAR
    # ------------------------------------------------------------------
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))

        # Pulsante Aggiungi
        add_action = QAction('➕', self)
        add_action.setToolTip('Add New Record')
        add_action.triggered.connect(self.add_record)
        toolbar.addAction(add_action)

        # Pulsante Refresh
        refresh_action = QAction('🔄', self)
        refresh_action.setToolTip('Refresh Data')
        refresh_action.triggered.connect(self.refresh_data)
        toolbar.addAction(refresh_action)

        # Pulsante Cerca
        search_action = QAction('🔍', self)
        search_action.setToolTip('Search Records')
        search_action.triggered.connect(self.search_records)
        toolbar.addAction(search_action)

    # ------------------------------------------------------------------
    # CREAZIONE TABELLA
    # ------------------------------------------------------------------
    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Course', 'Mobile'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 80)
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)

    # ------------------------------------------------------------------
    # CREAZIONE FOOTER
    # ------------------------------------------------------------------
    def create_footer(self):
        self.footer_frame = QFrame()
        self.footer_frame.setFrameStyle(QFrame.Shape.Box)
        self.footer_frame.setLineWidth(2)
        self.footer_frame.setFixedHeight(60)

        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(10, 10, 10, 10)

        spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        footer_layout.addItem(spacer)

        self.edit_button = QPushButton('Edit Record')
        self.edit_button.clicked.connect(self.edit_record)
        footer_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton('Delete Record')
        self.delete_button.clicked.connect(self.delete_record)
        footer_layout.addWidget(self.delete_button)

    # ------------------------------------------------------------------
    # FUNZIONI LOGICA
    # ------------------------------------------------------------------
    def load_students_from_database(self):
        """Carica gli studenti dal database MySQL senza suggerire dati di esempio"""
        try:
            self.students_data = db_manager.get_all_students()

            if self.students_data:
                self.populate_table()
                print(
                    f"Caricati {len(self.students_data)} studenti dal database")
            else:
                print("Nessun studente trovato nel database")
                # Messaggio informativo neutro (senza riferimento ai dati di esempio)
                self.show_message(
                    "Info", "Nessun studente trovato nel database.\nUsa 'File -> New' per aggiungere un nuovo studente.")

        except Exception as e:
            error_msg = f"Errore durante il caricamento dei dati dal database: {e}"
            print(error_msg)
            self.show_error("Errore Database", error_msg)

    def populate_table(self):
        self.table.setRowCount(len(self.students_data))
        for row, data in enumerate(self.students_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    # ------------------------------------------------------------------
    # AZIONI MENU / TOOLBAR
    # ------------------------------------------------------------------
    def new_record(self):
        print("New Record clicked")
        self.open_add_student_dialog()

    def refresh_data(self):
        print("Refresh data")
        self.load_students_from_database()

    def show_about(self):
        self.show_message(
            "About", "Student Management System\nVersione MySQL 1.0\nConnesso al database SchoolDb")

    def add_record(self):
        self.open_add_student_dialog()

    def open_add_student_dialog(self):
        dialog = InsertStudentDialog(self)
        dialog.student_added.connect(self.add_student_to_database)
        dialog.exec()

    def add_student_to_database(self, student_data):
        try:
            name, course, mobile = student_data[1], student_data[2], student_data[3]
            if db_manager.insert_student(name, course, mobile):
                self.refresh_data()
                self.show_message(
                    "Successo", f"Studente '{name}' aggiunto con successo!")
            else:
                self.show_error(
                    "Errore", "Errore durante l'inserimento dello studente nel database")
        except Exception as e:
            error_msg = f"Errore durante l'aggiunta dello studente: {e}"
            self.show_error("Errore", error_msg)

    def search_records(self):
        print("Search Records clicked")

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            print(f"Edit Record clicked - Row: {current_row}")
            # TODO: Implementare la modifica
        else:
            self.show_message(
                "Attenzione", "Seleziona un record da modificare")

    def delete_record(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            try:
                student_id = int(self.table.item(current_row, 0).text())
                student_name = self.table.item(current_row, 1).text()
                reply = QMessageBox.question(self, 'Conferma Eliminazione',
                                             f"Sei sicuro di voler eliminare lo studente '{student_name}'?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes and db_manager.delete_student(student_id):
                    self.refresh_data()
                    self.show_message(
                        "Successo", f"Studente '{student_name}' eliminato con successo!")
            except Exception as e:
                self.show_error(
                    "Errore", f"Errore durante l'eliminazione: {e}")
        else:
            self.show_message("Attenzione", "Seleziona un record da eliminare")

    # ------------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------------
    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def closeEvent(self, event):
        db_manager.disconnect()
        event.accept()


# ----------------------------------------------------------------------
# MAIN ENTRY POINT
# ----------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    if not db_manager.test_connection():
        QMessageBox.critical(None, "Errore Database",
                             "Impossibile connettersi al database MySQL.\n"
                             "Verifica che il server sia in esecuzione e che i parametri di connessione siano corretti.")
        sys.exit(1)

    window = StudentManagementForm()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
