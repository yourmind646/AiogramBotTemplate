#!/bin/bash

# INIT
DB_NAME=""
BASE_PATH=""

# Директория для хранения резервных копий относительно текущей директории
BACKUP_DIR="${BASE_PATH}/backups"
mkdir -p "$BACKUP_DIR"

# Текущая дата для имен файлов
DATE=$(date +%Y-%m-%d)

# Резервная копия PostgreSQL
echo "Создаём резервную копию PostgreSQL..."
docker exec postgredb pg_dump -Fc -U ruby -d $DB_NAME > "$BACKUP_DIR/pg_${DB_NAME}_backup_${DATE}.sql"
if [ $? -eq 0 ]; then
    echo "PostgreSQL backup успешно создан: $BACKUP_DIR/pg_${DB_NAME}_backup_${DATE}.sql"
else
    echo "Ошибка при создании backup PostgreSQL" >&2
fi

# Резервная копия Redis
echo "Сохраняем дамп Redis..."
docker exec plania_redis redis-cli SAVE

# Копируем файл дампа (обычно он располагается в /data/dump.rdb)
docker cp plania_redis:/data/dump.rdb "$BACKUP_DIR/redis_dump_${DATE}.rdb"
if [ $? -eq 0 ]; then
    echo "Redis backup успешно создан: $BACKUP_DIR/redis_dump_${DATE}.rdb"
else
    echo "Ошибка при создании backup Redis" >&2
fi

# crontab: 0 0 * * 1 ${BASE_PATH}/backuper.sh >> /var/log/docker_backuper.log 2>&1