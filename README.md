# Proyecto Web Full Stack - Trabajo Grupal #4

## Miembros del equipo

* Jafet Rojas
* Jose Ugalde
* Oscar Umaña

## Tecnologías utilizadas

* **Frontend**: HTML, CSS, JavaScript Vanilla (Fetch API)
* **Backend**: FastAPI + SQLAlchemy
* **Base de datos**: SQLite (por defecto) o MySQL
* **ETL Pipeline**: Python puro
* **Respaldo y logs**: CSV + JSON

---

## Funcionalidades

### Formulario web con API REST

- Permite ingresar registros (nombre, correo, intereses, descripción)
- Los datos se almacenan en la base de datos RAW (`formularios`)
- Se visualizan desde la tabla limpia (`formularios_cleaned`)

### Pipeline de limpieza (ETL)

- Automatiza la limpieza, validación y respaldo de datos
- Elimina registros inválidos (nulos, correos mal formateados, etc.)
- Inserta solo registros nuevos a la tabla limpia (`formularios_cleaned`)
- Respeta los registros ya editados o eliminados manualmente
- Crea respaldos en formato `.csv` y logs `.json` con métricas
- Se puede ejecutar:
  - Automáticamente
  - Manualmente desde el navegador (botón "Ejecutar Pipeline")

### Edición y eliminación desde el navegador

- Se pueden editar campos directamente desde la tabla visual
- Los registros se actualizan mediante `PUT` en la API
- Las eliminaciones son lógicas (soft delete), conservando historial
- El pipeline no vuelve a insertar registros eliminados

---

## Pasos para ejecutar

### Backend

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Verificar en navegador:

```
http://localhost:8000/docs
```

---

### Frontend

1. Desde la carpeta frontend:

```bash
cd frontend
python -m http.server 5500
```

2. Acceder en el navegador:

```
http://localhost:5500/index.html
```

---

### Ejecutar el pipeline manualmente

- Ir a la página principal
- Presionar el botón **"Ejecutar Pipeline"**
- Se procesarán los datos nuevos y se generarán backups en `/backups`
