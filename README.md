# Compliance Platform (Backend + Frontend)

Este repositorio incluye:

- `backend/`: API JWT con FastAPI (`/token`, `/token/refresh`, `/me`).
- `frontend/`: aplicación React con login y pantalla de bienvenida protegida.

## Flujo funcional

1. El usuario inicia sesión en `/login`.
2. El frontend envía credenciales a `POST /token`.
3. Si son válidas, guarda `access_token` en `sessionStorage`.
4. El usuario es redirigido a `/welcome`.
5. Si no hay token de sesión, no se permite entrar a bienvenida y se redirige a login.

## Requisitos

- Python 3.11+
- Poetry
- Node.js 20+

## Ejecución del backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

Backend disponible en `http://localhost:8000`.

## Ejecución del frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend disponible en `http://localhost:5173`.

> El frontend usa proxy de Vite para `http://localhost:8000` en rutas `/token` y `/me`.

## Credenciales de prueba

- Usuario: `admin`
- Contraseña: `admin123`

## Diseño

El estándar visual está documentado en [`DESIGN.md`](./DESIGN.md) y se aplica en la interfaz del frontend.

## Scripts útiles

### Backend

```bash
cd backend
poetry run pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
```
