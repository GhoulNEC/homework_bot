# home_work bot
***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Описание</summary>

Телеграм-бот, который с периодичностью в 10 минут обращается к API сервиса Яндекс.Домашка и проверяет статус отправленной на ревью домашней работы. 
При обновлении статуса анализирует ответ API и отправляет соответствующее сообщение в Telegram. 
Логирует свою работу и отправляет соответствующие уведомления в Telegram.
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Технологии</summary>

* Python 3.8.9
* python-telegram-bot 13.7

С полным списком технологий можно ознакомиться в файле ```requirements.txt```
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Запуск проекта</summary>

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/GhoulNEC/homework_bot.git
```

```
cd homework_bot
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать и заполнить файл ```.env``` по шаблону:
```
PRACTICUM_TOKEN={practicum_token}
TG_TOKEN={telegram_token}
TG_CHAT_ID={chat_id}
```

Запустить проект:

```
python3 homework.py
```
</details>

***
<details>
    <summary style="font-size: 16pt; font-weight: bold">Автор</summary>

[Роман Евстафьев](https://github.com/GhoulNEC)
</details>

***