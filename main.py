# generar_dataset.py
# Uso: python3 generar_dataset.py   (te pedira tu matricula)
import sys, random, csv
from datetime import datetime, timedelta

if len(sys.argv) == 2:
    matricula = sys.argv[1].strip()
else:
    matricula = input("Ingresa tu matricula (9 digitos): ").strip()

while not (matricula.isdigit() and len(matricula) == 9):
    matricula = input("Matricula invalida. Debe tener exactamente 9 digitos: ").strip()

random.seed(matricula)
print(f"Generando dataset para {matricula}... (tarda unos minutos)")

N = 5_000_000
tiendas = [f"T{str(i).zfill(3)}" for i in range(1, random.randint(15, 40))]
categorias = ["Electronica", "Abarrotes", "Ropa", "Hogar", "Juguetes",
              "Farmacia", "Deportes", "Papeleria", "Mascotas", "Bebidas"]
productos = {c: [f"{c[:3].upper()}-{j:04d}" for j in range(1, random.randint(30, 80))]
             for c in categorias}
pagos = ["Efectivo", "Tarjeta", "Transferencia", "Vales"]
inicio = datetime(2025, 1, 1)

with open(f"ventas_{matricula}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "fecha_hora", "tienda", "categoria", "producto",
                "cantidad", "precio_unitario", "metodo_pago"])
    for i in range(1, N + 1):
        cat = random.choice(categorias)
        fecha = inicio + timedelta(seconds=random.randint(0, 365 * 24 * 3600))
        w.writerow([i, fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    random.choice(tiendas), cat, random.choice(productos[cat]),
                    random.randint(1, 12), round(random.uniform(5, 2500), 2),
                    random.choice(pagos)])
print("Listo")

#######api
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()
DB_PATH = "resultados.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class RegistroUpdate(BaseModel):
    ingreso: float

# GET /resultados -> Todos los registros
@app.get("/resultados")
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, categoria, mes, ingreso FROM resultados")
    filas = cursor.fetchall()
    conn.close()
    return [dict(f) for f in filas]

# GET /resultados/<categoria> -> Filtro por clave (categoría)
@app.get("/resultados/{categoria}")
def get_por_categoria(categoria: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, categoria, mes, ingreso FROM resultados WHERE LOWER(categoria) = LOWER(?)", (categoria,))
    filas = cursor.fetchall()
    conn.close()
    if not filas:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return [dict(f) for f in filas]

# POST /resultados -> Endpoint de escritura (CRUD)
@app.post("/resultados")
def crear_registro(categoria: str, mes: str, ingreso: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resultados (categoria, mes, ingreso) VALUES (?, ?, ?)", (categoria, mes, ingreso))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {"id": nuevo_id, "categoria": categoria, "mes": mes, "ingreso": ingreso}

# DELETE /resultados/<id> -> Endpoint de eliminación (CRUD)
@app.delete("/resultados/{registro_id}")
def eliminar_registro(registro_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resultados WHERE id = ?", (registro_id,))
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()
    if filas_afectadas == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": f"Registro {registro_id} eliminado exitosamente"}