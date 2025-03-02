"""
Лаунчер Проектов по Компьютерной Графике с OpenGL

Простой графический интерфейс для запуска всех бинарных приложений.
Автор: Царюк Артём Владимирович
"""

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class ApplicationLauncher:
    def __init__(self, root):
        """
        Инициализация лаунчера приложений
        
        Args:
            root: Корневой элемент Tkinter
        """
        self.root = root
        self.root.title("Проекты по Компьютерной Графике с OpenGL")
        self.root.geometry("900x650")
        self.root.configure(bg="#333333")
        
        # Настройка стилей
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#333333')
        self.style.configure('TButton', 
                          background='#555555', 
                          foreground='white', 
                          padding=10, 
                          font=('Arial', 12))
        self.style.configure('TLabel', 
                          background='#333333', 
                          foreground='white', 
                          font=('Arial', 14))
        
        # Создание основного фрейма
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        header_label = ttk.Label(self.main_frame, 
                               text="Проекты по Компьютерной Графике с OpenGL", 
                               font=('Arial', 22, 'bold'))
        header_label.pack(pady=(0, 20))
        
        # Описание
        desc_label = ttk.Label(self.main_frame, 
                             text="Выберите проект для запуска:", 
                             font=('Arial', 16))
        desc_label.pack(pady=(0, 20))
        
        # Создание прокручиваемого фрейма для кнопок
        self.canvas = tk.Canvas(self.main_frame, bg="#333333", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Получение списка бинарных файлов
        self.load_binaries()
        
        # Добавление информации внизу
        footer_frame = ttk.Frame(root)
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        author_label = ttk.Label(footer_frame, 
                                text="Автор: Царюк Артём Владимирович", 
                                font=('Arial', 10))
        author_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(footer_frame, 
                                 text="Версия 1.0", 
                                 font=('Arial', 10))
        version_label.pack(side=tk.RIGHT)

    def load_binaries(self):
        """
        Загрузка бинарных файлов из директории binaries 
        и создание элементов управления для их запуска
        """
        binaries_dir = "binaries"
        if not os.path.exists(binaries_dir):
            messagebox.showerror("Ошибка", f"Директория '{binaries_dir}' не найдена!")
            return
            
        binaries = [f for f in os.listdir(binaries_dir) if f.endswith('.exe')]
        binaries.sort()
        
        if not binaries:
            messagebox.showinfo("Информация", "Бинарные файлы не найдены!")
            return
            
        # Словарь описаний проектов
        descriptions = {
            "project1_bin.exe": "Платоновы тела (Куб, Тетраэдр, Октаэдр)",
            "project2_bin.exe": "Платоновы тела (Икосаэдр и Додекаэдр)",
            "project3_bin.exe": "Алгоритмы построения линий",
            "project4_bin.exe": "Алгоритмы построения окружностей",
            "project5_bin.exe": "Отсечение линий",
            "project6_bin.exe": "Алгоритм отсечения Кируса-Бека",
            "project7_bin.exe": "Расширенный алгоритм Кируса-Бека",
            "project8_bin.exe": "Алгоритм Сазерленда-Ходжмена",
            "project9_bin.exe": "Отсечение цилиндром",
            "project10_bin.exe": "Алгоритм отсечения Вейлера-Азертона",
            "project11_bin.exe": "Исследование цветовых систем",
            "project12_bin.exe": "Дизеринг изображений",
            "project13_bin.exe": "Неизвестный проект",
            "project14_bin.exe": "Растеризация эллипса",
        }
            
        # Создание фрейма для каждого бинарного файла с кнопкой и описанием
        for binary in binaries:
            if binary == "README.txt":
                continue
                
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=5)
            
            # Получение номера проекта из имени файла
            project_num = binary.split('_')[0].replace('project', '')
            
            # Создание кнопки с номером проекта
            button = ttk.Button(
                frame, 
                text=f"Проект {project_num}", 
                command=lambda b=binary: self.launch_binary(b)
            )
            button.pack(side=tk.LEFT, padx=10)
            
            # Добавление описания
            desc = descriptions.get(binary, "Неизвестный проект")
            desc_label = ttk.Label(frame, text=desc)
            desc_label.pack(side=tk.LEFT, padx=10, fill=tk.X)
    
    def launch_binary(self, binary_name):
        """
        Запуск бинарного файла
        
        Args:
            binary_name: Имя бинарного файла для запуска
        """
        binary_path = os.path.join("binaries", binary_name)
        
        if not os.path.exists(binary_path):
            messagebox.showerror("Ошибка", f"Бинарный файл '{binary_path}' не найден!")
            return
            
        try:
            subprocess.Popen([binary_path], shell=True)
            messagebox.showinfo("Запуск", f"Запущен {binary_name}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить {binary_name}: {str(e)}")

def main():
    """Основная функция запуска приложения"""
    root = tk.Tk()
    app = ApplicationLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 