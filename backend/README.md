# JWT Auth Backend

API REST construida con **FastAPI** y **Python** que implementa autenticación basada en **JSON Web Tokens (JWT)**.

---

## Tabla de contenidos

1. [Descripción](#descripción)
2. [Requisitos previos](#requisitos-previos)
3. [Configuración con Poetry (desarrollo local)](#configuración-con-poetry-desarrollo-local)
4. [Despliegue con Docker](#despliegue-con-docker)
5. [Endpoints](#endpoints)
6. [Ejemplos de uso](#ejemplos-de-uso)

---

## Descripción

La aplicación expone tres endpoints:

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/token` | Genera un JWT a partir de credenciales válidas |
| `POST` | `/token/refresh` | Refresca un JWT vigente |
| `GET` | `/me` | Devuelve el usuario autenticado (ruta protegida) |

- El token expira en **300 segundos** (5 minutos).
- Credenciales por defecto: usuario `admin`, contraseña `admin123`.
- Documentación interactiva disponible en `/docs` (Swagger UI) y `/redoc`.

---

## Requisitos previos

- Python **3.11+**
- [Poetry](https://python-poetry.org/docs/#installation) ≥ 1.8
- Docker y Docker Compose (para despliegue containerizado)

---

## Configuración con Poetry (desarrollo local)

```bash
# Clonar el repositorio y entrar a la carpeta
cd backend

# (Opcional) Exportar clave secreta segura
export SECRET_KEY=$(openssl rand -hex 32)

# Instalar dependencias
poetry install

# Activar el entorno virtual de Poetry
poetry shell

# Iniciar el servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en <http://localhost:8000>.

---

## Despliegue con Docker

### Usando `docker-compose` (recomendado)

```bash
cd backend
# Opcional: exportar una clave secreta segura
export SECRET_KEY=$(openssl rand -hex 32)
docker-compose up --build
```

### Usando `docker` directamente

```bash
cd backend
docker build -t jwt-backend .
docker run -p 8000:8000 \
  -e SECRET_KEY=$(openssl rand -hex 32) \
  jwt-backend
```

El servidor estará disponible en <http://localhost:8000>.

---

## Endpoints

### `POST /token` – Obtener token

Autentica al usuario y devuelve un JWT.

**Request** (`application/x-www-form-urlencoded`)

| Campo | Valor |
|-------|-------|
| `username` | `admin` |
| `password` | `admin123` |

**Response**

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

### `POST /token/refresh` – Refrescar token

Genera un nuevo JWT a partir de uno vigente.

**Request** (`application/json`)

```json
{
  "token": "<jwt_vigente>"
}
```

**Response**

```json
{
  "access_token": "<nuevo_jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

### `GET /me` – Usuario actual (ruta protegida)

Devuelve información del usuario autenticado.

**Header requerido**

```
Authorization: Bearer <jwt>
```

**Response**

```json
{
  "username": "admin"
}
```

---

## Ejemplos de uso

### Con `curl`

```bash
# 1. Obtener token
TOKEN=$(curl -s -X POST http://localhost:8000/token \
  -d "username=admin&password=admin123" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"

# 2. Refrescar token
curl -s -X POST http://localhost:8000/token/refresh \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"$TOKEN\"}" | python3 -m json.tool

# 3. Acceder a ruta protegida
curl -s http://localhost:8000/me \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Con Swagger UI

Abre <http://localhost:8000/docs> en tu navegador para explorar y probar la API de forma interactiva.
