@echo off
REM Скрипт для сборки исполняемых файлов на Windows

echo ==========================================
echo   Remote Desktop - Build Script
echo ==========================================
echo.

REM Проверка установки PyInstaller
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PyInstaller не установлен!
    echo Установка PyInstaller...
    pip install pyinstaller
    echo.
)

REM Очистка старых сборок
echo Очистка старых сборок...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Выбор режима сборки
echo Выберите что собрать:
echo 1] Host (Сервер^)
echo 2] Viewer (Клиент^)
echo 3] Launcher (GUI^)
echo 4] Все приложения
echo.
set /p choice="Ваш выбор [1-4]: "

if "%choice%"=="1" (
    echo.
    echo Сборка Host...
    pyinstaller --clean host.spec
) else if "%choice%"=="2" (
    echo.
    echo Сборка Viewer...
    pyinstaller --clean viewer.spec
) else if "%choice%"=="3" (
    echo.
    echo Сборка Launcher...
    pyinstaller --clean launcher.spec
) else if "%choice%"=="4" (
    echo.
    echo Сборка всех приложений...
    echo.
    echo Сборка Host...
    pyinstaller --clean host.spec
    echo.
    echo Сборка Viewer...
    pyinstaller --clean viewer.spec
    echo.
    echo Сборка Launcher...
    pyinstaller --clean launcher.spec
) else (
    echo Неверный выбор!
    exit /b 1
)

echo.
echo ==========================================
echo Сборка завершена!
echo ==========================================
echo.
echo Исполняемые файлы находятся в папке dist\
dir /b dist
echo.
echo Для запуска:
echo   dist\RemoteDesktop-Host.exe      (Host^)
echo   dist\RemoteDesktop-Viewer.exe    (Viewer^)
echo   dist\RemoteDesktop-Launcher.exe  (Launcher^)
echo.
pause
