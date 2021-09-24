# API для сервиса учета продаж и покупок

<h2>Для запуска требуется</h2>
<ol>
<li>Установить зависмиости из файла 

[requirements.txt](requirements.txt)

```bash
pip install -r requirements.txt
```
</li>
<li>
Задать переменные окружения

| Название | Описание |
|:--------:|:--------:|
|HOST| Хост на который приходят запросы
|PORT| Порт хоста
|DATABASE_URL| URL подключения к базе данных (поддерживается только sqlite)
|SECRET_KEY| Секретный ключ для создания и валидации токенов
</li>

<li>
Выполнить миграции alembic

```bash
alembic upgrade head
```
</li>
<li>
Выполнить команду

```bash
PYTHONPATH=src uvicorn accounting_service.app:app --port $PORT --host $HOST
```
</li>
</ol>