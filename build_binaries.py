"""
Скрипт сборки бинарных файлов

Автоматическая сборка всех Python файлов проектов в бинарные файлы
с использованием PyInstaller и оптимизацией размера.

Автор: Царюк Артём Владимирович
"""

import os
import glob
import subprocess
import time
import sys
import shutil

def create_banner(text):
    """Создание декоративного баннера для текста"""
    return f"\n{'='*60}\n{text}\n{'='*60}"

def get_project_files():
    """
    Получение всех файлов проектов
    
    Returns:
        list: Список файлов проектов
    """
    # Ищем все Python файлы, начинающиеся с "project" в текущей директории
    project_files = glob.glob("project*.py")
    
    # Сортируем файлы по номеру проекта
    project_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    
    return project_files

def create_common_spec(project_file, excluded_modules):
    """
    Создание spec-файла для оптимизированной сборки
    
    Args:
        project_file (str): Имя файла проекта
        excluded_modules (list): Список модулей для исключения
        
    Returns:
        str: Имя созданного spec-файла
    """
    project_name = os.path.splitext(project_file)[0]
    
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

excluded_modules = {repr(excluded_modules)}

a = Analysis(
    ['{project_file}'],
    pathex=[],
    binaries=[],
    datas=[('utils', 'utils')],
    hiddenimports=['numpy.core._methods'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excluded_modules,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{project_name}_bin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[
        'libopenblas*', 'tcl*', 'tk*', 'libQt*', 'QtCore*', 'QtGui*',
        'QtWidgets*', '*_test*', '*.pyo', '*.pyc'
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    spec_file = f"{project_name}_bin.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    return spec_file

def build_binary(project_file, total_projects, current_index, excluded_modules):
    """
    Сборка бинарного файла для проекта
    
    Args:
        project_file (str): Путь к файлу проекта
        total_projects (int): Общее количество проектов
        current_index (int): Текущий индекс проекта
        excluded_modules (list): Список модулей для исключения
        
    Returns:
        tuple: (bool, float) Успех сборки и размер файла в МБ
    """
    # Получаем имя проекта без расширения
    project_name = os.path.splitext(project_file)[0]
    
    print(create_banner(f"[{current_index}/{total_projects}] Сборка оптимизированного бинарного файла для {project_file}"))
    
    # Засекаем время начала сборки
    start_time = time.time()
    
    # Создание оптимизированного spec-файла
    spec_file = create_common_spec(project_file, excluded_modules)
    print(f"Создан оптимизированный spec-файл для {project_file}")
    
    # Опции PyInstaller
    cmd = [
        "pyinstaller",
        "--clean",          # Очистить кэш PyInstaller перед сборкой
        "--strip",          # Удалить отладочные символы
    ]
    
    # Проверяем наличие UPX для сжатия
    try:
        upx_result = subprocess.run(["upx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if upx_result.returncode == 0:
            print("UPX найден, будет выполнено дополнительное сжатие")
            cmd.extend(["--upx-dir", "."])
        else:
            print("UPX не найден, сжатие не будет выполнено")
            cmd.append("--noupx")
    except:
        print("UPX не найден, сжатие не будет выполнено")
        cmd.append("--noupx")
    
    # Добавляем spec файл
    cmd.append(spec_file)
    
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
        # Перемещение бинарного файла в папку binaries
        source = os.path.join("dist", f"{project_name}_bin.exe")
        destination = os.path.join("binaries", f"{project_name}_bin.exe")
        
        if os.path.exists(source):
            try:
                os.replace(source, destination)
                
                # Получаем размер файла в МБ
                file_size_mb = os.path.getsize(destination) / (1024 * 1024)
                
                print(f"Бинарный файл перемещен в {destination} (Размер: {file_size_mb:.2f} МБ)")
                
                # Выводим затраченное время
                elapsed_time = time.time() - start_time
                print(f"Время сборки: {elapsed_time:.2f} секунд")
                
                return True, file_size_mb
            except Exception as e:
                print(f"Ошибка при перемещении бинарного файла: {e}")
                return False, 0
        else:
            print(f"Бинарный файл не найден по пути {source}")
            return False, 0
    else:
        print(f"Ошибка при сборке {project_file}")
        return False, 0

def cleanup_temp_files(spec_files):
    """
    Очистка временных файлов и директорий после сборки
    
    Args:
        spec_files (list): Список spec-файлов для удаления
    """
    print(create_banner("Очистка временных файлов"))
    
    # Удаление spec-файлов
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            try:
                os.remove(spec_file)
                print(f"Удален файл: {spec_file}")
            except Exception as e:
                print(f"Не удалось удалить файл {spec_file}: {e}")
    
    # Удаление временных директорий
    temp_dirs = ["build", "dist", "__pycache__"]
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"Удалена директория: {temp_dir}")
            except Exception as e:
                print(f"Не удалось удалить директорию {temp_dir}: {e}")

def main():
    """Основная функция сборки всех бинарных файлов"""
    # Получаем файлы проектов
    project_files = get_project_files()
    
    if not project_files:
        print("Не найдены файлы проектов.")
        return
    
    print(create_banner(f"Найдено {len(project_files)} файлов проектов для сборки:"))
    for i, project in enumerate(project_files, 1):
        print(f"{i}. {project}")
    
    # Запрос подтверждения
    response = input("\nХотите собрать бинарные файлы для всех проектов? (y/n): ")
    if response.lower() != 'y':
        print("Сборка отменена.")
        return
    
    # Проверка наличия директории для вывода
    if not os.path.exists("binaries"):
        os.makedirs("binaries")
        print("Создана директория 'binaries'")
    
    # Определяем общие модули для исключения
    excluded_modules = [
        'matplotlib', 'scipy', 'pandas', 'tkinter', 'PIL.ImageQt',
        'PySide2', 'PyQt5', 'IPython', 'PyQt4', 'wx', 'pydoc',
        'email', 'html', 'http', 'xml', 'logging', 'doctest', 'argparse',
        'zipfile', 'pytz', 'unicodedata', 'bz2', 'encodings.idna',
        'encodings.*', 'unittest', 'test', 'pdb', 'difflib', 'pydoc_data'
    ]
    
    # Запуск процесса сборки для каждого проекта
    total_start_time = time.time()
    total_projects = len(project_files)
    successful_builds = 0
    failed_builds = 0
    spec_files = []
    file_sizes = []
    
    for index, project_file in enumerate(project_files, 1):
        spec_files.append(f"{os.path.splitext(project_file)[0]}_bin.spec")
        success, file_size = build_binary(project_file, total_projects, index, excluded_modules)
        
        if success:
            successful_builds += 1
            file_sizes.append((project_file, file_size))
        else:
            failed_builds += 1
        
        # Разделитель между проектами
        if index < total_projects:
            print("\n" + "-"*60 + "\n")
    
    # Очистка временных файлов
    cleanup_temp_files(spec_files)
    
    # Вывод итоговой статистики
    total_elapsed_time = time.time() - total_start_time
    
    print(create_banner("Результаты сборки"))
    print(f"Всего проектов: {total_projects}")
    print(f"Успешно собрано: {successful_builds}")
    print(f"Не удалось собрать: {failed_builds}")
    print(f"Общее время сборки: {total_elapsed_time:.2f} секунд")
    
    # Вывод размеров файлов
    if file_sizes:
        print("\nРазмеры собранных бинарных файлов:")
        for project, size in file_sizes:
            print(f"  {project}: {size:.2f} МБ")
    
    print(create_banner("Сборка завершена"))

if __name__ == "__main__":
    main() 