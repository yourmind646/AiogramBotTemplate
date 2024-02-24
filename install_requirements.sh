clear
sudo apt update -y
sudo apt upgrade -y

sudo apt install python3 python3-pip htop neofetch unzip unrar p7zip-full postgresql redis-server jq -y

python3 -m pip install --upgrade pip
pip3 install -U aiogram==2.25.1 tgcrypto Redis asyncpg sqlalchemy asyncio openpyxl rich simplejson uvloop

# Чтение данных из файла db_config.json
DATABASE_NAME=$(jq -r '.database' cfg/db_config.json)
USERNAME=$(jq -r '.user' cfg/db_config.json)
PASSWORD=$(jq -r '.password' cfg/db_config.json)

# Создание базы данных
sudo -u postgres psql -c "CREATE DATABASE $DATABASE_NAME;"

# Создание пользователя
sudo -u postgres psql -c "CREATE USER $USERNAME WITH PASSWORD '$PASSWORD' SUPERUSER LOGIN;"
sudo -u postgres psql -c "CREATE USER root SUPERUSER LOGIN;"
