clear
sudo apt update -y
sudo apt upgrade -y

sudo apt install python3 python3-pip htop neofetch unzip unrar p7zip-full postgresql redis-server -y

python3 -m pip install --upgrade pip
pip3 install -U aiogram==2.25.1 tgcrypto Redis asyncpg sqlalchemy asyncio openpyxl rich simplejson uvloop