#!/bin/bash
# Скрипт для сборки исполняемых файлов

echo "=========================================="
echo "  Remote Desktop - Build Script"
echo "=========================================="
echo ""

# Проверка установки PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️  PyInstaller не установлен!"
    echo "Установка PyInstaller..."
    pip install pyinstaller
    echo ""
fi

# Очистка старых сборок
echo "🧹 Очистка старых сборок..."
rm -rf build/ dist/ *.spec.bak
echo ""

# Выбор режима сборки
echo "Выберите что собрать:"
echo "1) Host (Сервер)"
echo "2) Viewer (Клиент)"
echo "3) Launcher (GUI)"
echo "4) Все приложения"
echo ""
read -p "Ваш выбор [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "🔨 Сборка Host..."
        pyinstaller --clean host.spec
        ;;
    2)
        echo ""
        echo "🔨 Сборка Viewer..."
        pyinstaller --clean viewer.spec
        ;;
    3)
        echo ""
        echo "🔨 Сборка Launcher..."
        pyinstaller --clean launcher.spec
        ;;
    4)
        echo ""
        echo "🔨 Сборка всех приложений..."
        echo ""
        echo "Сборка Host..."
        pyinstaller --clean host.spec
        echo ""
        echo "Сборка Viewer..."
        pyinstaller --clean viewer.spec
        echo ""
        echo "Сборка Launcher..."
        pyinstaller --clean launcher.spec
        ;;
    *)
        echo "❌ Неверный выбор!"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "✅ Сборка завершена!"
echo "=========================================="
echo ""
echo "Исполняемые файлы находятся в папке dist/"
ls -lh dist/
echo ""
echo "Для запуска:"
echo "  ./dist/RemoteDesktop-Host      (Host)"
echo "  ./dist/RemoteDesktop-Viewer    (Viewer)"
echo "  ./dist/RemoteDesktop-Launcher  (Launcher)"
echo ""
