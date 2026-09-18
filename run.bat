@echo off
REM Double-click to run the store. Uses venv + PostgreSQL (.env).
cd /d "%~dp0"
call venv\Scripts\activate
python manage.py migrate
start http://127.0.0.1:8000/
python manage.py runserver
pause
