# Link shortener
[source](https://github.com/avito-tech/auto-backend-trainee-assignment)
## локальный запуск
### 1. создание .env файл при необходимости переопределения Config
```bash
touch .env
```
### 2. уставновка зависимостей
```bash
poetry install --no-interaction --no-cache --no-root --no-directory --without dev
```
### 3. вирутальное окружение созданное poetry
bash
```bash
eval $(poetry env activate)
```
windows
```powershell
Invoke-Expression (poetry env activate)
```
### 4. запуск 
1. flask development server 
```bash
flask run --host 127.0.0.1 --port 5000
```
2. запуск wsgi сервера
```bash
waitress-serve --host 127.0.0.1 --port 5000 --call app:create_app
``` 
## Docker


## pytest local
### poetry
```bash
poetry install --no-interaction --no-cache --no-root --no-directory --with dev
```
### pytest
```bash
pytest
```
### pytest-cov
```bash
pytest --cov-report html --cov=app ### результат в html
pytest --cov=app ### результат в терминал
```
