# Проекты по Компьютерной Графике с OpenGL  
# OpenGL Graphics Projects

*[English version below](#opengl-graphics-projects)*

## О проектах

Этот репозиторий содержит коллекцию проектов по компьютерной графике, реализованных с использованием OpenGL и Python. Проекты охватывают различные аспекты компьютерной графики, начиная от базовых геометрических фигур и заканчивая алгоритмами обработки изображений.

### Реализованные проекты:

1. **Платонические тела** - визуализация правильных многогранников (тетраэдр, куб, октаэдр, додекаэдр, икосаэдр)
2. **Алгоритмы рисования линий** - реализации алгоритмов Брезенхема, ЦДА и других методов растеризации линий
3. **Алгоритмы отсечения линий** - алгоритмы Коэна-Сазерленда, центральных точек и Цируса-Бека
4. **Исследование цветовых систем** - интерактивное отображение RGB, CMYK, HSV и LAB цветовых пространств
5. **Алгоритмы дизеринга изображений** - упорядоченный дизеринг, случайный и алгоритм Флойда-Стейнберга
6. **Алгоритмы растеризации эллипсов** - демонстрация различных методов растеризации эллипсов

## Использование

Существует три способа запуска проектов:

### 1. Через графический лаунчер

Просто запустите `Лаунчер Проектов OpenGL.exe` в корневой директории. Это наиболее удобный способ доступа ко всем проектам.

### 2. Напрямую через исполняемые файлы

Все скомпилированные бинарные файлы находятся в директории `binaries`. Вы можете запустить любой из них напрямую.

### 3. Запуск исходного кода

Если вы предпочитаете запустить проекты из исходного кода:

1. Установите зависимости: `pip install pygame PyOpenGL numpy pillow`
2. Запустите любой проект: `python <имя_файла.py>`

## Сборка бинарных файлов

Если вы хотите пересобрать бинарные файлы:

### Сборка всех проектов
- Windows: Запустите `build_all_binaries.bat`
- Другие системы: `python build_binaries.py`

### Сборка отдельного проекта
- `python build_single_binary.py <имя_файла.py>`

## Структура проекта

- `/utils` - вспомогательные модули для OpenGL, графики и UI
- `/binaries` - скомпилированные исполняемые файлы
- Файлы `*.py` в корневой директории - исходный код проектов
- `build_*.py` - скрипты для сборки бинарных файлов
- `launcher.py` - графический интерфейс для запуска проектов

## Особенности обновления

- **Многоязычный интерфейс**: Доступен интерфейс на русском и английском языках
- **Улучшенные скрипты сборки**: Скрипты теперь показывают время сборки и имеют расширенный функционал
- **Расширенная документация**: Подробные инструкции на двух языках

## Управление

- **WASD** - Перемещение камеры
- **Мышь** - Вращение камеры
- **Колесо мыши** - Масштабирование
- **ESC** - Выход из приложения
- **Дополнительные клавиши** - описаны внутри каждого приложения

## Автор

Царюк Артём Владимирович

---

# OpenGL Graphics Projects

## Overview

This repository contains a collection of computer graphics projects implemented using OpenGL and Python. The projects cover various aspects of computer graphics, from basic geometric shapes to image processing algorithms.

### Implemented Projects:

1. **Platonic Solids** - visualization of regular polyhedra (tetrahedron, cube, octahedron, dodecahedron, icosahedron)
2. **Line Drawing Algorithms** - implementations of Bresenham's algorithm, DDA, and other line rasterization methods
3. **Line Clipping Algorithms** - Cohen-Sutherland, midpoint, and Cyrus-Beck algorithms
4. **Color Systems Exploration** - interactive display of RGB, CMYK, HSV, and LAB color spaces
5. **Image Dithering Algorithms** - ordered dithering, random dithering, and Floyd-Steinberg algorithm
6. **Ellipse Rasterization Algorithms** - demonstration of various methods for ellipse rasterization

## Usage

There are three ways to run the projects:

### 1. Using the Graphical Launcher

Simply run `OpenGL_Projects_Launcher.exe` or `Лаунчер Проектов OpenGL.exe` in the root directory. This is the most convenient way to access all projects.

### 2. Directly via Executables

All compiled binary files are located in the `binaries` directory. You can run any of them directly.

### 3. Running from Source Code

If you prefer to run the projects from source code:

1. Install dependencies: `pip install pygame PyOpenGL numpy pillow`
2. Run any project: `python <filename.py>`

## Building Binaries

If you want to rebuild the binaries:

### Building All Projects
- Windows: Run `build_all_binaries.bat`
- Other systems: `python build_binaries.py`

### Building a Single Project
- `python build_single_binary.py <filename.py>`

## Project Structure

- `/utils` - utility modules for OpenGL, graphics, and UI
- `/binaries` - compiled executable files
- `*.py` files in the root directory - project source code
- `build_*.py` - scripts for building binary files
- `launcher.py` - graphical interface for launching projects

## Update Features

- **Multilingual Interface**: Interface available in Russian and English
- **Improved Build Scripts**: Scripts now show build time and have enhanced functionality
- **Extended Documentation**: Detailed instructions in two languages

## Controls

- **WASD** - Camera movement
- **Mouse** - Camera rotation
- **Mouse wheel** - Zoom
- **ESC** - Exit application
- **Additional keys** - described within each application

## Author

Tsaryuk Artem Vladimirovich