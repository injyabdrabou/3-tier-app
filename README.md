# 3-Tier Web Application with Docker Compose

A simple 3-tier web application demonstrating container orchestration with
Docker Compose. A static frontend served by Nginx fetches data from a Flask
REST API, which reads from a MySQL database. Built as a hands-on project for
the DevOps training track.

## Architecture

```
Browser
   |  http://localhost:8080
   v
[ frontend ]  Nginx - serves static HTML/JS, reverse-proxies /api/* to the backend
   |  http://backend:5000  (internal Docker network)
   v
[ backend ]   Flask REST API - business logic, reads from the database
   |  mysql://db:3306  (internal Docker network)
   v
[ db ]        MySQL 8.0 - persistent storage via named volume
```

All services share one bridge network (`app-net`) and communicate using
Compose **service names** as hostnames. Only the frontend exposes a port to
the host — the backend and database are unreachable from outside the network.

## Tech Stack

| Tier         | Technology            | Base Image           |
|--------------|-----------------------|----------------------|
| Presentation | HTML/JS + Nginx       | `nginx:alpine`       |
| Application  | Python 3.12 + Flask   | `python:3.12-slim`   |
| Data         | MySQL 8.0             | `mysql:8.0`          |

## Prerequisites

- Docker Engine 24+
- Docker Compose v2 (`docker compose version`)

## Setup & Run

```bash
# 1. Clone the repository
git clone git@github.com:injyabdrabou/3-tier-app.git
cd 3-tier-app

# 2. Create your environment file
cp .env.example .env
# edit .env and set your own passwords

# 3. Build and start the stack
docker compose up -d --build

# 4. Open the app
# http://localhost:8080
```

## Environment Variables

| Variable           | Description                          | Example    |
|--------------------|--------------------------------------|------------|
| `DB_ROOT_PASSWORD` | MySQL root password                  | (secret)   |
| `DB_NAME`          | Application database name            | `appdb`    |
| `DB_USER`          | Application database user            | `appuser`  |
| `DB_PASSWORD`      | Application database password        | (secret)   |
| `DB_HOST`          | Database hostname (service name)     | `db`       |
| `DB_PORT`          | Database port                        | `3306`     |

See `.env.example` for the template. The real `.env` is never committed.

## API Endpoints

| Method | Path        | Description                         |
|--------|-------------|-------------------------------------|
| GET    | `/health`   | Health check, returns `{status}`    |
| GET    | `/items`    | Returns all items from the database |

(Reachable from the host via the Nginx proxy: `http://localhost:8080/api/items`)

## Project Structure

```
3-tier-app/
|-- frontend/          # Nginx + static HTML/JS
|   |-- Dockerfile
|   |-- nginx.conf
|   `-- src/index.html
|-- backend/           # Flask REST API
|   |-- Dockerfile
|   |-- requirements.txt
|   `-- src/app.py
|-- db/
|   `-- init.sql       # seed script (runs on first init)
|-- docker-compose.yml
|-- .env.example
|-- .gitignore
`-- README.md
```

## Stopping & Cleaning Up

```bash
docker compose down        # stop and remove containers (data persists)
docker compose down -v     # also remove the volume (full reset, re-seeds on next up)
```

## Author

**Injy** — DevOps Training Track, 2026
