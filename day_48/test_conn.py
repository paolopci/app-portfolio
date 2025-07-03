import mysql.connector
from mysql.connector import Error


def test_basic_connection():
    """Test di connessione base senza specificare il database"""
    print("=== TEST CONNESSIONE BASE ===")

    try:
        # Prima prova: connessione senza database specifico
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Venerina@07',
            charset='utf8mb4'
        )

        if connection.is_connected():
            print("✓ Connessione a MySQL riuscita!")

            cursor = connection.cursor()

            # Verifica database esistenti
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            print("\nDatabase disponibili:")
            for db in databases:
                print(f"  - {db[0]}")

            # Verifica se SchoolDb esiste
            schooldb_exists = any(db[0] == 'SchoolDb' for db in databases)

            if schooldb_exists:
                print("\n✓ Database 'SchoolDb' trovato!")

                # Connessione al database specifico
                cursor.execute("USE SchoolDb;")

                # Verifica tabelle
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                print("\nTabelle in SchoolDb:")
                for table in tables:
                    print(f"  - {table[0]}")

                # Test query semplice
                if tables:
                    try:
                        cursor.execute("SELECT COUNT(*) FROM students;")
                        student_count = cursor.fetchone()[0]
                        print(f"\n✓ Tabella students: {student_count} record")

                        cursor.execute("SELECT COUNT(*) FROM courses;")
                        course_count = cursor.fetchone()[0]
                        print(f"✓ Tabella courses: {course_count} record")

                    except Error as e:
                        print(f"⚠ Errore nel conteggio record: {e}")

            else:
                print("\n❌ Database 'SchoolDb' NON TROVATO!")
                print("Creazione database SchoolDb...")

                try:
                    cursor.execute("CREATE DATABASE SchoolDb;")
                    cursor.execute("USE SchoolDb;")

                    # Creazione tabelle
                    cursor.execute("""
                        CREATE TABLE students (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            courses VARCHAR(255),
                            mobile VARCHAR(20)
                        );
                    """)

                    cursor.execute("""
                        CREATE TABLE courses (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            course VARCHAR(255) NOT NULL UNIQUE
                        );
                    """)

                    print("✓ Database e tabelle creati con successo!")

                except Error as e:
                    print(f"❌ Errore nella creazione del database: {e}")

            cursor.close()
            connection.close()
            print("\n✓ Connessione chiusa correttamente")
            return True

    except Error as e:
        print(f"❌ Errore di connessione: {e}")
        print(f"Codice errore: {e.errno}")

        if e.errno == 1045:
            print("Suggerimento: Verifica username e password")
        elif e.errno == 2003:
            print("Suggerimento: Verifica che MySQL sia in esecuzione")
            print("Comando: docker ps | grep mysql")
        elif e.errno == 1251:
            print("Suggerimento: Problema di autenticazione MySQL 8.0")
            print("Prova questo comando in MySQL:")
            print(
                "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Venerina@07';")

        return False

    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return False


def test_with_corrected_config():
    """Test con la configurazione corretta dal tuo codice"""
    print("\n=== TEST CON CONFIGURAZIONE CORRETTA ===")

    try:
        connection = mysql.connector.connect(
            host='localhost',  # Nota: era 'localhost1' nel codice originale
            port=3306,
            database='SchoolDb',
            user='root',
            password='Venerina@07',
            charset='utf8mb4',
            autocommit=True
        )

        if connection.is_connected():
            print("✓ Connessione con configurazione corretta riuscita!")

            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            current_db = cursor.fetchone()
            print(f"Database attuale: {current_db[0]}")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"❌ Errore: {e}")
        return False


if __name__ == "__main__":
    print("Avvio test di connessione...")

    # Test 1: Connessione base
    if test_basic_connection():
        print("\n" + "="*50)
        # Test 2: Connessione con configurazione specifica
        test_with_corrected_config()

    print("\n=== FINE TEST ===")
