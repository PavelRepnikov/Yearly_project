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
 
 
 Этап 1.
 
 
Сбор данных из открытых источников производился парсерами из папки scrappers. Общий принцип их работы: сбор ссылок на отдельные новости путем парсинга главных страниц и по датам архивов вебсайтов, затем - извлечение информации из отдельных URLов.
 
 
Ссылки на источник данных:


https://disk.yandex.ru/d/Z9bF2McpfyzAKw - csv файл всех данных, пропарщенных папкой scrappers(3 гб)


https://disk.yandex.ru/d/x8JRQeN-_yA1cA - csv файл всех данных после EDA(2.73 гб)

https://drive.google.com/file/d/1Fd7mIda8d2KjbyBAlVn6g9HkcFvcjbSz/view?usp=drive_link - данные после обработки с определенным тэгом для статей с несколькими тэгами.


 Этап 2.

На данный момент реализованы ML решения проекта


 Этап 3.
 
Реализованы FastApi и telegram бот

Docker images:

https://hub.docker.com/r/pavelrepnikov/hw4_fastapi_app

https://hub.docker.com/r/antonai/telegram_bot

Gif работы telegram бота

![](https://github.com/PavelRepnikov/Yearly_project/blob/main/Images/gif1.gif)

Gif работы FastApi приложения

![](https://github.com/PavelRepnikov/Yearly_project/blob/main/Images/gif2.gif)
