#!/usr/bin/env python3
"""
Host (Сервер) - машина, к которой подключаются
Захватывает экран и принимает команды удаленного управления
"""

import socket
import threading
import pickle
import struct
import time
import io
from PIL import ImageGrab
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import config


class RemoteDesktopHost:
    def __init__(self, host=config.DEFAULT_HOST, port=config.DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        
    def start(self):
        """Запуск сервера"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"[HOST] Сервер запущен на {self.host}:{self.port}")
        print("[HOST] Ожидание подключения...")
        
        try:
            self.client_socket, addr = self.server_socket.accept()
            print(f"[HOST] Клиент подключен: {addr}")
            
            # Запуск потоков для передачи экрана и приема команд
            screen_thread = threading.Thread(target=self.send_screen, daemon=True)
            command_thread = threading.Thread(target=self.receive_commands, daemon=True)
            
            screen_thread.start()
            command_thread.start()
            
            # Ожидание завершения
            screen_thread.join()
            command_thread.join()
            
        except Exception as e:
            print(f"[HOST] Ошибка: {e}")
        finally:
            self.stop()
    
    def send_screen(self):
        """Захват и отправка экрана клиенту"""
        print("[HOST] Начата передача экрана")
        
        while self.running:
            try:
                # Захват экрана
                screenshot = ImageGrab.grab()
                
                # Масштабирование если нужно
                if config.SCREEN_SCALE != 1.0:
                    new_size = (
                        int(screenshot.width * config.SCREEN_SCALE),
                        int(screenshot.height * config.SCREEN_SCALE)
                    )
                    screenshot = screenshot.resize(new_size)
                
                # Конвертация в JPEG для сжатия
                buffer = io.BytesIO()
                screenshot.save(buffer, format='JPEG', quality=config.SCREEN_QUALITY)
                img_data = buffer.getvalue()
                
                # Отправка размера данных и самих данных
                size = len(img_data)
                self.client_socket.sendall(struct.pack(">L", size))
                self.client_socket.sendall(img_data)
                
                # Контроль FPS
                time.sleep(1.0 / config.FPS)
                
            except (ConnectionResetError, BrokenPipeError):
                print("[HOST] Клиент отключился")
                self.running = False
                break
            except Exception as e:
                print(f"[HOST] Ошибка при отправке экрана: {e}")
                break
    
    def receive_commands(self):
        """Прием и выполнение команд от клиента"""
        print("[HOST] Начат прием команд")
        
        while self.running:
            try:
                # Получение размера команды
                size_data = self.client_socket.recv(4)
                if not size_data:
                    break
                    
                size = struct.unpack(">L", size_data)[0]
                
                # Получение команды
                command_data = b""
                while len(command_data) < size:
                    chunk = self.client_socket.recv(min(size - len(command_data), config.BUFFER_SIZE))
                    if not chunk:
                        break
                    command_data += chunk
                
                command = pickle.loads(command_data)
                self.execute_command(command)
                
            except (ConnectionResetError, BrokenPipeError):
                print("[HOST] Клиент отключился")
                self.running = False
                break
            except Exception as e:
                print(f"[HOST] Ошибка при приеме команд: {e}")
                break
    
    def execute_command(self, command):
        """Выполнение команды управления"""
        try:
            cmd_type = command.get('type')
            
            if cmd_type == 'mouse_move':
                x, y = command['x'], command['y']
                self.mouse.position = (x, y)
                
            elif cmd_type == 'mouse_click':
                button = Button.left if command['button'] == 'left' else Button.right
                if command['pressed']:
                    self.mouse.press(button)
                else:
                    self.mouse.release(button)
                    
            elif cmd_type == 'mouse_scroll':
                self.mouse.scroll(command['dx'], command['dy'])
                
            elif cmd_type == 'key_press':
                key = command['key']
                try:
                    # Попытка преобразовать в специальную клавишу
                    if hasattr(Key, key):
                        self.keyboard.press(getattr(Key, key))
                    else:
                        self.keyboard.press(key)
                except:
                    pass
                    
            elif cmd_type == 'key_release':
                key = command['key']
                try:
                    if hasattr(Key, key):
                        self.keyboard.release(getattr(Key, key))
                    else:
                        self.keyboard.release(key)
                except:
                    pass
                    
        except Exception as e:
            print(f"[HOST] Ошибка выполнения команды: {e}")
    
    def stop(self):
        """Остановка сервера"""
        print("[HOST] Остановка сервера...")
        self.running = False
        
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()


def main():
    print("=" * 50)
    print("Remote Desktop Host (Сервер)")
    print("=" * 50)
    
    host_ip = input(f"Введите IP адрес для прослушивания (по умолчанию {config.DEFAULT_HOST}): ").strip()
    if not host_ip:
        host_ip = config.DEFAULT_HOST
    
    port_input = input(f"Введите порт (по умолчанию {config.DEFAULT_PORT}): ").strip()
    port = int(port_input) if port_input else config.DEFAULT_PORT
    
    host = RemoteDesktopHost(host_ip, port)
    
    try:
        host.start()
    except KeyboardInterrupt:
        print("\n[HOST] Прерывание пользователем")
        host.stop()


if __name__ == "__main__":
    main()
