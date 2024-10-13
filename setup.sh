clear
sudo apt update -y
sudo apt upgrade -y

sudo apt install python3 python3-pip htop neofetch unzip p7zip-full postgresql redis-server jq -y

python3 -m pip install --upgrade pip
pip3 install -U aiogram tgcrypto Redis asyncpg sqlalchemy asyncio openpyxl rich simplejson uvloop python-decouple apscheduler requests dotenv-cli

# Загрузка данных из .env файла
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs) # Загружаем переменные из .env
else
  echo ".env файл не найден!"
  exit 1
fi

# Убедиться, что все значения из .env были загружены
if [ -z "$DB_NAME" ] || [ -z "$DB_USERNAME" ] || [ -z "$DB_PASSWORD" ]; then
  echo "Одно или несколько значений из .env не были загружены. Пожалуйста проверьте .env файл."
  exit 1
fi

# Создание базы данных
sudo -u postgres psql -c "CREATE DATABASE \"$DB_NAME\";" || { echo "Ошибка при создании базы данных"; exit 1; }

# Создание пользователя с параметрами
sudo -u postgres psql -c "CREATE USER \"$DB_USERNAME\" WITH PASSWORD '$DB_PASSWORD';" || { echo "Ошибка при создании пользователя"; exit 1; }

# Наделение пользователя необходимыми привилегиями
sudo -u postgres psql -c "ALTER USER \"$DB_USERNAME\" WITH SUPERUSER LOGIN;" || { echo "Ошибка при изменении привилегий пользователя"; exit 1; }

# Создание пользователя с параметрами
sudo -u postgres psql -c "CREATE USER root SUPERUSER LOGIN;" || { echo "Ошибка при создании пользователя"; exit 1; }