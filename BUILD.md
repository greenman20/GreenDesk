# 🔨 Инструкция по сборке исполняемых файлов

Эта инструкция описывает, как собрать standalone исполняемые файлы из Python кода.

## 📋 Требования для сборки

### Linux/macOS
```bash
pip install pyinstaller
```

### Windows
```bash
pip install pyinstaller
```

### Дополнительные зависимости
Убедитесь, что установлены все зависимости:
```bash
pip install -r requirements.txt
```

---

## 🚀 Быстрая сборка

### Способ 1: Автоматическая сборка всех приложений

**Linux/macOS:**
```bash
./build_all.sh
```

**Windows:**
```bash
build.bat
# Выберите опцию "4" для сборки всех приложений
```

### Способ 2: Интерактивная сборка

**Linux/macOS:**
```bash
./build.sh
```

**Windows:**
```bash
build.bat
```

Выберите что собрать:
- `1` - Host (Сервер)
- `2` - Viewer (Клиент)  
- `3` - Launcher (GUI)
- `4` - Все приложения

---

## 🔧 Ручная сборка через PyInstaller

### Сборка Host
```bash
pyinstaller --clean host.spec
```

### Сборка Viewer
```bash
pyinstaller --clean viewer.spec
```

### Сборка Launcher
```bash
pyinstaller --clean launcher.spec
```

### Сборка с дополнительными опциями

**Один файл (onefile mode):**
```bash
pyinstaller --clean --onefile host.spec
```

**Без консольного окна (только для GUI):**
```bash
pyinstaller --clean --noconsole launcher.spec
```

**С иконкой (если есть icon.ico):**
```bash
pyinstaller --clean --icon=icon.ico host.spec
```

---

## 📦 Результаты сборки

После успешной сборки файлы появятся в папке `dist/`:

```
dist/
├── RemoteDesktop-Host         (или .exe на Windows)
├── RemoteDesktop-Viewer       (или .exe на Windows)
└── RemoteDesktop-Launcher     (или .exe на Windows)
```

### Проверка сборки

**Linux/macOS:**
```bash
ls -lh dist/
./dist/RemoteDesktop-Launcher
```

**Windows:**
```bash
dir dist
dist\RemoteDesktop-Launcher.exe
```

---

## 📏 Размеры исполняемых файлов

Примерные размеры (зависят от платформы и режима сборки):

| Файл | Onefile mode | Onedir mode |
|------|--------------|-------------|
| Host | ~80-120 MB | ~100-150 MB |
| Viewer | ~80-120 MB | ~100-150 MB |
| Launcher | ~80-120 MB | ~100-150 MB |

### Оптимизация размера

Для уменьшения размера можно:

1. **Использовать UPX компрессию** (уже включена в spec файлах):
```bash
pyinstaller --clean --upx-dir=/path/to/upx host.spec
```

2. **Исключить ненужные модули**:
Отредактируйте `.spec` файл и добавьте в `excludes`:
```python
excludes=['matplotlib', 'scipy', 'pandas', 'tests']
```

3. **Собрать в onefile mode** (медленнее запуск, но один файл):
```bash
pyinstaller --clean --onefile host.spec
```

---

## 🔍 Решение проблем

### Ошибка "Failed to execute script"

**Решение**: Запустите с консолью для просмотра ошибок:
```bash
# В .spec файле измените:
console=True  # вместо console=False
```

### Ошибка "No module named 'PIL._tkinter_finder'"

**Решение**: Убедитесь, что в hiddenimports добавлено:
```python
hiddenimports=['PIL._tkinter_finder', 'PIL.Image', 'PIL.ImageTk']
```

### Ошибка на Linux: "cannot open display"

**Решение**: Убедитесь, что DISPLAY переменная установлена:
```bash
echo $DISPLAY
export DISPLAY=:0
```

### Большой размер исполняемого файла

**Решение**: 
1. Используйте виртуальное окружение с минимальными зависимостями
2. Включите UPX компрессию
3. Исключите ненужные модули в .spec файле

### Долгий запуск исполняемого файла

**Решение**: Это нормально для onefile режима. PyInstaller распаковывает файлы во временную папку. Используйте onedir режим для быстрого запуска:
```bash
pyinstaller --clean --onedir host.spec
```

### Антивирус блокирует исполняемый файл

**Решение**:
1. Добавьте файл в исключения антивируса
2. Подпишите исполняемый файл цифровой подписью (для production)
3. Отправьте на VirusTotal для проверки ложных срабатываний

---

## 🌐 Кросс-платформенная сборка

⚠️ **Важно**: PyInstaller НЕ поддерживает кросс-компиляцию!

Для сборки на разных платформах нужно:
- **Windows** → Собирать на Windows
- **macOS** → Собирать на macOS  
- **Linux** → Собирать на Linux

### Сборка для всех платформ

Используйте виртуальные машины или CI/CD:

```yaml
# Пример GitHub Actions
name: Build
on: [push]
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: ./build_all.sh  # или build.bat на Windows
      - uses: actions/upload-artifact@v2
        with:
          name: RemoteDesktop-${{ matrix.os }}
          path: dist/
```

---

## 📤 Распространение

### Linux
```bash
# Создать tar.gz архив
tar -czf RemoteDesktop-Linux.tar.gz dist/

# Или создать .deb пакет
# Используйте fpm или создайте debian/ структуру
```

### Windows
```bash
# Создать ZIP архив
# Или использовать Inno Setup для создания инсталлятора
```

### macOS
```bash
# Создать .dmg образ
# Используйте create-dmg или hdiutil
```

---

## 🔐 Безопасность

### Для production сборки рекомендуется:

1. **Подписать исполняемые файлы**:
   - Windows: signtool
   - macOS: codesign
   - Linux: gpg

2. **Обфускация кода** (опционально):
```bash
pip install pyarmor
pyarmor obfuscate host.py
```

3. **Включить проверку целостности**:
В .spec файле:
```python
exe = EXE(
    ...,
    runtime_tmpdir=None,
    console=True,
    strip=True,  # Убрать debug символы
    upx=True,    # Сжатие
)
```

---

## 📊 Тестирование сборки

После сборки протестируйте:

```bash
# 1. Проверка запуска
./dist/RemoteDesktop-Host --help

# 2. Проверка зависимостей (Linux)
ldd dist/RemoteDesktop-Host

# 3. Проверка размера
du -h dist/RemoteDesktop-*

# 4. Функциональное тестирование
# Запустите Host и Viewer, проверьте подключение
```

---

## 📝 Чек-лист перед релизом

- [ ] Все зависимости установлены
- [ ] Сборка успешна на всех целевых платформах
- [ ] Исполняемые файлы запускаются без ошибок
- [ ] Функционал работает (Host, Viewer, Launcher)
- [ ] Размер файлов приемлем
- [ ] README.md обновлен с инструкциями по использованию
- [ ] Файлы подписаны (для production)
- [ ] Создан инсталлятор (опционально)
- [ ] Проведено тестирование на чистой системе

---

## 🆘 Поддержка

При проблемах со сборкой:

1. Проверьте версию PyInstaller: `pyinstaller --version`
2. Обновите PyInstaller: `pip install --upgrade pyinstaller`
3. Проверьте логи в `build/` папке
4. Запустите с флагом `--debug all` для подробных логов
5. Проверьте [PyInstaller FAQ](https://pyinstaller.org/en/stable/common-problems-and-solutions.html)

---

**Успешной сборки! 🎉**
