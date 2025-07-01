import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QMenuBar, QToolBar, QStatusBar,
                             QHeaderView, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QFont, QPalette, QColor
import sqlite3


class StudentManagementForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Impostazioni finestra principale
        self.setWindowTitle("Student Management System")
        self.setGeometry(100, 100, 800, 600)

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Creazione della MenuBar
        self.create_menu_bar()

        # Creazione della ToolBar
        self.create_toolbar()

        # Creazione della tabella
        self.create_table()
        main_layout.addWidget(self.table)

        # Creazione del footer con i pulsanti
        self.create_footer()
        main_layout.addWidget(self.footer_frame)

        # Impostazione stile generale
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
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
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QToolBar {
                background-color: #f0f0f0;
                spacing: 5px;
                border: none;
            }
            QMenuBar {
                background-color: #f0f0f0;
            }
            QMenuBar::item {
                padding: 4px 8px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
        """)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Menu File
        file_menu = menubar.addMenu('&File')

        # Azioni del menu File
        new_action = QAction('&New', self)
        new_action.triggered.connect(self.new_record)
        file_menu.addAction(new_action)

        open_action = QAction('&Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('&Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Help
        help_menu = menubar.addMenu('&Help')

        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))

        # Pulsante Aggiungi (cerchio con croce)
        add_action = QAction('➕', self)
        add_action.setToolTip('Add New Record')
        add_action.triggered.connect(self.add_record)
        toolbar.addAction(add_action)

        # Pulsante Cerca (lente di ingrandimento)
        search_action = QAction('🔍', self)
        search_action.setToolTip('Search Records')
        search_action.triggered.connect(self.search_records)
        toolbar.addAction(search_action)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Course', 'Mobile'])

        # Impostazione larghezza colonne
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table.setColumnWidth(0, 80)

        # Aggiunta di alcune righe di esempio
        self.table.setRowCount(5)

        # Esempio di dati
        sample_data = [
            ['1', 'Mario Rossi', 'Computer Science', '333-1234567'],
            ['2', 'Anna Bianchi', 'Mathematics', '333-2345678'],
            ['3', 'Luca Verdi', 'Physics', '333-3456789'],
            ['4', 'Sara Neri', 'Chemistry', '333-4567890'],
            ['5', 'Marco Blu', 'Biology', '333-5678901']
        ]

        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)

        # Impostazione altezza righe
        self.table.verticalHeader().setDefaultSectionSize(30)
        self.table.verticalHeader().hide()

        # Selezione intera riga
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)

    def load_data(self):
        try:
            # Connessione al database
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()

            # Esecuzione della query
            cursor.execute("SELECT * FROM Students")

            # Recupero di tutti i records
            records = cursor.fetchall()

            # Stampa dei records a terminale
            print("Records dal database:")
            print("-" * 50)

            if records:
                for i, record in enumerate(records):
                    print(f"Record {i+1}: {record}")
            else:
                print("Nessun record trovato nel database")

            # Chiusura della connessione
            connection.close()

            return records

        except sqlite3.Error as e:
            print(f"Errore database: {e}")
            return None
        except Exception as e:
            print(f"Errore generico: {e}")
            return None

    def create_footer(self):
        self.footer_frame = QFrame()
        self.footer_frame.setFrameStyle(QFrame.Shape.Box)
        self.footer_frame.setLineWidth(2)
        self.footer_frame.setFixedHeight(60)

        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(10, 10, 10, 10)

        # Spacer per allineare i pulsanti a destra
        spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        footer_layout.addItem(spacer)

        # Pulsante Edit Record
        self.edit_button = QPushButton('Edit Record')
        self.edit_button.clicked.connect(self.edit_record)
        footer_layout.addWidget(self.edit_button)

        # Pulsante Delete Record
        self.delete_button = QPushButton('Delete Record')
        self.delete_button.clicked.connect(self.delete_record)
        footer_layout.addWidget(self.delete_button)

    # Metodi per le azioni dei pulsanti

    def new_record(self):
        print("New Record clicked")

    def open_file(self):
        print("Open File clicked")

    def save_file(self):
        print("Save File clicked")

    def show_about(self):
        print("About clicked")

    def add_record(self):
        print("Add Record clicked")
        row = self.table.rowCount()
        self.table.insertRow(row)

    def search_records(self):
        print("Search Records clicked")

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            print(f"Edit Record clicked - Row: {current_row}")
        else:
            print("No record selected for editing")

    def delete_record(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            print(f"Delete Record clicked - Row: {current_row} deleted")
        else:
            print("No record selected for deletion")


def main():
    app = QApplication(sys.argv)

    # Impostazione del tema dell'applicazione
    app.setStyle('Fusion')

    window = StudentManagementForm()
    window.show()
    rr = window.load_data()
    print(f"fffff: {rr}")

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
