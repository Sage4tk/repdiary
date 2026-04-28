# RepDiary API

REST API for tracking workout sessions and exercises, with voice-to-exercise transcription powered by OpenAI Whisper and Claude AI.

## Stack

- Django 6 + Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- OpenAI Whisper (transcription)
- Anthropic Claude Haiku (exercise extraction)

## Base URL

```
http://localhost:8000
```

## Authentication

All protected routes require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Tokens are obtained via `/auth/login/` or `/auth/register/`.

---

## Endpoints

### Auth

#### Register
```
POST /auth/register/
```

**Body**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret",
  "first_name": "John",
  "last_name": "Doe",
  "birth": "1995-04-20"
}
```

**Response** `200`
```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

---

#### Login
```
POST /auth/login/
```

**Body**
```json
{
  "email": "john@example.com",
  "password": "secret"
}
```

**Response** `200`
```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

---

#### Refresh Token
```
POST /auth/refresh/
```

**Body**
```json
{
  "refresh": "<refresh_token>"
}
```

**Response** `200`
```json
{
  "access": "..."
}
```

---

### User

#### Get Current User
```
GET /user/
```
Protected.

**Response** `200`
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "birth": "1995-04-20"
}
```

---

#### Update Current User
```
PUT /user/
```
Protected. All fields optional (partial update).

**Body**
```json
{
  "first_name": "Johnny",
  "birth": "1995-04-20"
}
```

**Response** `200` — updated user object

---

### Sessions

#### Get All Sessions
```
GET /exercise/session/
```
Protected.

**Response** `200`
```json
[
  {
    "id": "uuid",
    "title": "Morning Workout",
    "date": "2026-04-22T08:00:00Z",
    "created_at": "2026-04-22T08:01:00Z"
  }
]
```

---

#### Get Session by ID
```
GET /exercise/session/<id>/
```
Protected.

**Query Params**

| Param | Value | Description |
|-------|-------|-------------|
| `include` | `exercises` | Include exercises in the response |

**Response** `200`
```json
{
  "id": "uuid",
  "title": "Morning Workout",
  "date": "2026-04-22T08:00:00Z",
  "created_at": "2026-04-22T08:01:00Z",
  "exercises": []
}
```

---

#### Create Session
```
POST /exercise/session/
```
Protected.

**Body**
```json
{
  "title": "Morning Workout",
  "date": "2026-04-22T08:00:00Z"
}
```

**Response** `201` — created session object

---

#### Update Session
```
PUT /exercise/session/<id>/
```
Protected. All fields optional.

**Body**
```json
{
  "title": "Evening Workout"
}
```

**Response** `200` — updated session object

---

#### Delete Session
```
DELETE /exercise/session/<id>/
```
Protected.

**Response** `204`

---

### Exercises

#### Get Exercises by Session
```
GET /exercise/session/exercises/<session_id>/
```
Protected.

**Response** `200`
```json
[
  {
    "id": "uuid",
    "session": "uuid",
    "exercise": "Bench Press",
    "reps": 10,
    "sets": 3,
    "length": null,
    "notes": null
  }
]
```

---

#### Create Exercise
```
POST /exercise/exercise/
```
Protected.

**Body**
```json
{
  "session": "uuid",
  "exercise": "Bench Press",
  "reps": 10,
  "sets": 3,
  "length": null,
  "notes": "Felt strong"
}
```

**Response** `200` — created exercise object

---

#### Update Exercise
```
PUT /exercise/exercise/<id>/
```
Protected. All fields optional.

**Body**
```json
{
  "reps": 12
}
```

**Response** `202` — updated exercise object

---

#### Delete Exercise
```
DELETE /exercise/exercise/<id>/
```
Protected.

**Response** `200`
```json
{
  "message": "Exercise deleted"
}
```

---

### Voice Transcription

#### Transcribe Voice to Exercises
```
POST /exercise/transcribe/
```
Protected. Accepts a voice recording, transcribes it with Whisper, and uses Claude Haiku to extract and save exercises to a session.

**Request** `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `speech` | file | Audio file (mp3, wav, m4a, etc.) |
| `session_id` | string (UUID) | Session to attach exercises to |

**Response** `201`
```json
{
  "transcript": "I did 3 sets of bench press for 10 reps...",
  "created": 2
}
```

---

## Running Locally

### With Python
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### With Docker
```bash
docker build -t repdiary-backend .
docker run --env-file .env -p 8000:8000 repdiary-backend
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DEBUG` | `True` or `False` |
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Postgres connection string |
| `OPENAI_API_KEY` | For Whisper transcription |
| `ANTHROPIC_API_KEY` | For Claude exercise extraction |
