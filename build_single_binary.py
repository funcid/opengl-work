"""
Скрипт сборки отдельного бинарного файла

Сборка отдельного указанного проекта в бинарный файл с помощью PyInstaller.
Использование: python build_single_binary.py <имя_файла.py>
Оптимизирован для минимального размера выходного файла.

Автор: Царюк Артём Владимирович
"""

import os
import subprocess
import sys
import time
import shutil

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
    print(create_banner(f"Оптимизированная сборка бинарного файла для {project_file}"))
    
    # Начинаем отсчет времени
    start_time = time.time()
    
    # Создание spec-файла для улучшенной оптимизации
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Определяем модули, которые можно исключить для уменьшения размера бинарного файла
excluded_modules = [
    'matplotlib', 'scipy', 'pandas', 'tkinter', 'PIL.ImageQt',
    'PySide2', 'PyQt5', 'IPython', 'PyQt4', 'wx', 'pydoc',
    'email', 'html', 'http', 'xml', 'logging', 'doctest', 'argparse',
    'zipfile', 'pytz', 'unicodedata', 'bz2', 'encodings.idna',
    'encodings.*', 'unittest', 'test', 'pdb', 'difflib', 'pydoc_data'
]

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
    
    print("Создан оптимизированный spec-файл для сборки")
    
    # Определяем опции PyInstaller
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
        print(f"Сборка бинарного файла для {project_file} успешно завершена")
        
        # Перемещение бинарного файла в нашу папку binaries
        source = os.path.join("dist", f"{project_name}_bin.exe")
        destination = os.path.join("binaries", f"{project_name}_bin.exe")
        
        if os.path.exists(source):
            try:
                os.replace(source, destination)
                
                # Вывод информации о размере файла
                file_size_mb = os.path.getsize(destination) / (1024 * 1024)
                print(f"Бинарный файл перемещен в {destination} (Размер: {file_size_mb:.2f} МБ)")
                
                # Вывод информации о затраченном времени
                elapsed_time = time.time() - start_time
                print(f"Время сборки: {elapsed_time:.2f} секунд")
                
                # Очистка временных файлов
                cleanup_temp_files([spec_file], ["build", "dist", "__pycache__"])
                
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

def cleanup_temp_files(files, directories):
    """Очистка временных файлов и директорий после сборки"""
    
    print("\nОчистка временных файлов...")
    
    # Удаление временных файлов
    for file in files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Удален файл: {file}")
            except Exception as e:
                print(f"Не удалось удалить файл {file}: {e}")
    
    # Удаление временных директорий
    for directory in directories:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print(f"Удалена директория: {directory}")
            except Exception as e:
                print(f"Не удалось удалить директорию {directory}: {e}")

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