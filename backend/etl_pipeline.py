import sqlite3
import csv
import json
import os
from datetime import datetime
import re

# Crear carpeta de backups si no existe
os.makedirs("backups", exist_ok=True)

# Conexión a la base de datos SQLite
conn = sqlite3.connect("formularios.db")
cursor = conn.cursor()

# Obtener todos los datos RAW
cursor.execute("SELECT * FROM formularios")
raw_data = cursor.fetchall()

# Columnas esperadas
column_names = ["id", "nombre", "correo", "intereses", "descripcion"]

# Función para validar email
def email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Limpiar y validar
cleaned_data = []
eliminados = 0
for row in raw_data:
    registro = dict(zip(column_names, row))
    if not all([registro["nombre"].strip(), registro["correo"].strip(),
                registro["intereses"].strip(), registro["descripcion"].strip()]):
        eliminados += 1
        continue
    if not email_valido(registro["correo"]):
        eliminados += 1
        continue
    registro["nombre"] = registro["nombre"].strip().title()
    registro["correo"] = registro["correo"].strip().lower()
    registro["intereses"] = registro["intereses"].strip()
    registro["descripcion"] = registro["descripcion"].strip()
    cleaned_data.append(registro)

# Limpiar tabla cleaned antes de insertar
for reg in cleaned_data:
    cursor.execute("SELECT activo FROM formularios_cleaned WHERE id = ?", (reg["id"],))
    row = cursor.fetchone()

    if not row:
        # Si no existe, insertamos
        cursor.execute("""
            INSERT INTO formularios_cleaned (id, nombre, correo, intereses, descripcion, activo)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (reg["id"], reg["nombre"], reg["correo"], reg["intereses"], reg["descripcion"]))

conn.commit()

# Backups CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
raw_csv_path = f"backups/raw_{timestamp}.csv"
cleaned_csv_path = f"backups/cleaned_{timestamp}.csv"

with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(column_names)
    writer.writerows(raw_data)

with open(cleaned_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","nombre", "correo", "intereses", "descripcion"])
    writer.writeheader()
    writer.writerows(cleaned_data)

# Log JSON
log_data = {
    "timestamp": timestamp,
    "total_raw": len(raw_data),
    "total_cleaned": len(cleaned_data),
    "eliminados": eliminados,
    "raw_csv": raw_csv_path,
    "cleaned_csv": cleaned_csv_path
}

with open(f"backups/log_{timestamp}.json", "w", encoding="utf-8") as f:
    json.dump(log_data, f, indent=4)

conn.close()
print("ETL completado exitosamente.")
