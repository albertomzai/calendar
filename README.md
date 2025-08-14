# Visión General del Proyecto

Este proyecto es un **calendario interactivo** construido con Flask (backend) y FullCalendar (frontend). Su objetivo principal es permitir a los usuarios crear, leer, actualizar y eliminar eventos de calendario mediante una API RESTful sencilla. Los datos se persisten en una base de datos SQLite gestionada por SQLAlchemy.

- **Backend**: Exposea endpoints `/api/events` para CRUD sobre la entidad `Evento`.  
- **Frontend**: Una página estática que consume esos endpoints, mostrando los eventos en un calendario y permitiendo su edición mediante modales.  

El flujo típico es:

1. El cliente solicita `/api/events?start=...&end=...` para cargar el rango visible del calendario.  
2. Cuando se crea/edita/elimina un evento, la API devuelve el objeto actualizado o una confirmación, y el frontend refresca la vista.

---

# Arquitectura del Sistema

## Componentes Principales

| Componente | Tecnología | Responsabilidad |
|------------|------------|-----------------|
| **Flask** | Python 3.x | Servidor HTTP, manejo de rutas y errores. |
| **SQLAlchemy** | ORM | Mapeo objeto-relacional para la tabla `Evento`. |
| **SQLite** | BD local | Persistencia de datos en el archivo `calendario.db`. |
| **FullCalendar** | JS | Renderizado del calendario en el navegador. |
| **HTML/CSS/JS** | Frontend estático | Interfaz de usuario y lógica cliente. |

## Diagrama de Flujo

```mermaid
flowchart TD
    A[Usuario] --> B{Interacción}
    B -->|Crea evento| C[Frontend: Modal]
    C --> D[POST /api/events]
    D --> E[Flask -> SQLAlchemy]
    E --> F[SQLite]
    F --> G[Respuesta JSON]
    G --> H[Frontend actualiza vista]

    B -->|Edita evento| I[Frontend: Modal con datos prellenados]
    I --> J[PUT /api/events/{id}]
    J --> K[Flask -> SQLAlchemy]
    K --> L[SQLite]
    L --> M[Respuesta JSON]
    M --> H

    B -->|Elimina evento| N[DELETE /api/events/{id}]
    N --> O[Flask -> SQLAlchemy]
    O --> P[SQLite]
    P --> Q[Respuesta JSON]
    Q --> H
```

---

# Endpoints de la API

## Tabla de Rutas

| Método | Ruta | Descripción | Parámetros | Cuerpo | Respuesta |
|--------|------|-------------|------------|--------|-----------|
| **GET** | `/api/events` | Obtener eventos. | `start`, `end` (query, ISO 8601) | N/A | `200 OK`: lista de objetos evento |
| **POST** | `/api/events` | Crear un nuevo evento. | N/A | JSON: `{titulo, fecha_inicio, fecha_fin, descripcion?, color?}` | `201 Created`: objeto creado |
| **PUT** | `/api/events/<int:event_id>` | Actualizar evento existente. | `event_id` (path) | JSON con campos opcionales a actualizar | `200 OK`: objeto actualizado |
| **DELETE** | `/api/events/<int:event_id>` | Eliminar evento. | `event_id` (path) | N/A | `200 OK`: mensaje de confirmación |

### Ejemplo de Respuesta

```json
{
  "id": 1,
  "titulo": "Reunión",
  "descripcion": "",
  "fecha_inicio": "2025-08-15T10:00:00",
  "fecha_fin": "2025-08-15T11:00:00",
  "color": "#FFFFFF"
}
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tuusuario/calendario-interactivo.git
   cd calendario-interactivo
   ```

2. **Crear entorno virtual**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar la base de datos** (solo la primera vez)  
   ```bash
   python
   >>> from backend import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ...
   >>> exit()
   ```

5. **Ejecutar el servidor de desarrollo**  
   ```bash
   python app.py
   ```

6. **Abrir la aplicación**  
   Navega a `http://127.0.0.1:5000/` en tu navegador.

---

# Flujo de Datos Clave

1. **Creación**  
   - El usuario rellena el modal y envía un POST.  
   - Flask recibe, valida y crea una instancia `Evento`.  
   - SQLAlchemy persiste la entidad en SQLite.  
   - Se devuelve el objeto serializado.

2. **Lectura (Filtro por rango)**  
   - Frontend hace GET con parámetros `start`/`end`.  
   - `_parse_iso()` convierte las cadenas ISO a objetos `datetime`.  
   - Consulta SQLAlchemy filtra por `fecha_inicio >= start` y `fecha_fin <= end`.  
   - Se serializa cada evento a JSON.

3. **Actualización**  
   - PUT con los campos modificados.  
   - Flask busca el registro (`get_or_404`).  
   - Campos presentes en el payload se actualizan individualmente.  
   - Commit y respuesta.

4. **Eliminación**  
   - DELETE solicita la entidad por ID.  
   - Se elimina de la sesión y se confirma con mensaje JSON.

---

# Extensiones Futuras

| Área | Posible Mejora |
|------|----------------|
| **Autenticación** | Implementar JWT o OAuth para proteger los endpoints, evitando que cualquier usuario modifique el calendario. |
| **Sincronización en tiempo real** | Integrar Socket.IO para notificar a todos los clientes cuando un evento cambia. |
| **Soporte de múltiples usuarios** | Añadir tabla `User` y relacionar eventos con propietarios; añadir filtros por usuario. |
| **Exportación/Importación** | Endpoints `/api/events/export` y `/api/events/import` para manejar archivos iCal o CSV. |
| **Notificaciones** | Enviar correos electrónicos o push notifications cuando un evento se acerca. |

---