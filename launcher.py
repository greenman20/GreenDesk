#!/usr/bin/env python3
"""
Launcher - Графический интерфейс для запуска Host или Viewer
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import socket
import threading
import config


class LauncherGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Remote Desktop - Launcher")
        self.master.geometry("500x400")
        self.master.configure(bg=config.BACKGROUND_COLOR)
        self.master.resizable(False, False)
        
        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        
        # Заголовок
        title_label = tk.Label(
            master,
            text="🖥️ Remote Desktop",
            font=("Arial", 24, "bold"),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        )
        title_label.pack(pady=20)
        
        # Фрейм для выбора режима
        mode_frame = tk.Frame(master, bg=config.BACKGROUND_COLOR)
        mode_frame.pack(pady=20)
        
        tk.Label(
            mode_frame,
            text="Выберите режим:",
            font=("Arial", 12),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack()
        
        # Кнопки выбора режима
        button_frame = tk.Frame(master, bg=config.BACKGROUND_COLOR)
        button_frame.pack(pady=10)
        
        host_btn = tk.Button(
            button_frame,
            text="🖥️ Host (Сервер)\nРазрешить удаленный доступ",
            font=("Arial", 12),
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=20,
            height=3,
            command=self.show_host_settings,
            cursor="hand2"
        )
        host_btn.grid(row=0, column=0, padx=10)
        
        viewer_btn = tk.Button(
            button_frame,
            text="👁️ Viewer (Клиент)\nПодключиться к компьютеру",
            font=("Arial", 12),
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=20,
            height=3,
            command=self.show_viewer_settings,
            cursor="hand2"
        )
        viewer_btn.grid(row=0, column=1, padx=10)
        
        # Информация о системе
        info_frame = tk.Frame(master, bg=config.BACKGROUND_COLOR)
        info_frame.pack(pady=20)
        
        local_ip = self.get_local_ip()
        tk.Label(
            info_frame,
            text=f"Ваш IP адрес: {local_ip}",
            font=("Arial", 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack()
        
        tk.Label(
            info_frame,
            text=f"Порт по умолчанию: {config.DEFAULT_PORT}",
            font=("Arial", 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack()
    
    def get_local_ip(self):
        """Получение локального IP адреса"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Не определен"
    
    def show_host_settings(self):
        """Показать настройки для Host"""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Host Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=config.BACKGROUND_COLOR)
        settings_window.resizable(False, False)
        
        tk.Label(
            settings_window,
            text="Настройки сервера (Host)",
            font=("Arial", 14, "bold"),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(pady=20)
        
        # IP адрес
        ip_frame = tk.Frame(settings_window, bg=config.BACKGROUND_COLOR)
        ip_frame.pack(pady=10)
        
        tk.Label(
            ip_frame,
            text="IP адрес:",
            font=("Arial", 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        ip_entry = tk.Entry(ip_frame, font=("Arial", 10), width=20)
        ip_entry.insert(0, config.DEFAULT_HOST)
        ip_entry.pack(side=tk.LEFT, padx=5)
        
        # Порт
        port_frame = tk.Frame(settings_window, bg=config.BACKGROUND_COLOR)
        port_frame.pack(pady=10)
        
        tk.Label(
            port_frame,
            text="Порт:",
            font=("Arial", 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        port_entry = tk.Entry(port_frame, font=("Arial", 10), width=20)
        port_entry.insert(0, str(config.DEFAULT_PORT))
        port_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопка запуска
        def start_host():
            ip = ip_entry.get()
            port = port_entry.get()
            settings_window.destroy()
            self.run_host(ip, port)
        
        start_btn = tk.Button(
            settings_window,
            text="Запустить Host",
            font=("Arial", 12),
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            command=start_host,
            cursor="hand2"
        )
        start_btn.pack(pady=20)
        
        tk.Label(
            settings_window,
            text="⚠️ Убедитесь, что порт открыт в файерволе",
            font=("Arial", 9),
            bg=config.BACKGROUND_COLOR,
            fg="yellow"
        ).pack(pady=10)
    
    def show_viewer_settings(self):
        """Показать настройки для Viewer"""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Viewer Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=config.BACKGROUND_COLOR)
        settings_window.resizable(False, False)
        
        tk.Label(
            settings_window,
            text="Настройки клиента (Viewer)",
            font=("Arial", 14, "bold"),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(pady=20)
        
        # IP адрес удаленного хоста
        ip_frame = tk.Frame(settings_window, bg=config.BACKGROUND_COLOR)
        ip_frame.pack(pady=10)
        
        tk.Label(
            ip_frame,
            text="IP адрес хоста:",
            font=("Arial", 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        ip_entry = tk.Entry(ip_frame, font=("Arial", 10), width=20)
        ip_entry.insert(0, "192.168.1.100")
        ip_entry.pack(side=tk.LEFT, padx=5)
        
        # Порт
        port_frame = tk.Frame(settings_window, bg=config.BACKGROUND_COLOR)
        port_frame.pack(pady=10)
        
        tk.Label(
            port_frame,
            text="Порт:",
            font=("Arial", 10),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        port_entry = tk.Entry(port_frame, font=("Arial", 10), width=20)
        port_entry.insert(0, str(config.DEFAULT_PORT))
        port_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопка подключения
        def connect_viewer():
            ip = ip_entry.get()
            port = port_entry.get()
            
            if not ip:
                messagebox.showerror("Ошибка", "Введите IP адрес хоста")
                return
            
            settings_window.destroy()
            self.run_viewer(ip, port)
        
        connect_btn = tk.Button(
            settings_window,
            text="Подключиться",
            font=("Arial", 12),
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            command=connect_viewer,
            cursor="hand2"
        )
        connect_btn.pack(pady=20)
    
    def run_host(self, ip, port):
        """Запуск Host в отдельном процессе"""
        try:
            subprocess.Popen(
                ["python3", "host.py"],
                stdin=subprocess.PIPE,
                text=True
            ).communicate(input=f"{ip}\n{port}\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить Host: {e}")
    
    def run_viewer(self, ip, port):
        """Запуск Viewer в отдельном процессе"""
        try:
            subprocess.Popen(
                ["python3", "viewer.py"],
                stdin=subprocess.PIPE,
                text=True
            ).communicate(input=f"{ip}\n{port}\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить Viewer: {e}")


def main():
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
