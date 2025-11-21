#!/bin/bash
# Быстрая сборка всех исполняемых файлов без интерактивных запросов

echo "=========================================="
echo "  Remote Desktop - Build All"
echo "=========================================="
echo ""

# Проверка PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️  Установка PyInstaller..."
    pip install pyinstaller
fi

# Очистка
echo "🧹 Очистка..."
rm -rf build/ dist/

# Сборка
echo ""
echo "🔨 Сборка Host..."
pyinstaller --clean --onefile host.spec

echo ""
echo "🔨 Сборка Viewer..."
pyinstaller --clean --onefile viewer.spec

echo ""
echo "🔨 Сборка Launcher..."
pyinstaller --clean --onefile launcher.spec

# Результат
echo ""
echo "=========================================="
echo "✅ Готово!"
echo "=========================================="
echo ""
echo "📦 Исполняемые файлы:"
ls -lh dist/RemoteDesktop-* 2>/dev/null || ls -lh dist/

echo ""
echo "Размеры файлов:"
du -h dist/RemoteDesktop-* 2>/dev/null | awk '{print "  " $2 ": " $1}'

echo ""
