clear
sudo apt update -y
sudo apt upgrade -y

sudo apt install python3 python3-pip htop neofetch unzip unrar p7zip-full postgresql redis-server -y

python3 -m pip install --upgrade pip
pip3 install -U aiogram pyrogram tgcrypto Redis asyncpg sqlalchemy asyncio openpyxl click rich simplejson telethon opentele python-socks[asyncio]