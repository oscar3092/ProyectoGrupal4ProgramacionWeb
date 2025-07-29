from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import sqlite3


# Configuración de la base de datos
DATABASE_URL = "sqlite:///./formularios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo de datos
class Formulario(Base):
    __tablename__ = "formularios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100))
    intereses = Column(String(200))
    descripcion = Column(Text)

Base.metadata.create_all(bind=engine)

# Modelo para FastAPI
class FormularioSchema(BaseModel):
    nombre: str
    correo: str
    intereses: str
    descripcion: str

# Instancia de FastAPI
app = FastAPI()

# Configurar CORS para permitir el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para obtener todos los formularios
@app.get("/formularios/")
def get_formularios():
    db = SessionLocal()
    formularios = db.query(Formulario).all()
    db.close()
    return formularios

# Ruta para crear un nuevo formulario
@app.post("/formularios/")
def create_formulario(formulario: FormularioSchema):
    db = SessionLocal()
    nuevo = Formulario(
        nombre=formulario.nombre,
        correo=formulario.correo,
        intereses=formulario.intereses,
        descripcion=formulario.descripcion
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return nuevo

@app.post("/api/pipeline/run")
def ejecutar_pipeline():
    try:
        resultado = subprocess.run(
            ["python", "etl_pipeline.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode == 0:
            return {"mensaje": "Pipeline ejecutado exitosamente"}
        else:
            return JSONResponse(
                status_code=500,
                content={"error": "Error al ejecutar el pipeline", "detalle": resultado.stderr}
            )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

#Endpoint para presentar los datos limpios
@app.get("/formularios_cleaned/")
def get_formularios_limpios():
    conn = sqlite3.connect("formularios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, correo, intereses, descripcion FROM formularios_cleaned WHERE activo = 1")
    datos = cursor.fetchall()
    conn.close()
    return [
        {"id": id_, "nombre": nombre, "correo": correo,
         "intereses": intereses, "descripcion": descripcion}
        for id_, nombre, correo, intereses, descripcion in datos
    ]

#Endpoint para actualizar registros
@app.put("/formularios_cleaned/{id}")
def actualizar_formulario(id: int, datos: dict):
    conn = sqlite3.connect("formularios.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE formularios_cleaned
        SET nombre = ?, correo = ?, intereses = ?, descripcion = ?
        WHERE id = ?
    """, (datos["nombre"], datos["correo"], datos["intereses"], datos["descripcion"], id))
    conn.commit()
    conn.close()
    return {"mensaje": "Registro actualizado"}

#Endpoint para eliminar registros
@app.delete("/formularios_cleaned/{id}")
def eliminar_formulario(id: int):
    conn = sqlite3.connect("formularios.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE formularios_cleaned SET activo = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Registro eliminado"}

