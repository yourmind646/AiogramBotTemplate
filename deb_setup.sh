#!/bin/bash

echo "🔄 Загрузка пакетов..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install docker docker.io docker-compose-v2

echo "🚀 Запуск Docker Compose..."
docker compose up -d --build

echo "⏳ Ожидание запуска сервисов..."
sleep 5  # Даем контейнерам немного времени

echo "✅ Контейнеры, которые сейчас работают:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

sleep 3  # Даем контейнерам немного времени

echo "📜 Логи Postgres:"
docker logs plania_postgredb --tail 10

echo "📜 Логи Redis:"
docker logs plania_redis --tail 10

echo "📜 Логи бота:"
docker logs plania_bot --tail 10

echo "🎯 Развертывание завершено!"
