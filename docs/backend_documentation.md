# Visión General del Proyecto
Este proyecto es una API RESTful sencilla construida con **Flask** y **SQLAlchemy**, diseñada para gestionar eventos de un calendario. La lógica está separada en tres capas principales:

1. **Modelo (`models.py`)** – Define la entidad `Evento` que se almacena en SQLite.
2. **Rutas (`routes.py`)** – Exponen los endpoints `/api/events` y `/api/events/<id>` para crear, leer, actualizar y eliminar eventos.
3. **Aplicación (`__init__.py`)** – Configura Flask, la base de datos y registra el blueprint de la API. También sirve el frontend estático (un `index.html` que debe estar en la carpeta `frontend`).

El flujo típico es:
- El cliente envía una petición HTTP al endpoint correspondiente.
- Flask procesa la solicitud, interactúa con SQLAlchemy para consultar o modificar la base de datos y devuelve un JSON estructurado.

---

# Arquitectura del Sistema
La arquitectura sigue el patrón **MVC** simplificado:

| Componente | Responsabilidad |
|------------|-----------------|
| **Flask App** | Maneja las rutas HTTP, sirve archivos estáticos y gestiona la configuración global. |
| **Blueprint `api_bp`** | Agrupa todas las rutas de la API bajo `/api`. |
| **Modelo `Evento`** | Representa la tabla `eventos` en SQLite; incluye método `to_dict()` para serializar a JSON. |
| **SQLAlchemy (`db`)** | ORM que facilita consultas y transacciones con la base de datos SQLite. |

## Diagrama Mermaid
```mermaid
graph TD
    A[Cliente] --> B[Flask App]
    B --> C{Rutas}
    C --> D[GET /api/events]
    C --> E[POST /api/events]
    C --> F[PUT /api/events/<id>]
    C --> G[DELETE /api/events/<id>]
    D & E & F & G --> H[SQLAlchemy ORM]
    H --> I[SQLite: calendario.db]
    B --> J[Frontend static files (index.html)]
```

---

# Endpoints de la API
| Método | Ruta | Parámetros | Descripción | Respuesta |
|--------|------|------------|-------------|-----------|
| **GET** | `/api/events` | `start`, `end` (opcional, ISO 8601) | Devuelve todos los eventos, filtrados por rango de fechas si se proporcionan. | `200 OK` con lista JSON de eventos. |
| **POST** | `/api/events` | Cuerpo JSON (`titulo`, `fecha_inicio`, `fecha_fin`; opcional: `descripcion`, `color`) | Crea un nuevo evento. | `201 Created` con el objeto creado. |
| **PUT** | `/api/events/<int:event_id>` | Cuerpo JSON (cualquier campo de Evento) | Actualiza los campos del evento especificado. | `200 OK` con el objeto actualizado. |
| **DELETE** | `/api/events/<int:event_id>` | Ninguno | Elimina el evento. | `204 No Content`. |

### Ejemplo de Payload
```json
{
  "titulo": "Reunión de equipo",
  "descripcion": "Discusión de avances del proyecto.",
  "fecha_inicio": "2025-09-01T10:00:00",
  "fecha_fin": "2025-09-01T11:00:00",
  "color": "#ff5733"
}
```

---

# Instrucciones de Instalación y Ejecución
1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu_usuario/calendario-api.git
   cd calendario-api
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install Flask SQLAlchemy
   ```

4. **Inicializar la base de datos (solo una vez)**  
   ```bash
   python -c "from app import db; db.create_all()"
   ```
   *Esto crea `calendario.db` en el directorio raíz.*

5. **Ejecutar la aplicación**  
   ```bash
   export FLASK_APP=app  # En Windows: set FLASK_APP=app
   flask run --port 5000
   ```

6. **Acceder al frontend**  
   Navega a `http://localhost:5000/` para cargar el `index.html` (debe existir en la carpeta `frontend`).  

---

# Flujo de Datos Clave
1. **Solicitud GET `/api/events?start=...&end=...`**  
   - Flask recibe parámetros, convierte strings ISO a `datetime`.
   - Consulta SQLAlchemy con filtros (`>= start`, `<= end`).
   - Cada objeto `Evento` se serializa vía `to_dict()`.
   - Se devuelve JSON.

2. **Solicitud POST `/api/events`**  
   - Flask valida campos obligatorios.
   - Convierte fechas, crea instancia `Evento`.
   - Añade a la sesión y confirma (`commit`).
   - Devuelve el objeto creado en formato JSON.

3. **Solicitud PUT `/api/events/<id>`**  
   - Busca evento por ID; 404 si no existe.
   - Actualiza campos presentes en el cuerpo JSON, con validación de fechas.
   - Confirma cambios y devuelve el objeto actualizado.

4. **Solicitud DELETE `/api/events/<id>`**  
   - Busca evento por ID; 404 si no existe.
   - Elimina del session, confirma (`commit`).
   - Responde `204 No Content`.

---

# Extensiones Futuras
- **Autenticación y autorización** (JWT o OAuth) para proteger los endpoints.
- **Paginación y ordenamiento** en la lista de eventos.
- **Notificaciones por correo** cuando se cree o modifique un evento.
- **Persistencia en PostgreSQL** con migraciones Alembic para producción.
- **Frontend React/Vue** que consuma la API, con manejo avanzado del calendario (drag‑and‑drop).