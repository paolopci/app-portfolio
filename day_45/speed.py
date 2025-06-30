import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QGridLayout, QLabel, QLineEdit,
                             QComboBox, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class AverageSpeedCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        self.setFixedSize(400, 200)

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        layout = QGridLayout(central_widget)
        layout.setSpacing(15)

        # Riga 1: Distanza
        distance_label = QLabel("Distance:")
        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText("10")

        self.unit_select = QComboBox()
        self.unit_select.addItem("Metric (km)")
        self.unit_select.addItem("Imperial (miles)")

        layout.addWidget(distance_label, 0, 0)
        layout.addWidget(self.distance_input, 0, 1)
        layout.addWidget(self.unit_select, 0, 2)

        # Riga 2: Tempo
        time_label = QLabel("Time (hours):")
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("2")

        layout.addWidget(time_label, 1, 0)
        layout.addWidget(self.time_input, 1, 1)

        # Riga 3: Pulsante Calculate
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_average_speed)

        layout.addWidget(self.calculate_button, 2, 1)

        # Riga 4: Risultato
        self.result_label = QLabel("Average Speed: ")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.result_label, 3, 0, 1, 3)  # Span su 3 colonne

        # Stile
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 12px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)

    def calculate_average_speed(self):
        """Calcola la velocità media"""
        try:
            # Ottieni i valori di input
            distance = float(self.distance_input.text())
            time = float(self.time_input.text())

            # Verifica che i valori siano validi
            if distance <= 0 or time <= 0:
                self.result_label.setText(
                    "Average Speed: Inserire valori positivi")
                return

            # Calcola la velocità media
            average_speed = distance / time

            # Determina l'unità di misura
            if self.unit_select.currentText() == "Metric (km)":
                unit = "km/h"
            else:
                unit = "miles/h"

            # Mostra il risultato
            self.result_label.setText(
                f"Average Speed: {average_speed:.1f} {unit}")

        except ValueError:
            self.result_label.setText(
                "Average Speed: Inserire valori numerici validi")
        except Exception as e:
            self.result_label.setText(f"Average Speed: Errore - {str(e)}")


def main():
    app = QApplication(sys.argv)

    # Imposta lo stile dell'applicazione per un aspetto più moderno
    app.setStyle('Fusion')

    calculator = AverageSpeedCalculator()
    calculator.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
