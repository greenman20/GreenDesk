#!/usr/bin/env python3
"""
Viewer (Клиент) - машина, которая просматривает удаленный рабочий стол
Получает экран и отправляет команды управления
"""

import socket
import threading
import pickle
import struct
import io
import tkinter as tk
from PIL import Image, ImageTk
import config


class RemoteDesktopViewer:
    def __init__(self, master, host, port):
        self.master = master
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
        # GUI элементы
        self.master.title(f"Remote Desktop Viewer - {host}:{port}")
        self.master.configure(bg=config.BACKGROUND_COLOR)
        
        # Фрейм для отображения экрана
        self.canvas = tk.Canvas(master, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status_label = tk.Label(
            master, 
            text="Подключение...", 
            bg=config.BACKGROUND_COLOR, 
            fg=config.TEXT_COLOR,
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Переменные для изображения
        self.current_image = None
        self.photo_image = None
        self.remote_width = 0
        self.remote_height = 0
        
        # Привязка событий мыши и клавиатуры
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_release)
        self.canvas.bind("<MouseWheel>", self.on_scroll)
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)
        
        # Фокус на canvas для получения событий клавиатуры
        self.canvas.focus_set()
        
    def connect(self):
        """Подключение к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            
            self.status_label.config(text=f"Подключено к {self.host}:{self.port}")
            
            # Запуск потока для получения экрана
            receive_thread = threading.Thread(target=self.receive_screen, daemon=True)
            receive_thread.start()
            
            return True
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка подключения: {e}")
            return False
    
    def receive_screen(self):
        """Получение экрана от сервера"""
        print("[VIEWER] Начат прием экрана")
        
        while self.running:
            try:
                # Получение размера данных
                size_data = self.socket.recv(4)
                if not size_data:
                    break
                    
                size = struct.unpack(">L", size_data)[0]
                
                # Получение данных изображения
                img_data = b""
                while len(img_data) < size:
                    chunk = self.socket.recv(min(size - len(img_data), config.BUFFER_SIZE))
                    if not chunk:
                        break
                    img_data += chunk
                
                # Декодирование и отображение
                image = Image.open(io.BytesIO(img_data))
                self.display_image(image)
                
            except (ConnectionResetError, BrokenPipeError):
                print("[VIEWER] Соединение разорвано")
                self.running = False
                break
            except Exception as e:
                print(f"[VIEWER] Ошибка при получении экрана: {e}")
                break
        
        self.master.after(0, lambda: self.status_label.config(text="Отключено"))
    
    def display_image(self, image):
        """Отображение изображения на canvas"""
        try:
            self.remote_width, self.remote_height = image.size
            
            # Масштабирование под размер окна
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Вычисление коэффициента масштабирования
                scale_w = canvas_width / self.remote_width
                scale_h = canvas_height / self.remote_height
                scale = min(scale_w, scale_h)
                
                new_width = int(self.remote_width * scale)
                new_height = int(self.remote_height * scale)
                
                image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Конвертация для Tkinter
            self.photo_image = ImageTk.PhotoImage(image)
            
            # Отображение на canvas
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2, 
                canvas_height // 2, 
                image=self.photo_image, 
                anchor=tk.CENTER
            )
            
        except Exception as e:
            print(f"[VIEWER] Ошибка отображения: {e}")
    
    def send_command(self, command):
        """Отправка команды на сервер"""
        try:
            if self.socket and self.running:
                data = pickle.dumps(command)
                size = len(data)
                self.socket.sendall(struct.pack(">L", size))
                self.socket.sendall(data)
        except Exception as e:
            print(f"[VIEWER] Ошибка отправки команды: {e}")
    
    def get_remote_coords(self, canvas_x, canvas_y):
        """Преобразование координат canvas в координаты удаленного экрана"""
        if self.remote_width == 0 or self.remote_height == 0:
            return None, None
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Вычисление смещения и масштаба
        scale_w = canvas_width / self.remote_width
        scale_h = canvas_height / self.remote_height
        scale = min(scale_w, scale_h)
        
        scaled_width = int(self.remote_width * scale)
        scaled_height = int(self.remote_height * scale)
        
        offset_x = (canvas_width - scaled_width) // 2
        offset_y = (canvas_height - scaled_height) // 2
        
        # Преобразование координат
        remote_x = int((canvas_x - offset_x) / scale)
        remote_y = int((canvas_y - offset_y) / scale)
        
        # Ограничение координат
        remote_x = max(0, min(remote_x, self.remote_width - 1))
        remote_y = max(0, min(remote_y, self.remote_height - 1))
        
        return remote_x, remote_y
    
    # Обработчики событий мыши
    def on_mouse_move(self, event):
        x, y = self.get_remote_coords(event.x, event.y)
        if x is not None:
            self.send_command({'type': 'mouse_move', 'x': x, 'y': y})
    
    def on_left_click(self, event):
        x, y = self.get_remote_coords(event.x, event.y)
        if x is not None:
            self.send_command({'type': 'mouse_click', 'button': 'left', 'pressed': True})
    
    def on_left_release(self, event):
        self.send_command({'type': 'mouse_click', 'button': 'left', 'pressed': False})
    
    def on_right_click(self, event):
        x, y = self.get_remote_coords(event.x, event.y)
        if x is not None:
            self.send_command({'type': 'mouse_click', 'button': 'right', 'pressed': True})
    
    def on_right_release(self, event):
        self.send_command({'type': 'mouse_click', 'button': 'right', 'pressed': False})
    
    def on_scroll(self, event):
        delta = event.delta // 120  # Windows
        self.send_command({'type': 'mouse_scroll', 'dx': 0, 'dy': delta})
    
    # Обработчики событий клавиатуры
    def on_key_press(self, event):
        key = event.keysym
        self.send_command({'type': 'key_press', 'key': key})
    
    def on_key_release(self, event):
        key = event.keysym
        self.send_command({'type': 'key_release', 'key': key})
    
    def disconnect(self):
        """Отключение от сервера"""
        print("[VIEWER] Отключение...")
        self.running = False
        if self.socket:
            self.socket.close()


def main():
    print("=" * 50)
    print("Remote Desktop Viewer (Клиент)")
    print("=" * 50)
    
    host = input("Введите IP адрес сервера: ").strip()
    port_input = input(f"Введите порт (по умолчанию {config.DEFAULT_PORT}): ").strip()
    port = int(port_input) if port_input else config.DEFAULT_PORT
    
    root = tk.Tk()
    root.geometry("1024x768")
    
    viewer = RemoteDesktopViewer(root, host, port)
    
    if viewer.connect():
        try:
            root.protocol("WM_DELETE_WINDOW", lambda: [viewer.disconnect(), root.destroy()])
            root.mainloop()
        except KeyboardInterrupt:
            viewer.disconnect()
    else:
        print("Не удалось подключиться к серверу")


if __name__ == "__main__":
    main()
