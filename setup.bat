@echo off
REM ============================================================
REM  E-Shop - COMPLETE SETUP for Windows
REM  Double-click this file on any new machine and it will:
REM   1. Check Python
REM   2. Create virtual environment venv
REM   3. Install all requirements
REM   4. Create .env config file
REM   5. Connect PostgreSQL, or fall back to SQLite
REM   6. Migrate database + load demo data
REM   7. Optionally create admin account
REM   8. Start the server
REM  NOTE for editors: never put ( ) inside an IF block below,
REM  it breaks Windows batch parsing.
REM ============================================================
title E-Shop Complete Setup
cd /d "%~dp0"

echo ============================================
echo   E-Shop - Complete Setup
echo ============================================
echo.

REM ---- STEP 1 - Check Python ----
where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set PY=python
  ) else (
    echo [ERROR] Python is NOT installed!
    echo         Download it from: https://www.python.org/downloads/
    echo         IMPORTANT: tick Add python.exe to PATH during install,
    echo         then close this window and run setup again.
    pause
    exit /b 1
  )
)
echo [1/7] Python found:
%PY% --version
echo.

REM ---- STEP 2 - Virtual environment ----
if not exist "venv\Scripts\python.exe" (
  echo [2/7] Creating virtual environment - first run only, may take a minute...
  %PY% -m venv venv
  if %errorlevel% neq 0 (
    echo [ERROR] Could not create venv.
    pause
    exit /b 1
  )
) else (
  echo [2/7] Virtual environment already exists - skipping.
)
call "venv\Scripts\activate"
echo.

REM ---- STEP 3 - Install requirements ----
echo [3/7] Installing libraries - first run only, may take a few minutes...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
  echo [ERROR] pip install failed. Check your internet connection and try again.
  pause
  exit /b 1
)
echo.

REM ---- STEP 4 - Config file ----
if not exist ".env" (
  echo [4/7] Creating .env config file...
  copy ".env.example" ".env" >nul
  echo       Created .env - if your PostgreSQL password is NOT postgres,
  echo       open .env in Notepad and fix DB_PASSWORD, then run setup again.
) else (
  echo [4/7] .env already exists - skipping.
)
echo.

REM ---- STEP 5 - Database ----
echo [5/7] Applying migrations - trying PostgreSQL first...
python manage.py migrate
if %errorlevel% neq 0 (
  echo.
  echo PostgreSQL is not reachable. Switching to temporary SQLite mode
  echo so you can run immediately - change back to postgresql in .env anytime.
  powershell -Command "(Get-Content .env) -replace '^DB_ENGINE=.*','DB_ENGINE=sqlite' | Set-Content .env"
  python manage.py migrate
  if %errorlevel% neq 0 (
    echo [ERROR] Migration failed even on SQLite. Read the error above.
    pause
    exit /b 1
  )
)
echo       Database ready.
echo.

REM ---- STEP 6 - Demo data ----
echo [6/7] Loading demo categories and products...
python manage.py seed
echo.

REM ---- STEP 7 - Admin account, optional ----
set /p CREATE_SUPER="Create admin account now? Y/N, default N: "
if /i "%CREATE_SUPER%"=="Y" (
  python manage.py createsuperuser
  echo.
) else (
  echo Skipped. Demo login is admin@test.com / admin12345
  echo.
)

echo ============================================
echo   Setup complete! Starting the server...
echo   Store: http://127.0.0.1:8000/
echo   Admin: http://127.0.0.1:8000/admin/
echo   Keep this window open. Press CTRL+C to stop.
echo ============================================
start http://127.0.0.1:8000/
python manage.py runserver
pause
