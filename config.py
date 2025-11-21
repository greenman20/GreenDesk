"""
Конфигурация для приложения удаленного доступа
"""

# Сетевые настройки
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 5555
BUFFER_SIZE = 65536

# Настройки качества изображения
SCREEN_QUALITY = 70  # Качество JPEG сжатия (0-100)
SCREEN_SCALE = 1.0   # Масштаб экрана (0.5 = 50%, 1.0 = 100%)
FPS = 30             # Целевой FPS для передачи экрана

# Настройки безопасности
USE_ENCRYPTION = True
CONNECTION_PASSWORD = "change_this_password"  # Изменить в production!

# Цвета для GUI
BACKGROUND_COLOR = "#1e1e1e"
BUTTON_COLOR = "#0078d4"
TEXT_COLOR = "#ffffff"
