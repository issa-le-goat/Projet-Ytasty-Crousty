FROM python:3.11-slim

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copier l'intégralité du projet (y compris src/ et pyproject.toml)
COPY . .

# Installer les dépendances et le package local
RUN uv sync --frozen --no-dev

# Exposer le port de l'application
EXPOSE 8000

# Lancer l'API avec uvicorn
CMD ["uv", "run", "uvicorn", "src.ytasty_crousty.main:app", "--host", "0.0.0.0", "--port", "8000"]