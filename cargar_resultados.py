import sqlite3
import os

DB_PATH = "resultados.db"

def cargar_datos():
    ruta_part = os.path.join("output_mapreduce", "part-00000")
    if not os.path.exists(ruta_part):
        print(f"Error: No se encontró el archivo {ruta_part}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            mes TEXT NOT NULL,
            ingreso REAL NOT NULL
        )
    ''')

    # Limpiar tabla previa si fuera necesario
    cursor.execute("DELETE FROM resultados")

    # Leer part-00000 e insertar
    with open(ruta_part, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            partes = line.split("\t")
            if len(partes) == 3:
                categoria, mes, ingreso = partes[0], partes[1], float(partes[2])
                cursor.execute('''
                    INSERT INTO resultados (categoria, mes, ingreso)
                    VALUES (?, ?, ?)
                ''', (categoria, mes, ingreso))

    conn.commit()
    conn.close()
    print("¡Resultados cargados exitosamente en la base de datos!")

if __name__ == "__main__":
    cargar_datos()