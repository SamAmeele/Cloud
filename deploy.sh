#!/usr/bin/env bash
# Eenvoudig deploy-script voor de Cloud-opdracht

set -e  # stop bij fout

echo "=== Cloud stack deployen ==="

# Ga naar de map waar het script zelf staat
cd "$(dirname "$0")"

echo "[0/4] Portainer-data resetten (zodat admin-wachtwoord uit docker-compose.yml geldt)..."
docker volume rm portainer_data || true

echo "[1/4] Oude stack stoppen..."
docker compose down

echo "[2/4] Nieuwe images bouwen..."
docker compose build

echo "[3/4] Stack opnieuw opstarten (detached)..."
docker compose up -d

echo "[4/4] Huidige status containers:"
docker compose ps

echo "=== Deploy klaar. ==="
