# Visión General del Proyecto

El proyecto es una API RESTful sencilla construida con **Flask** que permite gestionar eventos de un calendario.  
- La capa de datos utiliza **SQLite** a través de **SQLAlchemy**, lo cual facilita el desarrollo local y la persistencia ligera.  
- Los endpoints están agrupados bajo el prefijo `/api` y manejan operaciones CRUD sobre la entidad `Evento`.  
- Se incluye una carpeta estática (`frontend`) que contiene un archivo `index.html`, sirviendo como punto de entrada para una aplicación cliente (por ejemplo, un SPA en React o Vue).  

El flujo típico es:  
1. El usuario accede a `/` y recibe el front‑end.  
2. Desde allí se realizan peticiones AJAX a los endpoints `/api/events`.  
3. Los datos son guardados/consultados en la base de datos `calendario.db`.

---

# Arquitectura del Sistema

```
┌─────────────────────┐
│  Cliente (SPA)      │
├─────────────────────┤
│  Flask App          │
│  ├── config.py      │
│  ├── __init__.py    │
│  ├── models.py      │
│  └── routes.py      │
├─────────────────────┤
│  SQLite DB (calendario.db)
└─────────────────────┘
```

- **Flask** actúa como servidor web y API.  
- **SQLAlchemy** gestiona la ORM con SQLite.  
- Los blueprints (`events_bp`) encapsulan las rutas de eventos bajo `/api`.  

## Diagrama Mermaid (API + Base de Datos)

```mermaid
graph TD
    A[Cliente] -->|HTTP GET/POST/PUT/DELETE| B[Flask App]
    B --> C{Blueprint: events}
    C --> D[Evento Model (SQLAlchemy)]
    D --> E[SQLite DB (calendario.db)]
```

---

# Endpoints de la API

## Tabla de Endpoints

| Método | Ruta                 | Descripción                                 | Parámetros Entrada                           | Respuesta 200/201 | Errores comunes |
|--------|----------------------|---------------------------------------------|----------------------------------------------|-------------------|-----------------|
| GET    | `/api/events`        | Lista eventos filtrados por rango de fechas | `start` (ISO), `end` (ISO) – query string   | `200 OK`, array de eventos | 400 (formato fecha inválido) |
| POST   | `/api/events`        | Crea un nuevo evento                        | JSON: `titulo`, `fecha_inicio`, `fecha_fin`, opcionales `descripcion`, `color` | `201 Created`, objeto del evento | 400 (campos requeridos / formato fechas) |
| PUT    | `/api/events/<id>`   | Actualiza evento existente                  | Path: `event_id`; JSON con campos a actualizar | `200 OK`, objeto actualizado | 404, 400 (formato fecha inválido) |
| DELETE | `/api/events/<id>`   | Elimina evento                              | Path: `event_id`                             | `200 OK`, mensaje de éxito | 404 |

## Ejemplos de Uso

```bash
# Obtener eventos entre dos fechas
curl "http://localhost:5000/api/events?start=2024-08-01T00:00:00&end=2024-08-31T23:59:59"

# Crear evento
curl -X POST http://localhost:5000/api/events \
     -H 'Content-Type: application/json' \
     -d '{"titulo":"Reunión","fecha_inicio":"2024-08-15T10:00:00","fecha_fin":"2024-08-15T11:00:00"}'

# Actualizar evento
curl -X PUT http://localhost:5000/api/events/1 \
     -H 'Content-Type: application/json' \
     -d '{"color":"#ff0000"}'
```

---

# Instrucciones de Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/usuario/proyecto-calendario.git
cd proyecto-calendario

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1

# 4. Generar la base de datos (se ejecutará automáticamente al arrancar)
python app.py

# 5. Acceder a la aplicación
# Navega a http://localhost:5000/ en tu navegador para ver el front‑end.
```

---

# Flujo de Datos Clave

1. **Creación**  
   - Cliente envía POST `/api/events` con JSON.  
   - Flask valida campos y fechas, crea instancia `Evento`, la persiste en SQLite.  
   - Responde con objeto JSON del nuevo evento.

2. **Lectura (con filtros)**  
   - Cliente hace GET `/api/events?start=...&end=...`.  
   - Flask convierte parámetros ISO a `datetime` y filtra la consulta.  
   - Devuelve lista de eventos serializados (`to_dict()`).

3. **Actualización**  
   - Cliente envía PUT con JSON parcial o completo.  
   - Flask busca el registro, actualiza campos proporcionados, guarda cambios.

4. **Eliminación**  
   - Cliente hace DELETE `/api/events/<id>`.  
   - Flask elimina la fila y confirma con mensaje.

---

# Extensiones Futuras (Opcional)

| Área | Posible Mejora | Justificación |
|------|----------------|---------------|
| Autenticación | Implementar JWT o OAuth2 para proteger los endpoints. | Seguridad en producción. |
| Validaciones | Usar `marshmallow` o `pydantic` para schemas de entrada/ salida. | Mayor robustez y mensajes claros. |
| Testing | Añadir pruebas unitarias con `pytest` y cobertura. | Garantizar estabilidad al refactorizar. |
| Front‑end | Integrar un framework SPA (React/Vue) dentro de `/frontend`. | Experiencia de usuario completa. |
| Base de datos | Migraciones con Alembic para versionado de esquema. | Escalabilidad a bases más grandes. |

---