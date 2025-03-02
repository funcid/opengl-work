"""
Скрипт сборки отдельного бинарного файла

Сборка отдельного указанного проекта в бинарный файл с помощью PyInstaller.
Использование: python build_single_binary.py <имя_файла.py>

Автор: Царюк Артём Владимирович
"""

import os
import subprocess
import sys
import time

def create_banner(text):
    """Создание декоративного баннера для текста"""
    return f"\n{'='*60}\n{text}\n{'='*60}"

def build_binary(project_file):
    """
    Сборка бинарного файла из файла Python проекта
    
    Args:
        project_file: Путь к файлу проекта для сборки
        
    Returns:
        bool: True в случае успешной сборки, иначе False
    """
    # Проверяем существование файла
    if not os.path.exists(project_file):
        print(f"Ошибка: Файл {project_file} не существует.")
        return False
    
    # Проверяем расширение файла
    if not project_file.endswith('.py'):
        print(f"Предупреждение: Файл {project_file} не является Python файлом (.py)")
        response = input("Хотите продолжить? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Создание директории для вывода, если она не существует
    if not os.path.exists("binaries"):
        os.makedirs("binaries")
        print("Создана директория 'binaries'")
    
    project_name = os.path.splitext(project_file)[0]
    print(create_banner(f"Сборка бинарного файла для {project_file}"))
    
    # Начинаем отсчет времени
    start_time = time.time()
    
    # Формирование команды PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",        # Создание одного исполняемого файла
        "--noconsole",      # Не показывать окно консоли при запуске
        f"--name={project_name}_bin",  # Имя выходного файла
        "--add-data", "utils;utils",  # Включение папки utils
        project_file  # Файл Python для конвертации
    ]
    
    print(f"Выполнение команды: {' '.join(cmd)}")
    
    # Выполнение команды с выводом в реальном времени
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Вывод результатов в реальном времени
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    
    # Проверка результата выполнения
    if process.returncode == 0:
        print(f"Сборка бинарного файла для {project_file} успешно завершена")
        
        # Перемещение бинарного файла в нашу папку binaries
        source = os.path.join("dist", f"{project_name}_bin.exe")
        destination = os.path.join("binaries", f"{project_name}_bin.exe")
        
        if os.path.exists(source):
            try:
                os.replace(source, destination)
                print(f"Бинарный файл перемещен в {destination}")
                
                # Вывод информации о затраченном времени
                elapsed_time = time.time() - start_time
                print(f"Время сборки: {elapsed_time:.2f} секунд")
                
                return True
            except Exception as e:
                print(f"Ошибка при перемещении бинарного файла: {e}")
                return False
        else:
            print(f"Бинарный файл не найден по пути {source}")
            return False
    else:
        print(f"Ошибка при сборке {project_file}. Код возврата: {process.returncode}")
        return False

if __name__ == "__main__":
    # Проверка аргументов командной строки
    if len(sys.argv) < 2:
        print("Использование: python build_single_binary.py <имя_файла.py>")
        print("Пример: python build_single_binary.py project1.py")
        sys.exit(1)
    
    # Получение имени файла из аргументов
    project_file = sys.argv[1]
    
    # Запуск сборки
    success = build_binary(project_file)
    
    # Вывод результата
    if success:
        output_path = os.path.join("binaries", f"{os.path.splitext(project_file)[0]}_bin.exe")
        print(create_banner("Сборка успешно завершена!"))
        print(f"Бинарный файл доступен по пути: {output_path}")
        
        # Предложение запустить созданный бинарный файл
        response = input("Хотите запустить созданный бинарный файл? (y/n): ")
        if response.lower() == 'y':
            subprocess.Popen([output_path], shell=True)
    else:
        print(create_banner("Сборка не удалась")) 