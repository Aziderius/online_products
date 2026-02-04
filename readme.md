# Project Products API

API REST desarrollada con **FastAPI**, **SQLAlchemy** y **PostgreSQL**, pensada principalmente para **práctica con Apigee** (policies como Extract Variables, Assign Message, validación de headers, etc.).

El proyecto implementa un CRUD básico de **categorías** y **productos**, con relaciones entre tablas y validaciones simples.

---

## Tecnologías utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn
- Pydantic

---

## Estructura general del proyecto

```
project-products/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   ├── database.py
│   │   └── dependencies.py
│   ├── models/
│   │   └── models.py
│   ├── routers/
│   │   ├── categories.py
│   │   └── products.py
│   ├── schemas/
│   │   ├── category.py
│   │   └── product.py
│   └── main.py
│
├── script_para_db.txt
├── requirements.txt
├── .env
└── README.md
```

---

## Crear entorno virtual

Desde la raíz del proyecto:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Instalación de dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables (ejemplo):

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=online_products

INTERNAL_API_TOKEN=super-secret-internal-key
```

---

## Base de datos

El archivo **`script_para_db.txt`** contiene:

- Creación de tablas (`categories`, `products`)
- Relaciones entre tablas
- Inserción de datos iniciales

Ejecuta el script completo en tu gestor de base de datos (por ejemplo **DBeaver** o `psql`) antes de iniciar la API.

---

## Ejecutar la API en local

Con el entorno virtual activado:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O simplemente ejecuta el siguiente comando para que FastAPI asigne host y port por defecto:

```bash
uvicorn app.main:app --reload
```

---

## Documentación automática

FastAPI genera documentación automáticamente:

- Swagger UI:

  ```
  http://localhost:8000/docs
  ```

- OpenAPI JSON:
  ```
  http://localhost:8000/openapi.json
  ```

> El archivo OpenAPI puede convertirse a YAML si se desea usar directamente en Apigee.

---

## Seguridad

La API utiliza un **header interno** para validación básica:

```http
INTERNAL-API-KEY: <valor definido en .env>
```

Esta validación se implementa a nivel de dependencias de FastAPI y es ideal para pruebas con Apigee.

---

## Objetivo del proyecto

- Practicar diseño de APIs REST
- Practicar relaciones con SQLAlchemy
- Servir como backend de prueba para **Apigee X**
- Experimentar con policies como:
  - Extract Variables
  - Assign Message
  - Validate Headers

---

## Estado del proyecto

✔ Funcional
✔ CRUD completo
✔ Relaciones entre entidades
✔ Listo para pruebas con Apigee

---

## Autor

Aziderius

Proyecto desarrollado con fines educativos y de práctica.

---

Siéntete libre de clonar, modificar y experimentar.
