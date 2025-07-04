# Link shortener
![Coverage](https://raw.githubusercontent.com.FruKun/link-shortener/master/coverage.svg)  
[source](https://github.com/avito-tech/auto-backend-trainee-assignment) 
## локальный запуск
### 1. создание .env файл при необходимости переопределения Config
```bash
touch .env
```
### 2. уставновка зависимостей
```bash
poetry install --no-interaction --no-cache --no-root --no-directory --without dev, postgres
```
### 3. вирутальное окружение созданное poetry
bash
```bash
eval $(poetry env activate)
```
powershell
```powershell
Invoke-Expression (poetry env activate)
```
### 4. запуск 
flask development server 
```bash
flask run --host 127.0.0.1 --port 5000
```
запуск wsgi сервера
```bash
waitress-serve --host 127.0.0.1 --port 5000 --call app:create_app
``` 
## Docker
### создание .env файла обязательно с аргументами указанными в env.example
```bash
cp env.example .env
```
### запуск контейнеров
```bash
docker compose up
```
если появляется ошибка связанная с пользователем, паролем или именем базы данных [link to issue](https://github.com/docker-library/postgres/issues/203#issuecomment-255200501)
```bash
docker compose down -v #очистится volume
```
## пример обращения к апи
```bash
curl -X POST -H "content-type: application/json" -d '{"original_url": "https://google.com", "short_url":"aboba"}' 127.0.0.1:5000/api/urls
```
powershell
```powershell
curl 127.0.0.1:5000/api/urls -Method Post -ContentType application/json -Body '{"original_url": "https://google.com", "short_url":"aboba"}'
```
## pytest local
### poetry
```bash
poetry install --no-interaction --no-cache --no-root --no-directory --with dev --without postgres
```
### pytest
```bash
pytest
```
### pytest-cov
```bash
pytest --cov-report html --cov=app # результат в html
pytest --cov=app # результат в терминал
```
