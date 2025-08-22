
@echo off
echo ========================================
echo TaskFlow AI - Script de Instalacion
echo ========================================
echo.

echo [1/6] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo [2/6] Actualizando pip...
python -m pip install --upgrade pip

echo [3/6] Instalando dependencias...
pip install -r requirements.txt

echo [4/6] Instalando TaskFlow AI en modo desarrollo...
pip install -e .

echo [5/6] Creando archivo de configuracion...
if not exist .env (
    copy .env.example .env
    echo Archivo .env creado. Por favor editalo con tus tokens.
) else (
    echo Archivo .env ya existe.
)

echo [6/6] Verificando instalacion...
taskflow --help
if %errorlevel% neq 0 (
    echo ERROR: TaskFlow no se instalo correctamente
    pause
    exit /b 1
)

echo.
echo ========================================
echo INSTALACION COMPLETADA EXITOSAMENTE!
echo ========================================
echo.
echo Proximos pasos:
echo 1. Edita el archivo .env con tus tokens
echo 2. Ejecuta: taskflow ask "crear mi primera tarea"
echo.
echo Para ejecutar tests:
echo pytest --cov=src/taskflow --cov-report=html
echo.