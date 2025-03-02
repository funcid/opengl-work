"""
Скрипт сборки бинарных файлов

Автоматическая сборка всех проектов в бинарные файлы с помощью PyInstaller.
Скрипт находит все файлы project*.py и компилирует их в исполняемые файлы.

Автор: Царюк Артём Владимирович
"""

import os
import subprocess
import glob
import time
import sys

def create_banner(text):
    """Создание декоративного баннера для текста"""
    return f"\n{'='*60}\n{text}\n{'='*60}"

# Получение всех файлов проектов
project_files = glob.glob("project*.py")

print(f"Найдено {len(project_files)} файлов проектов для сборки:")
for project in project_files:
    print(f"- {project}")

# Запрос подтверждения
input("\nНажмите Enter для начала сборки бинарных файлов...")

# Создание директории для вывода, если она не существует
if not os.path.exists("binaries"):
    os.makedirs("binaries")
    print("Создана директория 'binaries'")

# Настройка общих параметров PyInstaller
pyinstaller_common_args = [
    "--onefile",         # Создание одного исполняемого файла
    "--noconsole",       # Не показывать окно консоли при запуске
    "--add-data", "utils;utils"  # Включение папки utils
]

# Счетчики для отслеживания прогресса
total_projects = len(project_files)
successful_builds = 0
failed_builds = []
start_time = time.time()

# Сборка каждого проекта
for i, project_file in enumerate(project_files, 1):
    project_name = os.path.splitext(project_file)[0]
    print(create_banner(f"Сборка бинарного файла для {project_file} ({i}/{total_projects})"))
    
    # Формирование команды PyInstaller
    cmd = [
        "pyinstaller",
        *pyinstaller_common_args,
        f"--name={project_name}_bin",  # Имя выходного файла
        project_file  # Файл Python для конвертации
    ]
    
    print(f"Выполнение команды: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Сборка бинарного файла для {project_file} успешно завершена")
        
        # Перемещение бинарного файла в нашу папку binaries
        source = os.path.join("dist", f"{project_name}_bin.exe")
        destination = os.path.join("binaries", f"{project_name}_bin.exe")
        
        if os.path.exists(source):
            try:
                os.replace(source, destination)
                print(f"Бинарный файл перемещен в {destination}")
                successful_builds += 1
            except Exception as e:
                print(f"Ошибка при перемещении бинарного файла: {e}")
                failed_builds.append((project_file, f"Ошибка перемещения: {e}"))
        else:
            print(f"Бинарный файл не найден по пути {source}")
            failed_builds.append((project_file, "Файл не найден после сборки"))
    else:
        print(f"Ошибка при сборке {project_file}:")
        print(result.stderr)
        failed_builds.append((project_file, "Ошибка при сборке"))

# Вывод статистики сборки
elapsed_time = time.time() - start_time
print(create_banner("Процесс сборки завершен"))
print(f"Общее время выполнения: {elapsed_time:.2f} секунд")
print(f"Успешно собрано: {successful_builds}/{total_projects} проектов")

if failed_builds:
    print(f"\nНеудачные сборки ({len(failed_builds)}):")
    for project, reason in failed_builds:
        print(f"- {project}: {reason}")

print("\nБинарные файлы доступны в папке 'binaries'.")

# Очистка временных файлов PyInstaller
for temp_dir in ["build", "__pycache__"]:
    if os.path.exists(temp_dir):
        print(f"Очистка временной директории: {temp_dir}")
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    # Рекурсивное удаление с помощью системных команд
                    if sys.platform == "win32":
                        subprocess.run(["rmdir", "/S", "/Q", file_path], shell=True)
                    else:
                        subprocess.run(["rm", "-rf", file_path])
            except Exception as e:
                print(f"Ошибка при удалении {file_path}: {e}")

print("Сборка бинарных файлов успешно завершена!") 