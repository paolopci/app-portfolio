import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Tuple
import time


class DatabaseManager:
    """Gestisce le operazioni del database MySQL per il sistema di gestione studenti"""

    def __init__(self):
        self.connection_config = {
            'host': 'localhost',  # CORREZIONE: rimosso '1' da 'localhost1'
            'port': 3306,
            'database': 'SchoolDb',
            'user': 'root',
            'password': 'Venerina@07',
            'charset': 'utf8mb4',
            'autocommit': True,
            'connect_timeout': 10,  # Timeout di connessione
            'raise_on_warnings': True
        }
        self.connection = None
        self.max_retries = 3
        self.retry_delay = 1

    def connect(self) -> bool:
        """Stabilisce la connessione al database MySQL con retry"""
        for attempt in range(self.max_retries):
            try:
                print(
                    f"Tentativo di connessione {attempt + 1}/{self.max_retries}...")
                self.connection = mysql.connector.connect(
                    **self.connection_config)

                if self.connection.is_connected():
                    db_info = self.connection.get_server_info()
                    print(f"Connessione al database MySQL stabilita con successo")
                    print(f"Versione server: {db_info}")
                    return True

            except Error as e:
                print(f"Tentativo {attempt + 1} fallito: {e}")
                if e.errno == 1045:  # Access denied
                    print("Errore di autenticazione - verifica username e password")
                    break  # Non riprovare per errori di autenticazione
                elif e.errno == 2003:  # Can't connect
                    print("Server MySQL non raggiungibile")
                elif e.errno == 1049:  # Database non esiste
                    print("Database 'SchoolDb' non esiste - tentativo di creazione...")
                    if self.create_database():
                        continue  # Riprova la connessione
                    else:
                        break
                elif e.errno == 1251:  # Client does not support
                    print("Problema di autenticazione MySQL 8.0")
                    print(
                        "Esegui: ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Venerina@07';")
                    break

                if attempt < self.max_retries - 1:
                    print(
                        f"Attendo {self.retry_delay} secondi prima del prossimo tentativo...")
                    time.sleep(self.retry_delay)

            except Exception as e:
                print(f"Errore generico durante la connessione: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        print("Impossibile stabilire la connessione al database")
        return False

    def create_database(self) -> bool:
        """Crea il database SchoolDb se non esiste"""
        try:
            # Connessione senza database specifico
            temp_config = self.connection_config.copy()
            del temp_config['database']

            temp_connection = mysql.connector.connect(**temp_config)
            cursor = temp_connection.cursor()

            # Crea database
            cursor.execute("CREATE DATABASE IF NOT EXISTS SchoolDb;")
            cursor.execute("USE SchoolDb;")

            # Crea tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    courses VARCHAR(255),
                    mobile VARCHAR(20)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course VARCHAR(255) NOT NULL UNIQUE
                );
            """)

            temp_connection.commit()
            cursor.close()
            temp_connection.close()

            print("Database e tabelle creati con successo!")
            return True

        except Error as e:
            print(f"Errore nella creazione del database: {e}")
            return False

    def disconnect(self):
        """Chiude la connessione al database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connessione al database chiusa")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Tuple]]:
        """Esegue una query SELECT e restituisce i risultati"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            results = cursor.fetchall()
            cursor.close()
            return results

        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
            print(f"Query: {query}")
            if params:
                print(f"Parametri: {params}")
            return None

    def execute_non_query(self, query: str, params: tuple = None) -> bool:
        """Esegue una query INSERT, UPDATE, DELETE"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return False

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()

            print(
                f"Query eseguita con successo. Righe interessate: {affected_rows}")
            return True

        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
            print(f"Query: {query}")
            if params:
                print(f"Parametri: {params}")
            try:
                self.connection.rollback()
            except:
                pass
            return False

    def get_all_students(self) -> List[List[str]]:
        """Recupera tutti gli studenti dalla tabella students"""
        query = "SELECT id, name, courses, mobile FROM students ORDER BY id"
        results = self.execute_query(query)

        if results:
            return [[str(row[0]), row[1], row[2], row[3]] for row in results]
        return []

    def get_all_courses(self) -> List[str]:
        """Recupera tutti i corsi dalla tabella courses"""
        query = "SELECT course FROM courses ORDER BY course"
        results = self.execute_query(query)

        if results:
            return [row[0] for row in results]
        return []

    def insert_student(self, name: str, course: str, mobile: str) -> bool:
        """Inserisce un nuovo studente nella tabella students"""
        query = "INSERT INTO students (name, courses, mobile) VALUES (%s, %s, %s)"
        params = (name, course, mobile)
        return self.execute_non_query(query, params)

    def update_student(self, student_id: int, name: str, course: str, mobile: str) -> bool:
        """Aggiorna un studente esistente"""
        query = "UPDATE students SET name = %s, courses = %s, mobile = %s WHERE id = %s"
        params = (name, course, mobile, student_id)
        return self.execute_non_query(query, params)

    def delete_student(self, student_id: int) -> bool:
        """Elimina uno studente dalla tabella students"""
        query = "DELETE FROM students WHERE id = %s"
        params = (student_id,)
        return self.execute_non_query(query, params)

    def get_next_student_id(self) -> int:
        """Ottiene il prossimo ID disponibile per un nuovo studente"""
        query = "SELECT MAX(id) FROM students"
        results = self.execute_query(query)

        if results and results[0][0] is not None:
            return results[0][0] + 1
        return 1

    def initialize_sample_data(self):
        """Inizializza il database con dati di esempio se vuoto"""
        try:
            # Controlla se ci sono già dati
            existing_students = self.get_all_students()
            if existing_students:
                print("Il database contiene già dati studenti")
                return True

            # Inserisce i corsi di esempio
            sample_courses = [
                "Biology", "Math", "Astronomy", "Physics",
                "Computer Science", "Mathematics", "Chemistry"
            ]

            print("Inserimento corsi di esempio...")
            for course in sample_courses:
                query = "INSERT IGNORE INTO courses (course) VALUES (%s)"
                if not self.execute_non_query(query, (course,)):
                    print(f"Errore nell'inserimento del corso: {course}")

            # Inserisce gli studenti di esempio
            sample_students = [
                ('Mario Rossi', 'Computer Science', '333-1234567'),
                ('Anna Bianchi', 'Mathematics', '333-2345678'),
                ('Luca Verdi', 'Physics', '333-3456789'),
                ('Sara Neri', 'Chemistry', '333-4567890'),
                ('Marco Blu', 'Biology', '333-5678901')
            ]

            print("Inserimento studenti di esempio...")
            for student in sample_students:
                if not self.insert_student(student[0], student[1], student[2]):
                    print(
                        f"Errore nell'inserimento dello studente: {student[0]}")

            print("Dati di esempio inseriti nel database")
            return True

        except Exception as e:
            print(f"Errore durante l'inizializzazione dei dati: {e}")
            return False

    def test_connection(self) -> bool:
        """Testa la connessione al database"""
        print("Avvio test di connessione...")

        if self.connect():
            try:
                # Test query semplice
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                cursor.close()

                if result and result[0] == 1:
                    print("Test di connessione: SUCCESSO")
                    self.disconnect()
                    return True

            except Error as e:
                print(f"Errore durante il test: {e}")

        print("Test di connessione: FALLITO")
        return False

    def get_database_info(self) -> dict:
        """Ottiene informazioni sul database"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return {}

        try:
            cursor = self.connection.cursor()
            info = {}

            # Versione server
            info['server_version'] = self.connection.get_server_info()

            # Database corrente
            cursor.execute("SELECT DATABASE();")
            current_db = cursor.fetchone()
            info['current_database'] = current_db[0] if current_db else None

            # Lista tabelle
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            info['tables'] = [table[0] for table in tables]

            # Conteggio record per tabella
            info['table_counts'] = {}
            for table_name in info['tables']:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                info['table_counts'][table_name] = count

            cursor.close()
            return info

        except Error as e:
            print(f"Errore nel recupero informazioni database: {e}")
            return {}


# Istanza globale del database manager
db_manager = DatabaseManager()

# Test di base se eseguito direttamente
if __name__ == "__main__":
    print("=== TEST DATABASE MANAGER ===")

    # Test connessione
    if db_manager.test_connection():
        print("\n✓ Connessione riuscita!")

        # Mostra informazioni database
        info = db_manager.get_database_info()
        if info:
            print(f"\nInformazioni database:")
            print(f"  Server: {info.get('server_version', 'N/A')}")
            print(f"  Database: {info.get('current_database', 'N/A')}")
            print(f"  Tabelle: {info.get('tables', [])}")
            print(f"  Conteggi: {info.get('table_counts', {})}")
    else:
        print("\n❌ Connessione fallita!")
