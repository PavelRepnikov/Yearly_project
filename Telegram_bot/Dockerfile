# Используйте базовый образ. Например, образ Ubuntu.
FROM python:3.10-slim-bullseye
WORKDIR Telegram_bot
RUN apt-get update && apt-get install 
#-y --no-install-recomends libgomp1 sudo
#RUN sudo rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
