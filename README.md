# Анализ новостных данных

**Команда:**

| Фамилия и Имя| Телеграмм |
|----------|----------|
| Громов Артем  | @artyom_grom |
| Новоженина Надежда   | @ne_obijaysya |
| Репников Павел | @Pavel_Repnikov  |
| Иванов Антон | @Anton-A-I  |

 Этапы проекта:
 
 1)Сбор данных из открытых источников
 
 2)Решить, какие задачи будем решать и реализовать их
 
 3)Реализация веб сервиса (Web UI либо Telegram бот)
 
 
 # Этап 1.
 
 
Сбор данных из открытых источников производился парсерами из папки scrappers. Общий принцип их работы: сбор ссылок на отдельные новости путем парсинга главных страниц и по датам архивов вебсайтов, затем - извлечение информации из отдельных URLов.
 
 
Ссылки на источник данных:


https://disk.yandex.ru/d/Z9bF2McpfyzAKw - csv файл всех данных, пропарщенных папкой scrappers(3 гб)


https://disk.yandex.ru/d/x8JRQeN-_yA1cA - csv файл всех данных после EDA(2.73 гб)

https://drive.google.com/file/d/1Fd7mIda8d2KjbyBAlVn6g9HkcFvcjbSz/view?usp=drive_link - данные после обработки с определенным тэгом для статей с несколькими тэгами.


 # Этап 2.

На данный момент реализованы ML решения проекта


 # Этап 3.
 
Реализованы FastApi и telegram бот

Docker images:

https://hub.docker.com/r/pavelrepnikov/hw4_fastapi_app

Инструкция, для использования docker образа hw4_fastapi_app

1. Для загрузки Docker-образа с Docker Hub выполните следующую команду:

   
docker pull pavelrepnikov/hw4_fastapi_app

Эта команда загрузит образ pavelrepnikov/hw4_fastapi_app с Docker Hub на
ваш компьютер.

2. Чтобы запустить контейнер на основе загруженного образа, выполните
следующую команду:

docker run -p 8000:8000 pavelrepnikov/hw4_fastapi_app:1.0

3. Чтобы получить доступ к API сервиса, зайдите на http://localhost:8000/docs

https://hub.docker.com/r/antonai/telegram_bot

Инструкция, для использования docker образа telegram_bot

1. Для загрузки Docker-образа с Docker Hub выполните следующую команду:
docker pull antonai/telegram_bot:tg_bot_1

Эта команда загрузит образ antonai/telegram_bot с тегом tg_bot_1 с Docker Hub на
ваш компьютер.

2. Чтобы запустить контейнер на основе загруженного образа, выполните
следующую команду:

docker run -p 8080:80 antonai/telegram_bot:tg_bot_1

3. Чтобы получить доступ к телеграм боту, зайдите на https://t.me/news_data_analysis_bot



Видео работы telegram бота



https://github.com/PavelRepnikov/Yearly_project/assets/148060631/0daa4404-5380-40f2-bb85-65707d3c1bec



Видео работы FastApi приложения



https://github.com/PavelRepnikov/Yearly_project/assets/148060631/4c6839c6-c65e-498f-846d-614278ad010f


