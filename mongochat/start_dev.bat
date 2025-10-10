@echo off
echo ========================================
echo    Iniciando MongoChat Development
echo ========================================
echo.

echo Iniciando servidor Django...
start "Django Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && python manage.py runserver"

echo Esperando 3 segundos...
timeout /t 3 /nobreak > nul

echo Iniciando servidor React...
start "React Server" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================
echo    Servidores iniciados correctamente
echo ========================================
echo.
echo Django: http://127.0.0.1:8000
echo React:  http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar...
pause > nul
