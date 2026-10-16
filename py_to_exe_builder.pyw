# -*- coding: utf-8 -*-
"""
Py To EXE Builder
Версия: 0.8.2  (PySide6 / Qt6)

Изменения 0.8.2 (по итогам код-аудита):
- 🛑 Кнопка «Стоп» и корректное закрытие окна во время сборки/скачивания
  (процессы PyInstaller/pip убиваются, потоки дожидаются).
- 🐍 Сборщик, собранный в EXE (frozen), ищет настоящий python (py -3 / PATH)
  для режима «Текущий Python» и для анализа импортов.
- 🐛 Файлы с UTF-8 BOM больше не теряют импорты; проект в папке с именем
  dist/build/env больше не даёт «0 импортов».
- 🐛 VC++ Runtime DLL берутся под разрядность цели (x86 → SysWOW64).
- 🐛 Правильный путь к exe в режиме onedir, без подхвата устаревшего exe.
- 📦 Перед pip показывается список пакетов на подтверждение; в «Свой Python»
  ставятся только отсутствующие пакеты без -U; кэш хеша зависимостей.
- 🪟 yt-dlp_win7.exe вшивается только если проект использует yt_dlp.
- ⚡ Проверка python и поиск UPX больше не блокируют окно; лог ограничен.
- 🔒 UPX закреплён на версии 4.2.4; SHA256-проверка для известных хешей.

Изменения 0.8.1:
- 🐛 Фикс: если в настройках сохранён режим «📁 Свой Python» без пути к
  python.exe, сборка падала только в самом конце — после анализа проекта,
  скачивания UPX и поиска ffmpeg («❌ Свой Python: путь не задан»). Теперь
  путь проверяется ДО старта сборки: сразу показывается понятное окно с
  предложением указать python.exe или переключиться на «🐍 Текущий Python».

Изменения 0.8.0:
- 🎨 НОВЫЙ ДИЗАЙН (вариант A): тёмная «карточная» тема Modern Dark
  (+ Modern Light), две карточки «Проект» и «Имя и иконка».
- ⤓ Drag-and-drop: .py/.pyw, папку проекта или .ico можно перетащить
  в окно; папка проекта и папка EXE подставляются автоматически.
- 📄 Карточка выбранного файла (имя, папка, число .py), кнопки выбора
  папок — иконкой внутри полей ввода.
- 🖼 Быстрая сетка иконок прямо в главном окне + «…» — полный выбор.
- 🔘 Основные опции — чипы-переключатели; редкие — в «⚙ Ещё».
- 🚀 Кнопка сборки во всю ширину + полоса прогресса во время сборки.
- 🌈 Цветной лог: ошибки/предупреждения/успех; кнопки лога — в его шапке.

Изменения 0.7.17:
- 🧩 ПОДДЕРЖКА tkinter-приложений: раньше --collect-all применялся только к
  сторонним пакетам, а tkinter — stdlib и в этот список не попадал. Сборщик
  полагался на встроенный хук PyInstaller, который не всегда тянет tcl/tk
  рантайм (_tkinter.pyd, tcl86t.dll/tk86t.dll, папки tcl/ tk/) → готовый exe
  падал с «No module named tkinter». Теперь: если проект реально использует
  tkinter (авто-детект по импортам), во ВСЕХ режимах добавляются
  `--collect-all tkinter` + hidden-imports (tkinter.ttk/filedialog/messagebox/
  simpledialog/scrolledtext/colorchooser/font/_tkinter).
- ⚠ ПРЕДУПРЕЖДЕНИЕ О ПРЕРЕКВИЗИТЕ: если для tkinter-проекта выбран
  embeddable/portable Python (режимы win7/win10/win11), сборщик заранее
  проверяет наличие _tkinter в целевом Python и предупреждает — embeddable
  Python поставляется БЕЗ tkinter/tcl/tk, так что для tkinter-приложений
  нужен обычный установленный Python.

Изменения 0.7.16:
- 🖼 +22 новых вида иконок: два сердечка, разбитое сердце, валентинка,
  бабочка, клевер, свеча, воздушный шарик, торт, тюльпан, снеговик,
  воздушный змей, пчела, божья коровка, черепаха, заяц, утка, пингвин,
  очки, футболка, кольцо с камнем, магический шар, цилиндр.
- 🔍 ПОИСК ПО-РУССКИ: у иконок появились русские ключевые слова —
  «сердце», «сердечко», «звезда», «машина», «домик» и т.д. находят
  нужную плитку (раньше поиск понимал только английские имена — поэтому
  «сердечко» ничего не находило, хотя иконка Heart есть).

Изменения 0.7.15:
- 🗂 ИКОНКИ СГРУППИРОВАНЫ — БЕЗ ДУБЛЕЙ: в сетке теперь ОДНА плитка на
  каждую иконку (глиф). Раньше одна и та же иконка встречалась много раз
  (Python Blue/Green, Star Red/Blue/Pink, Flat/Round/Neon-серии...).
  Клик по плитке открывает панель: строки = цветовые варианты,
  столбцы = 8 стилей. Один клик — и вариант+стиль выбраны.
- 🧹 Удалены пресеты-дубликаты стилевых серий (Flat*, Round*, Rounded*,
  Neon*, Split*, Radial*, VGrad*) — они полностью покрываются выбором
  стиля в панели. Цветовые варианты (Star Red и т.п.) сохранены.
- ⚡ Окно выбора иконок открывается БЫСТРО:
  1) Диалог создаётся ОДИН раз и переиспользуется — раньше при каждом
     открытии заново строились сотни плиток с превью (отсюда задержка).
     Повторные открытия теперь мгновенные.
  2) Кэш превью-пиксмапов (имя+размер+стиль): превью рисуется один раз
     за сессию — ускоряет и первое открытие, и всплывающие панели стилей.
  3) На время построения сетки отключена перерисовка (setUpdatesEnabled).

Изменения 0.7.14:
- 🖱 Клик ПО САМОЙ ИКОНКЕ (по всей плитке) открывает сбоку панель её
  стилей — кнопка «Выбрать» убрана совсем. Курсор над плиткой —
  «рука», чтобы было видно, что она кликабельна.

Изменения 0.7.13:
- 🎨 Выбор стиля переделан ПО КЛИКУ НА ИКОНКУ: в окне выбора жмёшь
  «Выбрать» у иконки — рядом всплывает панель со ВСЕМИ 8 стилями
  именно этой иконки (реальные превью), кликаешь мышкой на нужный —
  и выбор сделан. Никаких отдельных комбо-боксов.
- 🧹 Убрано дублирование: комбо «Стиль фона» из главного окна и
  селектор стиля из шапки окна выбора удалены. Выбранный стиль
  по-прежнему запоминается в настройках и виден в превью и логе.

Изменения 0.7.12:
- 💡 НАСТОЯЩИЙ СТИЛЬ «НЕОН» в общем списке стилей (раньше неон был лишь
  серией пресетов Neon* с тёмным фоном). Теперь ЛЮБУЮ иконку можно
  показать в неоне: почти чёрный фон + глиф в ярком акцентном цвете
  (берётся из bg2 пресета и «разгоняется» до максимальной яркости)
  + РЕАЛЬНОЕ СВЕЧЕНИЕ (bloom): вокруг глифа рисуется мягкий ореол
  (сепарабельный box-blur маски глифа, аддитивное наложение).
  В превью (главное окно и окно выбора) неон тоже отображается.

Изменения 0.7.11:
- 🎨 ВЫБОР СТИЛЯ ДЛЯ ЛЮБОЙ ИКОНКИ: теперь стиль фона — отдельный
  переключатель, применимый к любой иконке (раньше стиль был «зашит»
  в пресет). Выбрал иконку → выбрал стиль → готово.
  • В окне выбора иконок сверху появился селектор стиля — ВСЕ превью
    мгновенно перерисовываются в выбранном стиле.
  • В главном окне рядом с иконкой — комбо «Стиль фона»
    (Как в пресете / Градиент / Плоский / Верт. градиент / Радиальный /
    Срез / Круглый / Скруглённый). Превью обновляется сразу.
  • Выбранный стиль сохраняется в настройках и применяется при
    генерации .ico для сборки (имя кэш-файла учитывает стиль).

Изменения 0.7.10:
- 🔒 Кнопка «🚀 Сделать EXE» на время сборки блокируется ВИЗУАЛЬНО ЯВНО:
  текст меняется на «⏳ Идёт сборка...» (сама блокировка была и раньше,
  но выглядела незаметно). После завершения/ошибки текст возвращается.
- 📂 После УСПЕШНОЙ сборки автоматически открывается папка с готовым
  EXE, причём файл сразу ВЫДЕЛЕН в проводнике (explorer /select).
  На macOS — Finder с выделением (open -R), на Linux — файл-менеджер.

Изменения 0.7.9:
- 🎨 СТИЛИ ФОНА иконок: кроме классического градиента добавлены
  flat (плоский), vgrad (вертикальный градиент), radial (радиальный),
  split (двухцветный срез), circle (круглый бейдж с прозрачными углами),
  rounded (скруглённый квадрат с прозрачными углами). У пресета появилось
  опциональное поле "style" (по умолчанию — прежний градиент).
- 🖼 +22 новых глифа: якорь, зонт, песочные часы, пазл, планета, НЛО,
  кристалл, мегафон, кнопка питания, уровень сигнала, бар-график,
  лин-график, круговая диаграмма, цепь-ссылка, меч, зелье, джойстик,
  луна со звездой, курсор, туча с молнией, гайка, радар.
- 🎨 +85 новых пресетов: серии Flat, Round (круглые бейджи),
  Neon (тёмный фон + яркий глиф), Split, Radial, Rounded.
- 🗜 МУЛЬТИРАЗМЕРНЫЙ .ico: теперь в файл пишутся 5 изображений
  (64/48/32/24/16 px, даунскейл с усреднением) — иконка выглядит чётко
  и в заголовке окна, и в таскбаре, и в проводнике (раньше был один
  64px, Windows масштабировала его сама — мыло на мелких размерах).
- 🔍 Поиск в окне выбора иконок: поле фильтра по имени — при ~300
  иконках листать сетку вручную уже неудобно.
- 🧹 Рефакторинг: генерация фона вынесена в _base_pixel/_style_alpha,
  запись одного изображения ICO — в _ico_image_bytes (write_ico теперь
  просто собирает мультиразмерный контейнер).

Изменения 0.7.8:
- 🐛 Фикс приоритета операторов в логировании пин-версий: на Python 3.9+
  лог ложно сообщал «Пин-версии → PySide6==6.1.3» (установка не страдала).
- 🐛 Отказ от скачивания ffmpeg теперь запоминается на время сборки —
  раньше вопрос задавался повторно после авто-скачивания UPX.
- 🐛 Убран риск «QThread: Destroyed while thread is still running»:
  ссылки на отработавшие воркеры удерживаются до завершения потока.
- 🐛 Фикс глифов wifi / antenna / mushroom / rainbow: «вырезание»
  прозрачным цветом стирало фон-градиент (дырки в .ico). Теперь фон
  восстанавливается. У antenna мачта больше не стирается целиком.
- 🐛 PyInstaller всегда запускается с --noconfirm — раньше без
  режимов universal/auto_opt сборка могла упасть на подтверждении
  (stdin=DEVNULL).
- 🐛 Папки Lib/Scripts/Include пропускаются при сканировании ТОЛЬКО если
  это реально Python/venv (рядом python.exe или pyvenv.cfg) — обычные
  папки проекта с такими именами больше не теряются.
- 🐛 Кнопка «💾 Экспорт всех иконок» (эксперт-настройки) — фича была
  заявлена в «О программе», но недостижима из UI.
- 🧹 Чистка мёртвого кода: resolve_python_exe, portable_python_exe,
  неиспользуемые импорты (QSize, QIcon, QSizePolicy), мёртвые локальные
  переменные, двойной вызов find_ffmpeg_binaries, кэш local_module_names.

Изменения 0.7.7:
- 🏗 Выбор АРХИТЕКТУРЫ Windows для авто-скачиваемого Python:
  x64 (amd64) / x86 (win32) / ARM64. Раньше было жёстко amd64 —
  теперь 32-битные и ARM-сборки возможны. Сборщик качает
  соответствующий python-{ver}-embed-{arch}.zip и кэширует его
  отдельно (py-{ver}-{arch}). Селектор активен только для режимов
  Windows 7/10/11; для «Текущий»/«Свой Python» игнорируется.
- 🚫 ARM64 embeddable существует только с Python 3.11+, поэтому
  комбинация Win7 (3.8) + ARM64 отклоняется с понятным сообщением.
- ℹ ВАЖНО про кросс-ОС: PyInstaller — НЕ кросс-компилятор. .exe
  собирается только на Windows, Linux-бинарь (ELF) — только на Linux.
  Embeddable Python есть только под Windows. «Собрать под Linux
  из-под Windows» технически невозможно — нужно запускать сборку
  на самом Linux (там будет использован системный python + venv).
- ⚠ Напоминание: PySide6/PyQt6 не имеют 32-бит (win32) колёс —
  x86-сборка подходит для чистого Python / tkinter, но не для Qt.

Изменения 0.7.6:
- 🚫 В Win7-режиме НЕ бандлим ffmpeg автоматически.
  Современный ffmpeg.exe (gyan.dev, BtbN, WinGet) часто скомпилирован
  с требованием SSE4.1 / AVX и крашится с `0xc0000005` на старых CPU
  (Celeron T-серии, ранние Atom). Лучше не положить — yt-dlp сам
  обойдётся без него для single-stream форматов. Пользователь может
  вручную положить Win7-совместимый ffmpeg.exe рядом с EXE, если ему
  нужен MP3-экстракт.

Изменения 0.7.5:
- 🪟 Гибридная Win7-сборка с bundled standalone yt-dlp.exe.
  Когда «Целевая ОС» = Windows 7 — сборщик автоматически:
    1) Скачивает СВЕЖИЙ yt-dlp_win7.exe из nicolaasjan/yt-dlp
       (фактически рекомендованный yt-dlp командой fork для Win7,
       с встроенным Python 3.14 и phantomjs).
    2) Прицепляет его внутрь EXE через --add-binary.
    3) Добавляет суффикс «_win7» к имени итогового exe.
  Приложение на запуске находит bundled yt-dlp.exe (через sys._MEIPASS)
  и вызывает его как subprocess. Это обходит проблему «yt-dlp Python
  модуль ≤ 2024.10.22 на Python 3.8 уже не качает с YouTube».
  Win10+ сборка НЕ меняется — она по-прежнему использует Python-модуль.
- 📥 Кэш yt-dlp.exe: %LOCALAPPDATA%\\Py-To-EXE-Builder\\nicolaasjan_ytdlp\\
  с tag-файлом — повторно не качаем, если версия совпадает.

Изменения 0.7.4:
- 🐛 Фикс «Qt plugin directory '...PySide6/plugins' does not exist!» при
  кириллице в пути проекта. PyInstaller-хуки Qt запускают subprocess,
  который ломает кодировку non-ASCII путей → плагины «не находятся».
  Решение: portable Python всегда живёт в %LOCALAPPDATA%/Py-To-EXE-Builder/
  portable_pythons/ (гарантированно ASCII), независимо от того, где
  лежит сборщик или проект.
- ⚠ Если в пути ПРОЕКТА есть кириллица — выводится предупреждение.
  Сама сборка обычно проходит, т.к. исполняемый Python теперь в ASCII.

Изменения 0.7.3:
- 🐛 Анализатор больше не сканирует свои же рабочие папки.
  В skip_dirs добавлены: _portable_pythons, _py_to_exe_builder,
  EXE_Output. Раньше после первой сборки анализатор находил 3000+
  файлов внутри yt_dlp/extractor (внутри portable python) и пытался
  pip-install имена типа «tiktok», «youtube», «abcnews» и т.д.
- 🐛 Скип относительных импортов («from .foo import bar») — раньше
  они ошибочно добавляли «foo» в top-level.
- 🐛 Фильтр stdlib C-расширений в install: имена с подчёркиванием
  (`_socket`, `_ssl`, `_brotli`, `_tkinter` ...) больше не идут в pip.
- 🔀 Алиасы import-name → pip-package: PIL→Pillow, Crypto→pycryptodome,
  OpenSSL→pyOpenSSL, cv2→opencv-python, yaml→PyYAML, bs4→beautifulsoup4,
  sklearn→scikit-learn, dateutil→python-dateutil, win32api/win32com/
  pywintypes→pywin32.
- 🚫 Не ставим в pip пакеты сборочной инфраструктуры (PyInstaller,
  pip, setuptools, wheel, altgraph, pefile, pywin32_ctypes, distutils,
  _distutils_hack, _pyinstaller_hooks_contrib) — приедут вместе с
  PyInstaller автоматически.

Изменения 0.7.2:
- 🐛 Фикс «DLL load failed while importing QtCore» на Windows 7.
  Qt 6.2+ официально требует Windows 10. Последняя версия PySide6
  с поддержкой Win7 — 6.1.3 (декабрь 2021). Пин для Python 3.8
  теперь жёстко привязывает PySide6 к 6.1.3 (и PyQt6 < 6.2).
  Также добавлено предупреждение в лог о том, что подменяется версия.

Изменения 0.7.1:
- 🐛 Фикс установки pip в portable Python 3.8 / 3.9.
  Главный bootstrap (https://bootstrap.pypa.io/get-pip.py) работает
  только с Python 3.10+. Для старых версий используется версионный
  URL: https://bootstrap.pypa.io/pip/3.8/get-pip.py (и .../pip/3.9/...).
  Без этого сборка под Win7 падала на этапе «Установка pip».

Изменения 0.7.0:
- 🪟 Один выпадающий список «Целевая ОС»: Текущий Python / Windows 7+ /
  Windows 10+ / Windows 11 / Свой Python. При выборе Windows-варианта
  сборщик САМ скачивает embeddable Python нужной версии в подпапку
  «portable_pythons» в %LOCALAPPDATA% (ASCII-путь, не лезет в систему!),
  ставит туда pip и зависимости проекта, и собирает EXE через него.
  Никаких ручных установок Python — поставил галку, и оно работает.
- 🐍 Для Win7 + PySide6 авто-пиннинг PySide6<6.6 (последняя версия,
  совместимая с Python 3.8). Также: numpy<1.25, pandas<2.1.
- 🗄 Один скачанный портативный Python кэшируется и переиспользуется
  для всех будущих сборок.

Изменения 0.6.5:
- 🐍 Выбор Python-интерпретатора для сборки (Эксперт-настройки).
  Позволяет собрать EXE через ДРУГОЙ Python, не тот, в котором запущен
  сам сборщик. Главное применение — собрать через Python 3.8.10
  (последняя версия с поддержкой Windows 7) — итоговый exe запустится
  и на Win7, и на Win10/11. По умолчанию используется текущий Python.

Изменения 0.6.4:
- 🐛 Фикс мелькающих чёрных окон консоли при UPX-сжатии.
  При UPX PyInstaller вызывает upx.exe 80+ раз (по одному на каждый
  PYD/DLL), и каждый вызов открывал отдельную консоль на долю секунды.
  Теперь сам PyInstaller запускается с CREATE_NO_WINDOW / SW_HIDE —
  все дочерние процессы (upx, pip install и т.д.) наследуют скрытый
  режим. Сборка идёт молча.

Изменения 0.6.3:
- 🗜 UPX-сжатие (авто-скачивание, ВКЛ по умолчанию, exe ~1.5× меньше).

Изменения 0.6.2:
- 🐛 Фикс размера exe: убран лишний --collect-all PySide6.

Изменения 0.6.0–0.6.1:
- 🚀 Упрощённый UI с одной кнопкой «Сделать EXE».
- 📦 Авто-bundle ffmpeg по импортам.

Изменения 0.5.1:
- Кнопка «⬇ Скачать ffmpeg» (BtbN/FFmpeg-Builds release).

Изменения 0.5.0:
- 🌍 Универсальный EXE, 🐞 Отладочный EXE, 📦 Bundle ffmpeg.

Изменения 0.4.0:
- ⚡ Авто-оптимизация EXE (5–10× меньше размер).

Автор: RomzesPRA-2026.
"""

APP_VERSION = "0.8.2"
APP_NAME = "Py To EXE Builder"
APP_AUTHOR = "RomzesPRA-2026"

import ast
import importlib.metadata
import importlib.util
import json
import math
import os
import shutil
import platform
import struct
import subprocess
import sys
import sysconfig
import tempfile
import time
import hashlib
from html import escape as html_escape
import urllib.request
import zipfile
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QSettings, QSize, QRect, QPoint, QTimer
from PySide6.QtGui import (
    QPixmap, QPainter, QColor, QLinearGradient, QRadialGradient,
    QFont, QBrush, QPalette, QAction, QActionGroup, QGuiApplication, QIcon,
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QFileDialog,
    QMessageBox, QGroupBox, QPlainTextEdit, QScrollArea, QFrame, QDialog,
    QStyleFactory, QMenu, QToolButton, QProgressBar, QStyle, QLayout,
)


STDLIB_PATH = Path(sysconfig.get_paths().get("stdlib", "")).resolve()
SITE_PATHS = [Path(p).resolve() for p in sys.path if "site-packages" in p or "dist-packages" in p]


# ---------------- Стили / темы ----------------
SYSTEM_DEFAULT = "Системный по умолчанию"

CUSTOM_PALETTES = {
    "Fusion Light": {
        "Window": "#f0f0f0", "WindowText": "#202020",
        "Base": "#ffffff", "AlternateBase": "#e9e9e9",
        "Text": "#202020", "Button": "#e8e8e8", "ButtonText": "#202020",
        "Highlight": "#3874f2", "HighlightedText": "#ffffff",
        "ToolTipBase": "#ffffe1", "ToolTipText": "#202020",
        "PlaceholderText": "#888888", "Link": "#1e64ff",
    },
    "Fusion Dark": {
        "Window": "#2b2b2b", "WindowText": "#e6e6e6",
        "Base": "#1e1e1e", "AlternateBase": "#2a2a2a",
        "Text": "#e6e6e6", "Button": "#353535", "ButtonText": "#e6e6e6",
        "Highlight": "#2a82da", "HighlightedText": "#ffffff",
        "ToolTipBase": "#3a3a3a", "ToolTipText": "#e6e6e6",
        "PlaceholderText": "#888888", "Link": "#56a8ff",
    },
    "Solarized Light": {
        "Window": "#fdf6e3", "WindowText": "#073642",
        "Base": "#fffbf0", "AlternateBase": "#eee8d5",
        "Text": "#073642", "Button": "#eee8d5", "ButtonText": "#073642",
        "Highlight": "#268bd2", "HighlightedText": "#fdf6e3",
        "PlaceholderText": "#93a1a1", "Link": "#268bd2",
    },
    "Solarized Dark": {
        "Window": "#002b36", "WindowText": "#eee8d5",
        "Base": "#073642", "AlternateBase": "#0a3540",
        "Text": "#eee8d5", "Button": "#0e3a44", "ButtonText": "#eee8d5",
        "Highlight": "#268bd2", "HighlightedText": "#fdf6e3",
        "PlaceholderText": "#7a8e8e", "Link": "#2aa198",
    },
    "Nord": {
        "Window": "#2e3440", "WindowText": "#eceff4",
        "Base": "#3b4252", "AlternateBase": "#434c5e",
        "Text": "#eceff4", "Button": "#4c566a", "ButtonText": "#eceff4",
        "Highlight": "#88c0d0", "HighlightedText": "#2e3440",
        "PlaceholderText": "#8a93a3", "Link": "#81a1c1",
    },
    "Dracula": {
        "Window": "#282a36", "WindowText": "#f8f8f2",
        "Base": "#1e1f29", "AlternateBase": "#343746",
        "Text": "#f8f8f2", "Button": "#44475a", "ButtonText": "#f8f8f2",
        "Highlight": "#bd93f9", "HighlightedText": "#1e1f29",
        "PlaceholderText": "#8c8e9b", "Link": "#8be9fd",
    },
    "Monokai": {
        "Window": "#272822", "WindowText": "#f8f8f2",
        "Base": "#1d1e19", "AlternateBase": "#2f312a",
        "Text": "#f8f8f2", "Button": "#3e3d32", "ButtonText": "#f8f8f2",
        "Highlight": "#fd971f", "HighlightedText": "#272822",
        "PlaceholderText": "#90917f", "Link": "#a6e22e",
    },
    "High Contrast": {
        "Window": "#000000", "WindowText": "#ffffff",
        "Base": "#000000", "AlternateBase": "#1a1a1a",
        "Text": "#ffffff", "Button": "#101010", "ButtonText": "#ffffff",
        "Highlight": "#ffff00", "HighlightedText": "#000000",
        "PlaceholderText": "#bbbbbb", "Link": "#00e5ff",
    },
}


# ---------------- Современная тема (0.8.0) ----------------
MODERN_DARK = "Modern Dark (карточки)"
MODERN_LIGHT = "Modern Light (карточки)"

MODERN_THEMES = {
    MODERN_DARK: {
        "bg": "#15171c", "card": "#1d2027", "border": "#2a2e37", "input": "#12141a",
        "input_border": "#2f3440", "text": "#e6e8ec", "mute": "#8b93a1",
        "chip": "#252933", "chip_on_bg": "#1f3a2a", "chip_on_border": "#2f6b45",
        "chip_on_text": "#8fe0a8", "accent": "#5b7cfa", "accent2": "#8b5cf6",
        "log": "#0f1115", "hover": "#2a2f3a",
    },
    MODERN_LIGHT: {
        "bg": "#eef0f4", "card": "#ffffff", "border": "#dfe3ea", "input": "#f7f8fa",
        "input_border": "#d5dae3", "text": "#1c1f24", "mute": "#6b7280",
        "chip": "#f1f3f6", "chip_on_bg": "#e3f6ea", "chip_on_border": "#8fd3a8",
        "chip_on_text": "#17663a", "accent": "#4f6ef7", "accent2": "#7c4dff",
        "log": "#fafbfc", "hover": "#e8ebf0",
    },
}


def modern_qss(c):
    return f"""
QMainWindow, QDialog, QWidget#centralRoot {{ background: {c['bg']}; color: {c['text']}; }}
QToolTip {{ background: {c['card']}; color: {c['text']}; border: 1px solid {c['border']}; padding: 4px; }}
QLabel {{ color: {c['text']}; background: transparent; }}
QLabel#versionBadge {{ background: {c['chip']}; color: {c['mute']}; border-radius: 6px; padding: 1px 7px; }}
QLabel#statusLabel, QLabel#fieldLabel, QLabel#dropSub {{ color: {c['mute']}; }}
QLabel#caption {{ color: {c['mute']}; font-size: 8pt; font-weight: 600; letter-spacing: 1px; }}
QFrame#card {{ background: {c['card']}; border: 1px solid {c['border']}; border-radius: 12px; }}
QFrame#dropZone {{ background: transparent; border: 2px dashed {c['input_border']}; border-radius: 12px; }}
QFrame#dropZone:hover, QFrame#dropZone[hover="true"] {{ border-color: {c['accent']}; background: {c['hover']}; }}
QLabel#dropArrow {{ color: {c['mute']}; }}
QFrame#fileCard {{ background: {c['chip']}; border-radius: 9px; border: none; }}
QLabel#fileCardIcon {{ border-radius: 8px; background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #3776ab, stop:1 #ffd43b); }}
QLabel#iconPreview {{ background: {c['chip']}; border-radius: 10px; }}
QLineEdit, QComboBox, QPlainTextEdit {{
    background: {c['input']}; color: {c['text']}; border: 1px solid {c['input_border']};
    border-radius: 8px; padding: 5px 8px; selection-background-color: {c['accent']};
}}
QLineEdit:focus, QComboBox:focus {{ border-color: {c['accent']}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{ background: {c['card']}; color: {c['text']}; border: 1px solid {c['border']};
    selection-background-color: {c['accent']}; }}
QPlainTextEdit#logView {{ background: {c['log']}; border-color: {c['border']}; }}
QPushButton {{ background: {c['chip']}; color: {c['text']}; border: 1px solid {c['input_border']};
    border-radius: 8px; padding: 6px 12px; }}
QPushButton:hover {{ background: {c['hover']}; }}
QPushButton:disabled {{ color: {c['mute']}; }}
QPushButton#primaryBtn {{ color: #ffffff; border: none; border-radius: 12px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {c['accent']}, stop:1 {c['accent2']}); }}
QPushButton#primaryBtn:hover {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {c['accent2']}, stop:1 {c['accent']}); }}
QPushButton#primaryBtn:disabled {{ background: {c['hover']}; color: {c['mute']}; }}
QPushButton#ghostBtn {{ background: transparent; border-radius: 12px; padding: 0 16px; }}
QPushButton#ghostBtn:hover, QPushButton#ghostBtn:checked {{ background: {c['hover']}; }}
QPushButton#linkBtn {{ background: transparent; border: none; color: {c['mute']}; padding: 2px 6px; }}
QPushButton#linkBtn:hover {{ color: {c['text']}; }}
QToolButton#flatBtn, QToolButton#gearBtn {{ background: transparent; border: none; color: {c['mute']}; border-radius: 6px; }}
QToolButton#flatBtn:hover, QToolButton#gearBtn:hover {{ background: {c['hover']}; color: {c['text']}; }}
QToolButton#gearBtn::menu-indicator {{ image: none; width: 0; }}
QToolButton#iconTile {{ background: {c['chip']}; border: 1px solid transparent; border-radius: 8px; color: {c['text']}; }}
QToolButton#iconTile:hover {{ background: {c['hover']}; }}
QToolButton#iconTile:checked {{ border: 2px solid {c['accent']}; }}
QCheckBox {{ color: {c['text']}; spacing: 6px; }}
QCheckBox#chip {{ background: {c['chip']}; border: 1px solid {c['input_border']}; border-radius: 13px; padding: 4px 11px; }}
QCheckBox#chip:hover {{ background: {c['hover']}; }}
QCheckBox#chip:checked {{ background: {c['chip_on_bg']}; border-color: {c['chip_on_border']}; color: {c['chip_on_text']}; }}
QCheckBox#chip::indicator {{ width: 0; height: 0; }}
QGroupBox {{ background: {c['card']}; border: 1px solid {c['border']}; border-radius: 12px; margin-top: 14px; padding: 12px 10px 8px 10px; color: {c['text']}; }}
QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; color: {c['mute']}; }}
QProgressBar#buildProgress {{ background: {c['chip']}; border: none; border-radius: 2px; }}
QProgressBar#buildProgress::chunk {{ border-radius: 2px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {c['accent']}, stop:1 {c['accent2']}); }}
QMenu {{ background: {c['card']}; color: {c['text']}; border: 1px solid {c['border']}; padding: 4px; }}
QMenu::item {{ padding: 5px 18px; border-radius: 5px; }}
QMenu::item:selected {{ background: {c['accent']}; color: #ffffff; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {c['input_border']}; border-radius: 4px; min-height: 24px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {c['input_border']}; border-radius: 4px; min-width: 24px; }}
"""


def _modern_palette(c):
    pal = QPalette()
    for role, key in (("Window", "bg"), ("WindowText", "text"), ("Base", "input"),
                      ("AlternateBase", "card"), ("Text", "text"), ("Button", "chip"),
                      ("ButtonText", "text"), ("ToolTipBase", "card"), ("ToolTipText", "text"),
                      ("PlaceholderText", "mute"), ("Highlight", "accent")):
        pal.setColor(getattr(QPalette.ColorRole, role), QColor(c[key]))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    return pal


def apply_style(app, style_name, default_style_name, default_palette):
    """Применить выбранный стиль ко всему приложению."""
    # QSS современной темы снимаем при любом другом выборе.
    app.setStyleSheet("")
    if style_name in MODERN_THEMES:
        if "Fusion" in QStyleFactory.keys():
            app.setStyle("Fusion")
        c = MODERN_THEMES[style_name]
        app.setPalette(_modern_palette(c))
        app.setStyleSheet(modern_qss(c))
        return

    if style_name == SYSTEM_DEFAULT:
        if default_style_name:
            app.setStyle(default_style_name)
        app.setPalette(default_palette)
        return

    if style_name in QStyleFactory.keys():
        app.setStyle(style_name)
        app.setPalette(app.style().standardPalette())
        return

    if style_name in CUSTOM_PALETTES:
        if "Fusion" in QStyleFactory.keys():
            app.setStyle("Fusion")
        spec = CUSTOM_PALETTES[style_name]
        pal = QPalette()
        for role_name, hex_color in spec.items():
            try:
                role = getattr(QPalette.ColorRole, role_name)
            except AttributeError:
                continue
            pal.setColor(role, QColor(hex_color))
        base = QColor(spec.get("Window", "#888888"))
        pal.setColor(QPalette.ColorRole.Light,    base.lighter(130))
        pal.setColor(QPalette.ColorRole.Midlight, base.lighter(115))
        pal.setColor(QPalette.ColorRole.Mid,      base.darker(115))
        pal.setColor(QPalette.ColorRole.Dark,     base.darker(150))
        pal.setColor(QPalette.ColorRole.Shadow,   base.darker(200))
        app.setPalette(pal)


def app_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def project_output_dir(project_dir):
    return Path(project_dir).resolve() / "EXE_Output"


def project_workspace_dir(project_dir):
    return Path(project_dir).resolve() / "_py_to_exe_builder"


def fallback_output_dir():
    return app_base_dir() / "EXE_Output"


def fallback_workspace_dir():
    return app_base_dir() / "_py_to_exe_builder"


NO_BUILTIN_ICON = "Без встроенной иконки"

BUILTIN_ICONS = {
    "Python Blue": {"bg1": "#1d4ed8", "bg2": "#facc15", "fg": "#ffffff", "glyph": "py"},
    "Python Green": {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "py"},
    "App Window": {"bg1": "#0f172a", "bg2": "#38bdf8", "fg": "#ffffff", "glyph": "window"},
    "Console": {"bg1": "#111827", "bg2": "#4b5563", "fg": "#22c55e", "glyph": "terminal"},
    "Code Brackets": {"bg1": "#312e81", "bg2": "#a78bfa", "fg": "#ffffff", "glyph": "code"},
    "EXE Package": {"bg1": "#7c2d12", "bg2": "#fb923c", "fg": "#ffffff", "glyph": "package"},
    "Rocket": {"bg1": "#be123c", "bg2": "#fda4af", "fg": "#ffffff", "glyph": "rocket"},
    "Lightning": {"bg1": "#854d0e", "bg2": "#fde047", "fg": "#ffffff", "glyph": "bolt"},
    "Shield": {"bg1": "#064e3b", "bg2": "#34d399", "fg": "#ffffff", "glyph": "shield"},
    "Star": {"bg1": "#713f12", "bg2": "#facc15", "fg": "#ffffff", "glyph": "star"},
    "Gear": {"bg1": "#374151", "bg2": "#d1d5db", "fg": "#ffffff", "glyph": "gear"},
    "Robot": {"bg1": "#164e63", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "robot"},
    "Video": {"bg1": "#581c87", "bg2": "#d8b4fe", "fg": "#ffffff", "glyph": "video"},
    "Music": {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "music"},
    "Download": {"bg1": "#14532d", "bg2": "#4ade80", "fg": "#ffffff", "glyph": "download"},
    "Folder": {"bg1": "#92400e", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "folder"},
    "Magic Wand": {"bg1": "#4c1d95", "bg2": "#c084fc", "fg": "#ffffff", "glyph": "magic"},
    "Cloud": {"bg1": "#075985", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "cloud"},
    "Fire": {"bg1": "#991b1b", "bg2": "#fb923c", "fg": "#ffffff", "glyph": "fire"},
    "Cube": {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "cube"},
    "Database": {"bg1": "#134e4a", "bg2": "#5eead4", "fg": "#ffffff", "glyph": "database"},
    "Lock": {"bg1": "#3f3f46", "bg2": "#a1a1aa", "fg": "#ffffff", "glyph": "lock"},
    "Key": {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "key"},
    "Camera": {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "camera"},
    "Image": {"bg1": "#166534", "bg2": "#86efac", "fg": "#ffffff", "glyph": "image"},
    "Book": {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "book"},
    "Wrench": {"bg1": "#0c4a6e", "bg2": "#38bdf8", "fg": "#ffffff", "glyph": "wrench"},
    "Globe": {"bg1": "#1e40af", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "globe"},
    "Heart": {"bg1": "#9f1239", "bg2": "#fb7185", "fg": "#ffffff", "glyph": "heart"},
    "Check": {"bg1": "#166534", "bg2": "#22c55e", "fg": "#ffffff", "glyph": "check"},
    "Cross": {"bg1": "#7f1d1d", "bg2": "#ef4444", "fg": "#ffffff", "glyph": "cross"},
    "Plus": {"bg1": "#0369a1", "bg2": "#38bdf8", "fg": "#ffffff", "glyph": "plus"},
    "Gamepad": {"bg1": "#172554", "bg2": "#818cf8", "fg": "#ffffff", "glyph": "gamepad"},
    "Bug": {"bg1": "#365314", "bg2": "#bef264", "fg": "#ffffff", "glyph": "bug"},
    "Browser": {"bg1": "#4338ca", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "browser"},
    "Wave": {"bg1": "#155e75", "bg2": "#22d3ee", "fg": "#ffffff", "glyph": "wave"},
    "Diamond": {"bg1": "#581c87", "bg2": "#e879f9", "fg": "#ffffff", "glyph": "diamond"},
    "Play": {"bg1": "#166534", "bg2": "#86efac", "fg": "#ffffff", "glyph": "play"},
    "Pause": {"bg1": "#7c2d12", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "pause"},
    "Stop": {"bg1": "#7f1d1d", "bg2": "#f87171", "fg": "#ffffff", "glyph": "stop"},
    "Upload": {"bg1": "#3730a3", "bg2": "#818cf8", "fg": "#ffffff", "glyph": "upload"},
    "Scissors": {"bg1": "#334155", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "scissors"},
    "Terminal Green": {"bg1": "#052e16", "bg2": "#22c55e", "fg": "#ffffff", "glyph": "terminal"},
    "Installer": {"bg1": "#0f766e", "bg2": "#99f6e4", "fg": "#ffffff", "glyph": "download"},
    "Analyzer": {"bg1": "#312e81", "bg2": "#c4b5fd", "fg": "#ffffff", "glyph": "search"},
    "Builder": {"bg1": "#78350f", "bg2": "#fcd34d", "fg": "#ffffff", "glyph": "wrench"},
    "Clean": {"bg1": "#075985", "bg2": "#bae6fd", "fg": "#ffffff", "glyph": "spark"},
    "Portable": {"bg1": "#4a044e", "bg2": "#f0abfc", "fg": "#ffffff", "glyph": "package"},

    # --- New in 0.3.0 ---
    "Sun": {"bg1": "#b45309", "bg2": "#fde047", "fg": "#ffffff", "glyph": "sun"},
    "Moon": {"bg1": "#1e1b4b", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "moon"},
    "Snowflake": {"bg1": "#0c4a6e", "bg2": "#bae6fd", "fg": "#ffffff", "glyph": "snowflake"},
    "Leaf": {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "leaf"},
    "Tree": {"bg1": "#064e3b", "bg2": "#34d399", "fg": "#ffffff", "glyph": "tree"},
    "Flower": {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "flower"},
    "Coffee": {"bg1": "#451a03", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "coffee"},
    "Pizza": {"bg1": "#7c2d12", "bg2": "#fde047", "fg": "#ffffff", "glyph": "pizza"},
    "Headphones": {"bg1": "#1e1b4b", "bg2": "#c4b5fd", "fg": "#ffffff", "glyph": "headphones"},
    "Microphone": {"bg1": "#3f3f46", "bg2": "#a1a1aa", "fg": "#ffffff", "glyph": "microphone"},
    "Phone": {"bg1": "#0f766e", "bg2": "#5eead4", "fg": "#ffffff", "glyph": "phone"},
    "Mail": {"bg1": "#1d4ed8", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "mail"},
    "Bell": {"bg1": "#a16207", "bg2": "#fde047", "fg": "#ffffff", "glyph": "bell"},
    "Calendar": {"bg1": "#7e22ce", "bg2": "#d8b4fe", "fg": "#ffffff", "glyph": "calendar"},
    "Clock": {"bg1": "#0f172a", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "clock"},
    "Flag": {"bg1": "#991b1b", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "flag"},
    "Tag": {"bg1": "#9a3412", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "tag"},
    "Bookmark": {"bg1": "#7f1d1d", "bg2": "#fda4af", "fg": "#ffffff", "glyph": "bookmark"},
    "Filter": {"bg1": "#374151", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "filter"},
    "Refresh": {"bg1": "#075985", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "refresh"},
    "Eye": {"bg1": "#312e81", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "eye"},
    "Trophy": {"bg1": "#92400e", "bg2": "#fde047", "fg": "#ffffff", "glyph": "trophy"},
    "Medal": {"bg1": "#a16207", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "medal"},
    "Crown": {"bg1": "#7c2d12", "bg2": "#facc15", "fg": "#ffffff", "glyph": "crown"},
    "Gift": {"bg1": "#9f1239", "bg2": "#fda4af", "fg": "#ffffff", "glyph": "gift"},
    "Cart": {"bg1": "#1e40af", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "cart"},
    "Monitor": {"bg1": "#1e293b", "bg2": "#64748b", "fg": "#ffffff", "glyph": "monitor"},
    "Keyboard": {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "keyboard"},
    "Mouse": {"bg1": "#334155", "bg2": "#cbd5e1", "fg": "#ffffff", "glyph": "mouse"},
    "CPU": {"bg1": "#0c4a6e", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "cpu"},
    "HDD": {"bg1": "#1e293b", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "hdd"},
    "USB": {"bg1": "#365314", "bg2": "#bef264", "fg": "#ffffff", "glyph": "usb"},
    "Car": {"bg1": "#7c2d12", "bg2": "#fb923c", "fg": "#ffffff", "glyph": "car"},
    "Plane": {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "plane"},
    "Ship": {"bg1": "#155e75", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "ship"},
    "Brush": {"bg1": "#5b21b6", "bg2": "#c4b5fd", "fg": "#ffffff", "glyph": "brush"},
    "Pencil": {"bg1": "#a16207", "bg2": "#fde047", "fg": "#ffffff", "glyph": "pencil"},
    "Calculator": {"bg1": "#1f2937", "bg2": "#a1a1aa", "fg": "#ffffff", "glyph": "calculator"},
    "Atom": {"bg1": "#1e3a8a", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "atom"},
    "Flask": {"bg1": "#155e75", "bg2": "#5eead4", "fg": "#ffffff", "glyph": "flask"},
    "Bulb": {"bg1": "#a16207", "bg2": "#fef08a", "fg": "#ffffff", "glyph": "bulb"},
    "Speaker": {"bg1": "#3f3f46", "bg2": "#a1a1aa", "fg": "#ffffff", "glyph": "speaker"},
    "Map Pin": {"bg1": "#9f1239", "bg2": "#fda4af", "fg": "#ffffff", "glyph": "pin"},
    "Wifi": {"bg1": "#075985", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "wifi"},
    "Battery": {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "battery"},
    "Hammer": {"bg1": "#78350f", "bg2": "#fcd34d", "fg": "#ffffff", "glyph": "hammer"},

    # --- Спорт ---
    "Soccer Ball": {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "ball"},
    "Basketball": {"bg1": "#9a3412", "bg2": "#fb923c", "fg": "#ffffff", "glyph": "basketball"},
    "Tennis": {"bg1": "#365314", "bg2": "#bef264", "fg": "#ffffff", "glyph": "tennis"},
    "Target": {"bg1": "#7f1d1d", "bg2": "#fecaca", "fg": "#ffffff", "glyph": "target"},
    "Dumbbell": {"bg1": "#374151", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "dumbbell"},

    # --- Природа ---
    "Mountain": {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "mountain"},
    "Ocean": {"bg1": "#0c4a6e", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "ocean"},
    "Rainbow": {"bg1": "#581c87", "bg2": "#fde047", "fg": "#ffffff", "glyph": "rainbow"},
    "Drop": {"bg1": "#075985", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "drop"},
    "Mushroom": {"bg1": "#7f1d1d", "bg2": "#fecaca", "fg": "#ffffff", "glyph": "mushroom"},

    # --- Транспорт ---
    "Bus": {"bg1": "#a16207", "bg2": "#fde047", "fg": "#ffffff", "glyph": "bus"},
    "Train": {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "train"},
    "Bicycle": {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "bicycle"},
    "Taxi": {"bg1": "#a16207", "bg2": "#facc15", "fg": "#ffffff", "glyph": "taxi"},

    # --- Еда / напитки ---
    "Burger": {"bg1": "#7c2d12", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "burger"},
    "Donut": {"bg1": "#9f1239", "bg2": "#fda4af", "fg": "#ffffff", "glyph": "donut"},
    "Apple Fruit": {"bg1": "#7f1d1d", "bg2": "#f87171", "fg": "#ffffff", "glyph": "apple"},
    "Ice Cream": {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "icecream"},
    "Bottle": {"bg1": "#075985", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "bottle"},

    # --- Технологии ---
    "Brain": {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "brain"},
    "Server": {"bg1": "#1e293b", "bg2": "#64748b", "fg": "#ffffff", "glyph": "server"},
    "Network": {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "network"},
    "Chip": {"bg1": "#312e81", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "chip"},

    # --- Финансы ---
    "Dollar": {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "dollar"},
    "Coin": {"bg1": "#a16207", "bg2": "#fde047", "fg": "#ffffff", "glyph": "coin"},
    "Wallet": {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "wallet"},
    "Bank": {"bg1": "#1e293b", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "bank"},

    # --- Здоровье ---
    "Pill": {"bg1": "#7e22ce", "bg2": "#d8b4fe", "fg": "#ffffff", "glyph": "pill"},
    "Medical Cross": {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "medcross"},

    # --- Стрелки ---
    "Arrow Up": {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "arrow_up"},
    "Arrow Down": {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "arrow_down"},
    "Arrow Left": {"bg1": "#92400e", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "arrow_left"},
    "Arrow Right": {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "arrow_right"},

    # --- Фигуры ---
    "Triangle": {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "triangle"},
    "Hexagon": {"bg1": "#0f766e", "bg2": "#5eead4", "fg": "#ffffff", "glyph": "hexagon"},
    "Ring": {"bg1": "#4c1d95", "bg2": "#c084fc", "fg": "#ffffff", "glyph": "ring"},
    "Square": {"bg1": "#0c4a6e", "bg2": "#38bdf8", "fg": "#ffffff", "glyph": "square_filled"},

    # --- Дом / повседневное ---
    "Home": {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "home"},
    "Door": {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "door"},
    "Key 2": {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "key2"},
    "Lightning Bolt 2": {"bg1": "#1e1b4b", "bg2": "#fde047", "fg": "#ffffff", "glyph": "bolt2"},

    # --- Образование / разное ---
    "Graduation Cap": {"bg1": "#0f172a", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "graduation"},
    "Dice": {"bg1": "#7f1d1d", "bg2": "#fecaca", "fg": "#ffffff", "glyph": "dice"},
    "Infinity": {"bg1": "#4c1d95", "bg2": "#c084fc", "fg": "#ffffff", "glyph": "infinity"},
    "Question": {"bg1": "#1e293b", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "question"},
    "Exclaim": {"bg1": "#7c2d12", "bg2": "#fb923c", "fg": "#ffffff", "glyph": "exclaim"},
    "Compass": {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "compass"},

    # --- Цветовые варианты ---
    "Star Red":     {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "star"},
    "Star Blue":    {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "star"},
    "Star Pink":    {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "star"},
    "Heart Purple": {"bg1": "#4c1d95", "bg2": "#c4b5fd", "fg": "#ffffff", "glyph": "heart"},
    "Heart Blue":   {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "heart"},
    "Rocket Cyan":  {"bg1": "#0c4a6e", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "rocket"},
    "Rocket Green": {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "rocket"},
    "Folder Blue":  {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "folder"},
    "Folder Red":   {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "folder"},
    "Gear Orange":  {"bg1": "#7c2d12", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "gear"},
    "Gear Cyan":    {"bg1": "#155e75", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "gear"},
    "Fire Blue":    {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "fire"},
    "Fire Purple":  {"bg1": "#581c87", "bg2": "#d8b4fe", "fg": "#ffffff", "glyph": "fire"},
    "Diamond Green":{"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "diamond"},
    "Diamond Gold": {"bg1": "#78350f", "bg2": "#facc15", "fg": "#ffffff", "glyph": "diamond"},
    "Cloud Pink":   {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "cloud"},
    "Lock Green":   {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "lock"},
    "Bell Red":     {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "bell"},

    # --- 0.4.0: Технологии и наука ---
    "AI Chip":      {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "ai_chip"},
    "Bot":          {"bg1": "#155e75", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "bot"},
    "QR Code":      {"bg1": "#0f172a", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "qrcode"},
    "Bar Code":     {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "barcode"},
    "Antenna":      {"bg1": "#075985", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "antenna"},
    "Satellite":    {"bg1": "#1e1b4b", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "satellite"},
    "Microscope":   {"bg1": "#0f766e", "bg2": "#5eead4", "fg": "#ffffff", "glyph": "microscope"},
    "Telescope":    {"bg1": "#1e3a8a", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "telescope"},
    "Magnet":       {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "magnet"},

    # --- 0.4.0: Погода / природа ---
    "Cloud Rain":   {"bg1": "#075985", "bg2": "#bae6fd", "fg": "#ffffff", "glyph": "cloud_rain"},
    "Cloud Snow":   {"bg1": "#0c4a6e", "bg2": "#e0f2fe", "fg": "#ffffff", "glyph": "cloud_snow"},
    "Sun Cloud":    {"bg1": "#a16207", "bg2": "#fde047", "fg": "#ffffff", "glyph": "sun_cloud"},
    "Wind":         {"bg1": "#475569", "bg2": "#cbd5e1", "fg": "#ffffff", "glyph": "wind"},
    "Tornado":      {"bg1": "#1e293b", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "tornado"},
    "Palm Tree":    {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "palm"},
    "Cactus":       {"bg1": "#365314", "bg2": "#bef264", "fg": "#ffffff", "glyph": "cactus"},
    "Pine Tree":    {"bg1": "#064e3b", "bg2": "#34d399", "fg": "#ffffff", "glyph": "pine"},
    "Footprint":    {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "footprint"},

    # --- 0.4.0: Анималы ---
    "Cat":          {"bg1": "#3f3f46", "bg2": "#a1a1aa", "fg": "#ffffff", "glyph": "cat"},
    "Dog":          {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "dog"},
    "Fish":         {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "fish"},
    "Bird":         {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "bird"},
    "Paw":          {"bg1": "#7c2d12", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "paw"},

    # --- 0.4.0: Эмодзи-стиль ---
    "Smile":        {"bg1": "#a16207", "bg2": "#fde047", "fg": "#000000", "glyph": "smile"},
    "Sad":          {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#000000", "glyph": "sad"},
    "Wink":         {"bg1": "#a16207", "bg2": "#fde047", "fg": "#000000", "glyph": "wink"},
    "Cool":         {"bg1": "#0c4a6e", "bg2": "#67e8f9", "fg": "#000000", "glyph": "cool"},

    # --- 0.4.0: Музыка и медиа ---
    "Notes":        {"bg1": "#581c87", "bg2": "#d8b4fe", "fg": "#ffffff", "glyph": "notes"},
    "Drum":         {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "drum"},
    "Guitar":       {"bg1": "#7c2d12", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "guitar"},
    "Vinyl":        {"bg1": "#111827", "bg2": "#4b5563", "fg": "#ffffff", "glyph": "vinyl"},
    "Film":         {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "film"},

    # --- 0.4.0: Дополнительные технологии ---
    "Print":        {"bg1": "#475569", "bg2": "#cbd5e1", "fg": "#ffffff", "glyph": "print"},
    "Scan":         {"bg1": "#0f172a", "bg2": "#64748b", "fg": "#ffffff", "glyph": "scan"},
    "Fax":          {"bg1": "#374151", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "fax"},
    "Drone":        {"bg1": "#1e293b", "bg2": "#64748b", "fg": "#ffffff", "glyph": "drone"},

    # --- 0.4.0: Соцсети / общение ---
    "Chat":         {"bg1": "#0f766e", "bg2": "#5eead4", "fg": "#ffffff", "glyph": "chat"},
    "Chat 2":       {"bg1": "#1e40af", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "chat2"},
    "Hashtag":      {"bg1": "#0c4a6e", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "hashtag"},
    "At Sign":      {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#ffffff", "glyph": "at"},
    "Share":        {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "share"},
    "Thumbs Up":    {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "thumbsup"},
    "Thumbs Down":  {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "thumbsdown"},

    # --- 0.4.0: Универсальные ---
    "Three Dots":   {"bg1": "#374151", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "dots3"},
    "Menu":         {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "menu_lines"},
    "Grid":         {"bg1": "#374151", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "grid"},
    "List":         {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "list"},
    "Layers":       {"bg1": "#312e81", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "layers"},
    "Sliders":      {"bg1": "#374151", "bg2": "#cbd5e1", "fg": "#ffffff", "glyph": "sliders"},

    # --- 0.4.0: Минимализм / геометрия ---
    "Circle":       {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "circle_filled"},
    "Half Moon":    {"bg1": "#111827", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "halfmoon"},
    "Yin Yang":     {"bg1": "#1f2937", "bg2": "#e5e7eb", "fg": "#ffffff", "glyph": "yinyang"},
    "Plus Circle":  {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "plus_circle"},
    "Minus Circle": {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "minus_circle"},

    # --- 0.4.0: Файлы ---
    "File":         {"bg1": "#1e293b", "bg2": "#94a3b8", "fg": "#ffffff", "glyph": "file"},
    "File Plus":    {"bg1": "#15803d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "file_plus"},
    "File Code":    {"bg1": "#1e3a8a", "bg2": "#60a5fa", "fg": "#ffffff", "glyph": "file_code"},
    "File ZIP":     {"bg1": "#78350f", "bg2": "#fbbf24", "fg": "#ffffff", "glyph": "file_zip"},

    # --- 0.4.0: Расширенные цветовые серии ---
    "Cube Red":     {"bg1": "#7f1d1d", "bg2": "#fca5a5", "fg": "#ffffff", "glyph": "cube"},
    "Cube Green":   {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ffffff", "glyph": "cube"},
    "Shield Blue":  {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "shield"},
    "Shield Gold":  {"bg1": "#78350f", "bg2": "#facc15", "fg": "#ffffff", "glyph": "shield"},
    "Lightning Pink":{"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#ffffff", "glyph": "bolt"},
    "Crown Silver": {"bg1": "#3f3f46", "bg2": "#d4d4d8", "fg": "#ffffff", "glyph": "crown"},

    # --- 0.7.9: новые глифы ---
    "Anchor":       {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ffffff", "glyph": "anchor"},
    "Umbrella":     {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#f87171", "glyph": "umbrella"},
    "Hourglass":    {"bg1": "#78350f", "bg2": "#fcd34d", "fg": "#ffffff", "glyph": "hourglass"},
    "Puzzle":       {"bg1": "#166534", "bg2": "#86efac", "fg": "#ffffff", "glyph": "puzzle"},
    "Planet":       {"bg1": "#1e1b4b", "bg2": "#6366f1", "fg": "#fb923c", "glyph": "planet"},
    "UFO":          {"bg1": "#111827", "bg2": "#4b5563", "fg": "#a1a1aa", "glyph": "ufo"},
    "Gem":          {"bg1": "#0f766e", "bg2": "#5eead4", "fg": "#a7f3d0", "glyph": "gem"},
    "Megaphone":    {"bg1": "#9a3412", "bg2": "#fdba74", "fg": "#ffffff", "glyph": "megaphone"},
    "Power":        {"bg1": "#1f2937", "bg2": "#4b5563", "fg": "#4ade80", "glyph": "power"},
    "Signal Bars":  {"bg1": "#0c4a6e", "bg2": "#38bdf8", "fg": "#ffffff", "glyph": "signal"},
    "Bar Chart":    {"bg1": "#312e81", "bg2": "#a5b4fc", "fg": "#ffffff", "glyph": "chart_bars"},
    "Line Chart":   {"bg1": "#064e3b", "bg2": "#34d399", "fg": "#ffffff", "glyph": "chart_line"},
    "Pie Chart":    {"bg1": "#7c2d12", "bg2": "#fb923c", "fg": "#ffffff", "glyph": "chart_pie"},
    "Chain Link":   {"bg1": "#374151", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "chain"},
    "Sword":        {"bg1": "#1e293b", "bg2": "#64748b", "fg": "#e2e8f0", "glyph": "sword"},
    "Potion":       {"bg1": "#4a044e", "bg2": "#f0abfc", "fg": "#e9d5ff", "glyph": "potion"},
    "Joystick":     {"bg1": "#172554", "bg2": "#818cf8", "fg": "#ffffff", "glyph": "joystick"},
    "Moon & Star":  {"bg1": "#0f172a", "bg2": "#1e3a8a", "fg": "#fde68a", "glyph": "moon_star"},
    "Cursor":       {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#ffffff", "glyph": "cursor"},
    "Storm":        {"bg1": "#1e293b", "bg2": "#475569", "fg": "#cbd5e1", "glyph": "cloud_bolt"},
    "Hex Nut":      {"bg1": "#3f3f46", "bg2": "#a1a1aa", "fg": "#d4d4d8", "glyph": "hexnut"},
    "Radar":        {"bg1": "#052e16", "bg2": "#166534", "fg": "#4ade80", "glyph": "radar"},

    # --- 0.7.16: новые виды ---
    "Two Hearts":   {"bg1": "#9f1239", "bg2": "#fda4af", "fg": "#ffffff", "glyph": "hearts"},
    "Broken Heart": {"bg1": "#7f1d1d", "bg2": "#fb7185", "fg": "#ffffff", "glyph": "broken_heart"},
    "Valentine":    {"bg1": "#831843", "bg2": "#f9a8d4", "fg": "#fdf2f8", "glyph": "valentine"},
    "Butterfly":    {"bg1": "#4c1d95", "bg2": "#c084fc", "fg": "#e9d5ff", "glyph": "butterfly"},
    "Clover":       {"bg1": "#14532d", "bg2": "#86efac", "fg": "#22c55e", "glyph": "clover"},
    "Candle":       {"bg1": "#431407", "bg2": "#fdba74", "fg": "#fef3c7", "glyph": "candle"},
    "Balloon":      {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#ef4444", "glyph": "balloon"},
    "Cake":         {"bg1": "#831843", "bg2": "#fbcfe8", "fg": "#f472b6", "glyph": "cake"},
    "Tulip":        {"bg1": "#14532d", "bg2": "#bbf7d0", "fg": "#f43f5e", "glyph": "tulip"},
    "Snowman":      {"bg1": "#0c4a6e", "bg2": "#bae6fd", "fg": "#ffffff", "glyph": "snowman"},
    "Kite":         {"bg1": "#1e3a8a", "bg2": "#93c5fd", "fg": "#f59e0b", "glyph": "kite"},
    "Bee":          {"bg1": "#365314", "bg2": "#bef264", "fg": "#facc15", "glyph": "bee"},
    "Ladybug":      {"bg1": "#14532d", "bg2": "#86efac", "fg": "#ef4444", "glyph": "ladybug"},
    "Turtle":       {"bg1": "#064e3b", "bg2": "#6ee7b7", "fg": "#34d399", "glyph": "turtle"},
    "Rabbit":       {"bg1": "#57534e", "bg2": "#e7e5e4", "fg": "#fafaf9", "glyph": "rabbit"},
    "Duck":         {"bg1": "#0c4a6e", "bg2": "#7dd3fc", "fg": "#fde047", "glyph": "duck"},
    "Penguin":      {"bg1": "#0f172a", "bg2": "#94a3b8", "fg": "#1e293b", "glyph": "penguin"},
    "Glasses":      {"bg1": "#1f2937", "bg2": "#9ca3af", "fg": "#e5e7eb", "glyph": "glasses"},
    "T-Shirt":      {"bg1": "#155e75", "bg2": "#67e8f9", "fg": "#ffffff", "glyph": "tshirt"},
    "Ring Gold":    {"bg1": "#78350f", "bg2": "#fde68a", "fg": "#fbbf24", "glyph": "ring_gem"},
    "Crystal Ball": {"bg1": "#312e81", "bg2": "#a5b4fc", "fg": "#6366f1", "glyph": "crystal_ball"},
    "Top Hat":      {"bg1": "#3f3f46", "bg2": "#d4d4d8", "fg": "#18181b", "glyph": "tophat"},
}


# ----------------------- Логика анализа импортов (без изменений) -----------------------
def is_relative_to(path, parent):
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def read_python_imports(file_path):
    """Возвращает (top_level_imports, dotted_imports).
    dotted — полные пути типа 'PySide6.QtCore', 'PySide6.QtGui.QPalette'.
    """
    tops = set()
    dotted = set()
    try:
        tree = ast.parse(Path(file_path).read_text(encoding="utf-8-sig", errors="ignore"))
    except Exception:
        return tops, dotted

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.strip()
                if not name:
                    continue
                tops.add(name.split(".")[0])
                dotted.add(name)
        elif isinstance(node, ast.ImportFrom):
            # Относительные импорты (from .foo import bar) — это внутрипакетные,
            # их top-level не должен попадать в внешние зависимости.
            if node.level and node.level > 0:
                continue
            if not node.module:
                continue
            module = node.module.strip()
            tops.add(module.split(".")[0])
            dotted.add(module)
            for alias in node.names:
                if alias.name and alias.name != "*":
                    dotted.add(f"{module}.{alias.name}")
    return tops, dotted


def _inside_python_install(path):
    """True, если path лежит в Lib/Scripts/Include НАСТОЯЩЕГО Python/venv
    (рядом с папкой есть python.exe или pyvenv.cfg). Обычные папки проекта
    с такими именами не считаются."""
    for parent in path.parents:
        if parent.name in ("Lib", "Scripts", "Include"):
            root = parent.parent
            try:
                if (root / "python.exe").exists() or (root / "pyvenv.cfg").exists():
                    return True
            except OSError:
                pass
    return False


# Лимит файлов при анализе (защита от выбора корня диска и т.п.).
MAX_SCAN_PY_FILES = 5000


def collect_project_imports(project_dir):
    """Возвращает (top_imports, dotted_imports, py_files).
    Обход через os.walk: служебные папки отсекаются ОТНОСИТЕЛЬНО проекта
    (раньше проверялся абсолютный путь → проект в D:\\dist\\app давал 0 импортов)."""
    tops = set()
    dotted = set()
    py_files = []
    skip_dirs = {
        "__pycache__", ".git", ".hg", ".svn", ".venv", "venv", "env",
        "build", "dist", ".idea", ".vscode", "node_modules",
        # Рабочие папки самого сборщика — НЕ сканируем их рекурсивно,
        # иначе анализатор попадает в yt_dlp.extractor (1500 файлов) и т.п.
        "_portable_pythons", "_py_to_exe_builder", "EXE_Output",
        "site-packages",
    }
    for root, dirnames, filenames in os.walk(project_dir):
        root_p = Path(root)
        # Lib/Scripts/Include пропускаем только внутри реального Python/venv.
        dirnames[:] = [
            d for d in dirnames
            if d not in skip_dirs and not _inside_python_install(root_p / d / "x")
        ]
        for fn in filenames:
            if Path(fn).suffix.lower() not in {".py", ".pyw"}:
                continue
            path = root_p / fn
            py_files.append(path)
            t, d = read_python_imports(path)
            tops.update(t)
            dotted.update(d)
            if len(py_files) >= MAX_SCAN_PY_FILES:
                return tops, dotted, py_files
    return tops, dotted, py_files


def local_module_names(project_dir, extra_dirs=()):
    """Локальные модули: верхний уровень проекта, папка src/ и доп. папки
    (например, папка главного файла)."""
    names = set()
    project_dir = Path(project_dir)
    bases = [project_dir, project_dir / "src", *[Path(x) for x in extra_dirs]]
    for base in bases:
        try:
            items = list(base.iterdir())
        except Exception:
            continue
        for path in items:
            if path.name.startswith("."):
                continue
            if path.is_file() and path.suffix.lower() in {".py", ".pyw"}:
                names.add(path.stem)
            elif path.is_dir() and (path / "__init__.py").exists():
                names.add(path.name)
    return names


def classify_import(name, project_dir, local_names=None):
    if name in sys.builtin_module_names:
        return "stdlib"
    if local_names is None:
        local_names = local_module_names(project_dir)
    if name in local_names:
        return "local"
    try:
        spec = importlib.util.find_spec(name)
    except Exception:
        return "unknown"
    if spec is None:
        return "unknown"

    origin = getattr(spec, "origin", "") or ""
    locations = getattr(spec, "submodule_search_locations", None)

    paths = []
    if origin and origin not in {"built-in", "frozen"}:
        paths.append(Path(origin))
    if locations:
        paths.extend(Path(x) for x in locations)

    if origin in {"built-in", "frozen"}:
        return "stdlib"

    for p in paths:
        try:
            rp = p.resolve()
        except Exception:
            continue
        if is_relative_to(rp, Path(project_dir)):
            return "local"
        if any(is_relative_to(rp, site) for site in SITE_PATHS):
            return "third-party"
        if STDLIB_PATH and is_relative_to(rp, STDLIB_PATH):
            return "stdlib"

    return "third-party"


_PKG_DISTS_CACHE = None


def _packages_distributions():
    """Кэш packages_distributions(): полный обход дистрибутивов — дорогой."""
    global _PKG_DISTS_CACHE
    if _PKG_DISTS_CACHE is None:
        try:
            _PKG_DISTS_CACHE = importlib.metadata.packages_distributions()
        except Exception:
            _PKG_DISTS_CACHE = {}
    return _PKG_DISTS_CACHE


def package_version(import_name):
    packages = _packages_distributions()
    dist_names = packages.get(import_name, [])
    if not dist_names:
        return None
    for dist_name in dist_names:
        try:
            version = importlib.metadata.version(dist_name)
            return f"{dist_name}=={version}"
        except Exception:
            continue
    return dist_names[0]


# ----------------------- Генерация .ico (растровая, без зависимостей) -----------------------
def hex_to_rgb(value):
    value = value.strip().lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def blend(c1, c2, t):
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))


# Стили фона иконок:
#   gradient — диагональный градиент + блик (классика, по умолчанию)
#   flat     — сплошной цвет bg1
#   vgrad    — вертикальный градиент bg1→bg2
#   radial   — радиальный: яркий bg2 в центре → bg1 к краям
#   split    — двухцветный диагональный срез bg1|bg2
#   circle   — круглый бейдж (углы прозрачные), внутри градиент
#   rounded  — скруглённый квадрат (углы прозрачные), внутри градиент
#   neon     — почти чёрный фон, глиф в ярком акценте (из bg2) + свечение
ICON_STYLES = ("gradient", "flat", "vgrad", "radial", "split", "circle", "rounded", "neon")

# Человекочитаемые метки стилей для UI. Пустой ключ = «не переопределять»
# (используется стиль, зашитый в пресете; у большинства это gradient).
ICON_STYLE_LABELS = {
    "":         "Как в пресете",
    "gradient": "Градиент (классика)",
    "flat":     "Плоский",
    "vgrad":    "Вертикальный градиент",
    "radial":   "Радиальный",
    "split":    "Двухцветный срез",
    "circle":   "Круглый бейдж",
    "rounded":  "Скруглённый квадрат",
    "neon":     "💡 Неон (свечение)",
}


def _neon_accent(c):
    """«Разгоняет» цвет до максимальной яркости (неоновый акцент)."""
    m = max(c) or 1
    return tuple(min(255, v * 255 // m) for v in c)


# Русские ключевые слова для поиска иконок (glyph → слова).
# «сердечко» найдёт heart, «машина» — car и т.д.
RU_GLYPH_KEYWORDS = {
    "py": "питон python пай",
    "heart": "сердце сердечко любовь",
    "hearts": "сердце сердечко сердечки два сердца любовь",
    "broken_heart": "разбитое сердце сердечко",
    "valentine": "валентинка письмо любовь конверт сердечко",
    "star": "звезда звездочка звёздочка",
    "sun": "солнце солнышко", "moon": "луна месяц", "moon_star": "луна месяц ночь звезда",
    "cloud": "облако туча", "cloud_rain": "дождь туча", "cloud_snow": "снег туча",
    "cloud_bolt": "гроза молния туча шторм", "sun_cloud": "погода облачно",
    "snowflake": "снежинка снег", "rainbow": "радуга", "drop": "капля вода",
    "wind": "ветер", "tornado": "торнадо смерч", "mountain": "гора горы",
    "ocean": "море океан волны", "palm": "пальма", "cactus": "кактус",
    "pine": "ёлка елка сосна", "tree": "дерево", "leaf": "лист листик",
    "flower": "цветок цветочек", "tulip": "тюльпан цветок", "mushroom": "гриб",
    "clover": "клевер удача", "butterfly": "бабочка", "bee": "пчела оса",
    "ladybug": "божья коровка жук", "turtle": "черепаха", "rabbit": "заяц кролик",
    "duck": "утка уточка", "penguin": "пингвин", "cat": "кот кошка котик",
    "dog": "собака пёс песик", "fish": "рыба рыбка", "bird": "птица птичка",
    "paw": "лапа лапка след", "footprint": "след следы",
    "rocket": "ракета запуск", "bolt": "молния", "bolt2": "молния",
    "fire": "огонь пламя", "gear": "шестерня шестеренка настройки",
    "wrench": "гаечный ключ инструмент", "hammer": "молоток",
    "shield": "щит защита", "lock": "замок", "key": "ключ", "key2": "ключ",
    "check": "галочка готово да", "cross": "крест нет отмена",
    "plus": "плюс добавить", "plus_circle": "плюс", "minus_circle": "минус",
    "folder": "папка", "file": "файл документ", "file_plus": "новый файл",
    "file_code": "файл код", "file_zip": "архив zip",
    "terminal": "терминал консоль", "code": "код скобки программирование",
    "window": "окно", "browser": "браузер", "package": "коробка пакет",
    "download": "скачать загрузка", "upload": "выгрузка отправить",
    "camera": "камера фотоаппарат фото", "image": "картинка фото изображение",
    "video": "видео", "film": "фильм кино", "music": "музыка нота",
    "notes": "ноты музыка", "microphone": "микрофон", "headphones": "наушники",
    "speaker": "динамик звук колонка", "drum": "барабан", "guitar": "гитара",
    "vinyl": "пластинка диск", "play": "плей пуск", "pause": "пауза",
    "stop": "стоп", "book": "книга", "mail": "письмо почта конверт",
    "phone": "телефон звонок", "chat": "чат сообщение", "chat2": "чат диалог",
    "bell": "колокольчик звонок уведомление", "calendar": "календарь",
    "clock": "часы время", "hourglass": "песочные часы время",
    "flag": "флаг флажок", "tag": "ярлык метка", "bookmark": "закладка",
    "filter": "фильтр воронка", "refresh": "обновить", "eye": "глаз",
    "search": "поиск лупа", "trophy": "кубок трофей", "medal": "медаль",
    "crown": "корона король", "gift": "подарок", "cart": "корзина покупки",
    "monitor": "монитор компьютер экран", "keyboard": "клавиатура",
    "mouse": "мышь мышка", "cpu": "процессор", "hdd": "диск жесткий",
    "usb": "флешка юсб", "chip": "чип микросхема", "ai_chip": "ии чип",
    "server": "сервер", "network": "сеть", "wifi": "вайфай интернет",
    "battery": "батарея аккумулятор", "power": "питание выключить кнопка",
    "signal": "сигнал связь уровень", "antenna": "антенна",
    "satellite": "спутник", "radar": "радар", "drone": "дрон квадрокоптер",
    "robot": "робот", "bot": "робот бот", "qrcode": "куар код",
    "barcode": "штрихкод", "print": "принтер печать", "scan": "сканер",
    "fax": "факс", "car": "машина авто автомобиль", "taxi": "такси",
    "bus": "автобус", "train": "поезд", "bicycle": "велосипед",
    "plane": "самолет самолёт", "ship": "корабль лодка", "kite": "воздушный змей",
    "balloon": "шарик воздушный шар", "coffee": "кофе чашка",
    "pizza": "пицца", "burger": "бургер", "donut": "пончик",
    "apple": "яблоко", "icecream": "мороженое", "bottle": "бутылка",
    "cake": "торт день рождения праздник", "candle": "свеча",
    "brain": "мозг", "dollar": "доллар деньги", "coin": "монета деньги",
    "wallet": "кошелек кошелёк деньги", "bank": "банк",
    "pill": "таблетка лекарство", "medcross": "медицина аптека крест",
    "arrow_up": "стрелка вверх", "arrow_down": "стрелка вниз",
    "arrow_left": "стрелка влево", "arrow_right": "стрелка вправо",
    "triangle": "треугольник", "hexagon": "шестиугольник", "ring": "кольцо круг",
    "square_filled": "квадрат", "circle_filled": "круг", "halfmoon": "полукруг",
    "yinyang": "инь ян", "home": "дом домик", "door": "дверь",
    "graduation": "выпускник шапочка учеба", "dice": "кубик кости игра",
    "infinity": "бесконечность", "question": "вопрос", "exclaim": "восклицание",
    "compass": "компас", "anchor": "якорь", "umbrella": "зонт зонтик",
    "puzzle": "пазл", "planet": "планета сатурн космос", "ufo": "нло тарелка",
    "gem": "кристалл алмаз камень", "diamond": "ромб алмаз бриллиант",
    "megaphone": "рупор мегафон", "chart_bars": "график диаграмма столбцы",
    "chart_line": "график линия", "chart_pie": "диаграмма круговая",
    "chain": "цепь ссылка звено", "sword": "меч оружие", "potion": "зелье колба",
    "joystick": "джойстик игра", "gamepad": "геймпад игра приставка",
    "cursor": "курсор стрелка мышь", "hexnut": "гайка болт",
    "smile": "улыбка смайл", "sad": "грусть смайл", "wink": "подмигивание",
    "cool": "очки крутой смайл", "glasses": "очки", "tshirt": "футболка одежда",
    "ring_gem": "кольцо перстень свадьба", "crystal_ball": "магический шар гадание",
    "tophat": "шляпа цилиндр", "snowman": "снеговик зима",
    "ball": "мяч футбол", "basketball": "баскетбол мяч", "tennis": "теннис мяч",
    "target": "мишень цель", "dumbbell": "гантеля спорт",
    "atom": "атом наука", "flask": "колба химия", "microscope": "микроскоп",
    "telescope": "телескоп", "magnet": "магнит", "bulb": "лампочка идея",
    "pin": "метка карта булавка", "globe": "глобус планета земля",
    "bug": "жук баг", "wave": "волна", "magic": "магия волшебство палочка",
    "spark": "искра блеск", "scissors": "ножницы", "brush": "кисть",
    "pencil": "карандаш", "calculator": "калькулятор",
    "hashtag": "хештег решетка", "at": "собака эт", "share": "поделиться",
    "thumbsup": "лайк палец вверх", "thumbsdown": "дизлайк палец вниз",
    "dots3": "точки меню", "menu_lines": "меню полоски", "grid": "сетка",
    "list": "список", "layers": "слои", "sliders": "ползунки настройки",
    "database": "база данных",
}


def _base_pixel(x, y, size, c1, c2, style):
    """Цвет (r, g, b) пикселя фона для выбранного стиля (без альфы)."""
    if style == "flat":
        return c1
    if style == "vgrad":
        return blend(c1, c2, y / max(1, size - 1))
    if style == "radial":
        cx = cy = (size - 1) / 2
        d = min(1.0, math.hypot(x - cx, y - cy) / (size * 0.62))
        return blend(c2, c1, d)
    if style == "split":
        return c1 if (x + y) < size else c2
    if style == "neon":
        # Почти чёрный фон + слабое центральное свечение акцентного цвета.
        base = tuple(v // 7 for v in c1)
        cx = cy = (size - 1) / 2
        d = min(1.0, math.hypot(x - cx, y - cy) / (size * 0.7))
        acc = _neon_accent(c2)
        k = (1.0 - d) * 0.10
        return tuple(min(255, int(base[i] + acc[i] * k)) for i in range(3))
    # gradient (а также база для circle / rounded)
    t = (x + y) / max(1, (size - 1) * 2)
    r, g, b = blend(c1, c2, t)
    dx = x - size * 0.28
    dy = y - size * 0.22
    d = min(1.0, math.sqrt(dx * dx + dy * dy) / size)
    boost = int((1.0 - d) * 38)
    return (min(255, r + boost), min(255, g + boost), min(255, b + boost))


def _style_alpha(x, y, size, style):
    """Альфа пикселя фона: у circle/rounded углы прозрачные."""
    if style == "circle":
        cx = cy = (size - 1) / 2
        return 255 if math.hypot(x - cx, y - cy) <= size / 2 - 0.5 else 0
    if style == "rounded":
        rr = max(2, int(size * 0.19))
        # Проверяем 4 угловых квадрата.
        for cx, cy in ((rr, rr), (size - 1 - rr, rr), (rr, size - 1 - rr), (size - 1 - rr, size - 1 - rr)):
            in_corner_x = (x < rr and cx == rr) or (x > size - 1 - rr and cx == size - 1 - rr)
            in_corner_y = (y < rr and cy == rr) or (y > size - 1 - rr and cy == size - 1 - rr)
            if in_corner_x and in_corner_y:
                return 255 if math.hypot(x - cx, y - cy) <= rr else 0
        return 255
    return 255


def make_canvas(size, c1, c2, style="gradient"):
    canvas = []
    for y in range(size):
        row = []
        for x in range(size):
            a = _style_alpha(x, y, size, style)
            if a == 0:
                row.append((0, 0, 0, 0))
                continue
            r, g, b = _base_pixel(x, y, size, c1, c2, style)
            row.append((r, g, b, a))
        canvas.append(row)
    return canvas


def put_px(canvas, x, y, color):
    h = len(canvas)
    w = len(canvas[0]) if h else 0
    if 0 <= x < w and 0 <= y < h:
        canvas[y][x] = color


def draw_rect(canvas, x1, y1, x2, y2, color):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            put_px(canvas, x, y, color)


def restore_rect(canvas, background, x1, y1, x2, y2):
    """Восстанавливает прямоугольную область из снимка фона
    (вместо «вырезания» прозрачным цветом, которое оставляло дырки в .ico)."""
    h = len(canvas)
    w = len(canvas[0]) if h else 0
    for y in range(max(0, y1), min(h, y2 + 1)):
        for x in range(max(0, x1), min(w, x2 + 1)):
            canvas[y][x] = background[y][x]


def draw_circle(canvas, cx, cy, r, color):
    rr = r * r
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= rr:
                put_px(canvas, x, y, color)


def draw_ring(canvas, cx, cy, r, thickness, color):
    r1 = r * r
    r2 = max(0, r - thickness) ** 2
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            d = (x - cx) ** 2 + (y - cy) ** 2
            if r2 <= d <= r1:
                put_px(canvas, x, y, color)


def draw_line(canvas, x1, y1, x2, y2, color, width=2):
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    x, y = x1, y1
    while True:
        r = max(1, width // 2)
        draw_circle(canvas, x, y, r, color)
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    else:
                        xinters = p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def draw_poly(canvas, points, color):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if point_in_poly(x, y, points):
                put_px(canvas, x, y, color)


def draw_text_like(canvas, text, x, y, color):
    patterns = {
        "P": ["1110", "1001", "1110", "1000", "1000"],
        "Y": ["1001", "1001", "0110", "0010", "0010"],
        "E": ["1111", "1000", "1110", "1000", "1111"],
        "X": ["1001", "0110", "0110", "0110", "1001"],
    }
    px = x
    for ch in text:
        pattern = patterns.get(ch.upper())
        if not pattern:
            px += 6
            continue
        for yy, row in enumerate(pattern):
            for xx, bit in enumerate(row):
                if bit == "1":
                    draw_rect(canvas, px + xx * 3, y + yy * 3, px + xx * 3 + 2, y + yy * 3 + 2, color)
        px += len(pattern[0]) * 3 + 3


def draw_glyph(canvas, glyph, color):
    fg = color
    size = len(canvas)
    c = size // 2
    # Снимок чистого фона — для глифов, которым нужно «срезать» часть фигуры
    # (wifi, antenna, mushroom, rainbow) без прозрачных дырок в иконке.
    bg_snapshot = [row[:] for row in canvas]

    if glyph == "py":
        draw_text_like(canvas, "PY", 17, 23, fg)
    elif glyph == "window" or glyph == "browser":
        draw_rect(canvas, 14, 17, 50, 47, fg)
        draw_rect(canvas, 17, 25, 47, 44, (20, 20, 20, 255))
        draw_circle(canvas, 21, 21, 2, (20, 20, 20, 255))
        draw_circle(canvas, 27, 21, 2, (20, 20, 20, 255))
        draw_circle(canvas, 33, 21, 2, (20, 20, 20, 255))
    elif glyph == "terminal":
        draw_rect(canvas, 13, 17, 51, 47, fg)
        draw_rect(canvas, 16, 20, 48, 44, (10, 10, 10, 255))
        draw_line(canvas, 22, 27, 28, 32, fg, 3)
        draw_line(canvas, 22, 37, 28, 32, fg, 3)
        draw_line(canvas, 32, 38, 43, 38, fg, 3)
    elif glyph == "code":
        draw_line(canvas, 27, 19, 15, 32, fg, 5)
        draw_line(canvas, 15, 32, 27, 45, fg, 5)
        draw_line(canvas, 37, 19, 49, 32, fg, 5)
        draw_line(canvas, 49, 32, 37, 45, fg, 5)
    elif glyph == "package":
        draw_poly(canvas, [(32, 10), (49, 20), (32, 30), (15, 20)], fg)
        draw_poly(canvas, [(15, 23), (31, 33), (31, 53), (15, 43)], fg)
        draw_poly(canvas, [(49, 23), (33, 33), (33, 53), (49, 43)], fg)
    elif glyph == "rocket":
        draw_poly(canvas, [(32, 9), (43, 31), (35, 45), (29, 45), (21, 31)], fg)
        draw_circle(canvas, 32, 27, 5, (40, 40, 40, 255))
        draw_poly(canvas, [(24, 40), (17, 51), (29, 45)], fg)
        draw_poly(canvas, [(40, 40), (47, 51), (35, 45)], fg)
    elif glyph == "bolt":
        draw_poly(canvas, [(36, 8), (19, 35), (31, 35), (27, 56), (46, 27), (34, 27)], fg)
    elif glyph == "shield":
        draw_poly(canvas, [(32, 9), (48, 16), (45, 39), (32, 54), (19, 39), (16, 16)], fg)
        draw_line(canvas, 24, 32, 30, 39, (30, 30, 30, 255), 4)
        draw_line(canvas, 30, 39, 42, 24, (30, 30, 30, 255), 4)
    elif glyph == "star":
        pts = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            r = 23 if i % 2 == 0 else 10
            pts.append((int(c + math.cos(angle) * r), int(c + math.sin(angle) * r)))
        draw_poly(canvas, pts, fg)
    elif glyph == "gear":
        draw_ring(canvas, c, c, 19, 7, fg)
        for ang in range(0, 360, 45):
            x = int(c + math.cos(math.radians(ang)) * 24)
            y = int(c + math.sin(math.radians(ang)) * 24)
            draw_circle(canvas, x, y, 4, fg)
    elif glyph == "robot":
        draw_rect(canvas, 18, 22, 46, 45, fg)
        draw_line(canvas, 32, 22, 32, 14, fg, 3)
        draw_circle(canvas, 32, 12, 3, fg)
        draw_circle(canvas, 26, 32, 3, (20, 20, 20, 255))
        draw_circle(canvas, 38, 32, 3, (20, 20, 20, 255))
        draw_line(canvas, 25, 40, 39, 40, (20, 20, 20, 255), 3)
    elif glyph == "video":
        draw_rect(canvas, 14, 22, 40, 43, fg)
        draw_poly(canvas, [(41, 27), (53, 20), (53, 45), (41, 38)], fg)
    elif glyph == "music":
        draw_line(canvas, 37, 15, 37, 43, fg, 5)
        draw_line(canvas, 37, 17, 49, 14, fg, 5)
        draw_circle(canvas, 28, 45, 8, fg)
        draw_circle(canvas, 45, 40, 8, fg)
    elif glyph == "download":
        draw_line(canvas, 32, 13, 32, 38, fg, 6)
        draw_poly(canvas, [(20, 32), (44, 32), (32, 45)], fg)
        draw_rect(canvas, 17, 48, 47, 54, fg)
    elif glyph == "upload":
        draw_line(canvas, 32, 51, 32, 26, fg, 6)
        draw_poly(canvas, [(20, 32), (44, 32), (32, 19)], fg)
        draw_rect(canvas, 17, 10, 47, 16, fg)
    elif glyph == "folder":
        draw_rect(canvas, 12, 22, 52, 48, fg)
        draw_rect(canvas, 16, 16, 32, 24, fg)
    elif glyph == "magic" or glyph == "spark":
        draw_line(canvas, 20, 47, 46, 19, fg, 5)
        draw_poly(canvas, [(46, 8), (49, 17), (58, 20), (49, 23), (46, 32), (43, 23), (34, 20), (43, 17)], fg)
        draw_poly(canvas, [(18, 9), (20, 15), (26, 17), (20, 19), (18, 25), (16, 19), (10, 17), (16, 15)], fg)
    elif glyph == "cloud":
        draw_circle(canvas, 25, 36, 11, fg)
        draw_circle(canvas, 36, 31, 15, fg)
        draw_circle(canvas, 45, 38, 10, fg)
        draw_rect(canvas, 20, 36, 50, 47, fg)
    elif glyph == "fire":
        draw_poly(canvas, [(33, 8), (45, 28), (40, 48), (32, 55), (22, 48), (18, 34), (25, 23), (26, 37), (34, 28)], fg)
    elif glyph == "cube":
        draw_poly(canvas, [(32, 11), (49, 21), (32, 31), (15, 21)], fg)
        draw_poly(canvas, [(15, 22), (32, 32), (32, 53), (15, 43)], fg)
        draw_poly(canvas, [(49, 22), (32, 32), (32, 53), (49, 43)], fg)
    elif glyph == "database":
        draw_ring(canvas, 32, 20, 16, 5, fg)
        draw_rect(canvas, 16, 20, 48, 45, fg)
        draw_ring(canvas, 32, 45, 16, 5, fg)
    elif glyph == "lock":
        draw_rect(canvas, 18, 30, 46, 51, fg)
        draw_ring(canvas, 32, 30, 13, 5, fg)
    elif glyph == "key":
        draw_ring(canvas, 23, 32, 10, 4, fg)
        draw_line(canvas, 32, 32, 52, 32, fg, 5)
        draw_line(canvas, 45, 32, 45, 40, fg, 4)
        draw_line(canvas, 51, 32, 51, 38, fg, 4)
    elif glyph == "camera":
        draw_rect(canvas, 14, 23, 50, 47, fg)
        draw_rect(canvas, 22, 17, 36, 24, fg)
        draw_circle(canvas, 32, 35, 10, (30, 30, 30, 255))
        draw_circle(canvas, 32, 35, 6, fg)
    elif glyph == "image":
        draw_rect(canvas, 14, 16, 50, 48, fg)
        draw_circle(canvas, 40, 25, 4, (30, 30, 30, 255))
        draw_poly(canvas, [(18, 45), (29, 32), (37, 41), (43, 35), (49, 45)], (30, 30, 30, 255))
    elif glyph == "book":
        draw_rect(canvas, 18, 13, 45, 52, fg)
        draw_line(canvas, 26, 14, 26, 51, (30, 30, 30, 255), 3)
        draw_line(canvas, 31, 22, 41, 22, (30, 30, 30, 255), 2)
        draw_line(canvas, 31, 29, 41, 29, (30, 30, 30, 255), 2)
    elif glyph == "wrench":
        draw_line(canvas, 22, 49, 46, 25, fg, 7)
        draw_ring(canvas, 48, 19, 9, 4, fg)
        draw_circle(canvas, 20, 51, 6, fg)
    elif glyph == "globe":
        draw_ring(canvas, 32, 32, 21, 4, fg)
        draw_line(canvas, 11, 32, 53, 32, fg, 3)
        draw_line(canvas, 32, 11, 32, 53, fg, 3)
        draw_ring(canvas, 32, 32, 12, 3, fg)
    elif glyph == "heart":
        draw_circle(canvas, 24, 25, 10, fg)
        draw_circle(canvas, 40, 25, 10, fg)
        draw_poly(canvas, [(14, 30), (50, 30), (32, 53)], fg)
    elif glyph == "check":
        draw_line(canvas, 17, 33, 28, 44, fg, 7)
        draw_line(canvas, 28, 44, 49, 20, fg, 7)
    elif glyph == "cross":
        draw_line(canvas, 19, 19, 45, 45, fg, 7)
        draw_line(canvas, 45, 19, 19, 45, fg, 7)
    elif glyph == "plus":
        draw_rect(canvas, 28, 14, 36, 50, fg)
        draw_rect(canvas, 14, 28, 50, 36, fg)
    elif glyph == "gamepad":
        draw_rect(canvas, 15, 28, 49, 43, fg)
        draw_circle(canvas, 21, 35, 9, fg)
        draw_circle(canvas, 43, 35, 9, fg)
        draw_line(canvas, 21, 31, 21, 39, (30, 30, 30, 255), 3)
        draw_line(canvas, 17, 35, 25, 35, (30, 30, 30, 255), 3)
        draw_circle(canvas, 40, 35, 2, (30, 30, 30, 255))
        draw_circle(canvas, 46, 35, 2, (30, 30, 30, 255))
    elif glyph == "bug":
        draw_circle(canvas, 32, 33, 13, fg)
        draw_circle(canvas, 32, 18, 8, fg)
        for y in (28, 36, 44):
            draw_line(canvas, 19, y, 10, y - 4, fg, 3)
            draw_line(canvas, 45, y, 54, y - 4, fg, 3)
    elif glyph == "wave":
        draw_line(canvas, 10, 38, 20, 30, fg, 5)
        draw_line(canvas, 20, 30, 32, 38, fg, 5)
        draw_line(canvas, 32, 38, 44, 30, fg, 5)
        draw_line(canvas, 44, 30, 54, 38, fg, 5)
    elif glyph == "diamond":
        draw_poly(canvas, [(32, 9), (53, 32), (32, 55), (11, 32)], fg)
    elif glyph == "play":
        draw_poly(canvas, [(23, 16), (23, 50), (50, 33)], fg)
    elif glyph == "pause":
        draw_rect(canvas, 21, 17, 29, 48, fg)
        draw_rect(canvas, 36, 17, 44, 48, fg)
    elif glyph == "stop":
        draw_rect(canvas, 20, 20, 44, 44, fg)
    elif glyph == "scissors":
        draw_circle(canvas, 21, 43, 7, fg)
        draw_circle(canvas, 43, 43, 7, fg)
        draw_line(canvas, 25, 39, 45, 18, fg, 4)
        draw_line(canvas, 39, 39, 19, 18, fg, 4)
    elif glyph == "search":
        draw_ring(canvas, 28, 28, 13, 5, fg)
        draw_line(canvas, 38, 38, 51, 51, fg, 6)
    elif glyph == "sun":
        draw_circle(canvas, c, c, 11, fg)
        for ang in range(0, 360, 45):
            x1 = int(c + math.cos(math.radians(ang)) * 17)
            y1 = int(c + math.sin(math.radians(ang)) * 17)
            x2 = int(c + math.cos(math.radians(ang)) * 26)
            y2 = int(c + math.sin(math.radians(ang)) * 26)
            draw_line(canvas, x1, y1, x2, y2, fg, 4)
    elif glyph == "moon":
        draw_circle(canvas, 32, 32, 20, fg)
        draw_circle(canvas, 40, 26, 18, (20, 20, 30, 255))
    elif glyph == "snowflake":
        for ang in range(0, 360, 60):
            x = int(c + math.cos(math.radians(ang)) * 24)
            y = int(c + math.sin(math.radians(ang)) * 24)
            draw_line(canvas, c, c, x, y, fg, 3)
            # маленькие "лучики"
            sx = int(c + math.cos(math.radians(ang)) * 14)
            sy = int(c + math.sin(math.radians(ang)) * 14)
            for off in (-30, 30):
                ex = int(sx + math.cos(math.radians(ang + off)) * 7)
                ey = int(sy + math.sin(math.radians(ang + off)) * 7)
                draw_line(canvas, sx, sy, ex, ey, fg, 2)
    elif glyph == "leaf":
        draw_poly(canvas, [(14, 50), (22, 22), (50, 14), (42, 42)], fg)
        draw_line(canvas, 14, 50, 42, 22, (20, 60, 20, 255), 2)
    elif glyph == "tree":
        draw_poly(canvas, [(32, 8), (20, 28), (28, 28), (16, 44), (48, 44), (36, 28), (44, 28)], fg)
        draw_rect(canvas, 29, 44, 35, 54, (90, 50, 20, 255))
    elif glyph == "flower":
        for ang in range(0, 360, 72):
            x = int(c + math.cos(math.radians(ang)) * 13)
            y = int(c + math.sin(math.radians(ang)) * 13)
            draw_circle(canvas, x, y, 8, fg)
        draw_circle(canvas, c, c, 6, (255, 220, 80, 255))
        draw_line(canvas, c, c + 18, c, 56, (40, 120, 40, 255), 3)
    elif glyph == "coffee":
        draw_rect(canvas, 18, 22, 44, 50, fg)
        draw_ring(canvas, 47, 32, 6, 3, fg)
        draw_line(canvas, 24, 14, 22, 20, fg, 2)
        draw_line(canvas, 30, 14, 28, 20, fg, 2)
        draw_line(canvas, 36, 14, 34, 20, fg, 2)
    elif glyph == "pizza":
        draw_poly(canvas, [(32, 10), (54, 50), (10, 50)], fg)
        draw_circle(canvas, 24, 36, 3, (200, 30, 30, 255))
        draw_circle(canvas, 38, 32, 3, (200, 30, 30, 255))
        draw_circle(canvas, 32, 44, 3, (200, 30, 30, 255))
    elif glyph == "headphones":
        draw_ring(canvas, 32, 30, 20, 4, fg)
        draw_rect(canvas, 10, 30, 20, 48, fg)
        draw_rect(canvas, 44, 30, 54, 48, fg)
    elif glyph == "microphone":
        draw_rect(canvas, 26, 12, 38, 38, fg)
        # скругление сверху
        draw_circle(canvas, 32, 12, 6, fg)
        draw_circle(canvas, 32, 38, 6, fg)
        draw_ring(canvas, 32, 38, 12, 3, fg)
        draw_line(canvas, 32, 50, 32, 56, fg, 3)
        draw_line(canvas, 22, 56, 42, 56, fg, 3)
    elif glyph == "phone":
        draw_poly(canvas, [(16, 14), (28, 14), (32, 24), (26, 30),
                            (34, 38), (40, 32), (50, 36), (50, 48),
                            (44, 52), (28, 48), (16, 36), (12, 20)], fg)
    elif glyph == "mail":
        draw_rect(canvas, 12, 20, 52, 46, fg)
        draw_line(canvas, 12, 20, 32, 36, (30, 30, 30, 255), 3)
        draw_line(canvas, 52, 20, 32, 36, (30, 30, 30, 255), 3)
    elif glyph == "bell":
        draw_poly(canvas, [(32, 12), (48, 40), (16, 40)], fg)
        draw_rect(canvas, 16, 40, 48, 44, fg)
        draw_circle(canvas, 32, 49, 4, fg)
    elif glyph == "calendar":
        draw_rect(canvas, 12, 18, 52, 50, fg)
        draw_rect(canvas, 12, 18, 52, 26, (180, 30, 30, 255))
        draw_line(canvas, 20, 14, 20, 22, fg, 3)
        draw_line(canvas, 44, 14, 44, 22, fg, 3)
        for r in (32, 40):
            for col in (18, 26, 34, 42, 50):
                draw_rect(canvas, col - 2, r - 2, col + 2, r + 2, (30, 30, 30, 255))
    elif glyph == "clock":
        draw_ring(canvas, c, c, 22, 4, fg)
        draw_line(canvas, c, c, c, 18, fg, 3)
        draw_line(canvas, c, c, 44, c, fg, 3)
        draw_circle(canvas, c, c, 2, fg)
    elif glyph == "flag":
        draw_rect(canvas, 16, 10, 19, 56, fg)
        draw_poly(canvas, [(19, 12), (50, 18), (40, 26), (50, 34), (19, 28)], fg)
    elif glyph == "tag":
        draw_poly(canvas, [(10, 22), (32, 10), (54, 32), (32, 54), (10, 32)], fg)
        draw_circle(canvas, 22, 22, 3, (30, 30, 30, 255))
    elif glyph == "bookmark":
        draw_poly(canvas, [(18, 10), (46, 10), (46, 56), (32, 44), (18, 56)], fg)
    elif glyph == "filter":
        draw_poly(canvas, [(12, 14), (52, 14), (38, 34), (38, 52), (26, 46), (26, 34)], fg)
    elif glyph == "refresh":
        draw_ring(canvas, c, c, 18, 4, fg)
        # вырез
        draw_rect(canvas, 32, 8, 56, 22, (0, 0, 0, 0))
        draw_poly(canvas, [(46, 8), (54, 18), (38, 18)], fg)
    elif glyph == "eye":
        draw_poly(canvas, [(8, 32), (32, 16), (56, 32), (32, 48)], fg)
        draw_circle(canvas, 32, 32, 8, (30, 30, 30, 255))
        draw_circle(canvas, 32, 32, 4, fg)
    elif glyph == "trophy":
        draw_rect(canvas, 22, 14, 42, 36, fg)
        draw_ring(canvas, 14, 22, 8, 3, fg)
        draw_ring(canvas, 50, 22, 8, 3, fg)
        draw_rect(canvas, 26, 36, 38, 44, fg)
        draw_rect(canvas, 20, 44, 44, 50, fg)
    elif glyph == "medal":
        draw_poly(canvas, [(20, 10), (44, 10), (38, 30), (26, 30)], fg)
        draw_circle(canvas, 32, 42, 14, fg)
        draw_circle(canvas, 32, 42, 8, (180, 130, 20, 255))
    elif glyph == "crown":
        draw_poly(canvas, [(10, 50), (14, 20), (24, 36), (32, 14),
                            (40, 36), (50, 20), (54, 50)], fg)
        draw_rect(canvas, 10, 50, 54, 54, fg)
    elif glyph == "gift":
        draw_rect(canvas, 12, 28, 52, 54, fg)
        draw_rect(canvas, 12, 22, 52, 30, fg)
        draw_rect(canvas, 29, 22, 35, 54, (200, 40, 40, 255))
        draw_circle(canvas, 24, 18, 5, fg)
        draw_circle(canvas, 40, 18, 5, fg)
    elif glyph == "cart":
        draw_line(canvas, 8, 14, 16, 14, fg, 3)
        draw_poly(canvas, [(16, 14), (54, 18), (48, 38), (22, 38)], fg)
        draw_circle(canvas, 26, 48, 4, fg)
        draw_circle(canvas, 46, 48, 4, fg)
    elif glyph == "monitor":
        draw_rect(canvas, 8, 14, 56, 44, fg)
        draw_rect(canvas, 12, 18, 52, 40, (20, 20, 30, 255))
        draw_rect(canvas, 24, 44, 40, 50, fg)
        draw_rect(canvas, 18, 50, 46, 54, fg)
    elif glyph == "keyboard":
        draw_rect(canvas, 6, 22, 58, 46, fg)
        for col in range(10, 56, 8):
            draw_rect(canvas, col, 26, col + 5, 30, (20, 20, 30, 255))
            draw_rect(canvas, col, 32, col + 5, 36, (20, 20, 30, 255))
        draw_rect(canvas, 18, 38, 46, 42, (20, 20, 30, 255))
    elif glyph == "mouse":
        draw_rect(canvas, 22, 14, 42, 50, fg)
        draw_line(canvas, 32, 14, 32, 30, (20, 20, 30, 255), 2)
        draw_circle(canvas, 32, 22, 2, (20, 20, 30, 255))
    elif glyph == "cpu":
        draw_rect(canvas, 16, 16, 48, 48, fg)
        draw_rect(canvas, 22, 22, 42, 42, (20, 20, 30, 255))
        for i in range(20, 45, 8):
            draw_rect(canvas, i, 8, i + 3, 16, fg)
            draw_rect(canvas, i, 48, i + 3, 56, fg)
            draw_rect(canvas, 8, i, 16, i + 3, fg)
            draw_rect(canvas, 48, i, 56, i + 3, fg)
    elif glyph == "hdd":
        draw_rect(canvas, 8, 22, 56, 42, fg)
        draw_circle(canvas, 48, 32, 3, (200, 40, 40, 255))
        draw_rect(canvas, 14, 28, 38, 36, (20, 20, 30, 255))
    elif glyph == "usb":
        draw_circle(canvas, 32, 14, 5, fg)
        draw_line(canvas, 32, 14, 32, 50, fg, 4)
        draw_poly(canvas, [(20, 30), (28, 30), (24, 22)], fg)
        draw_line(canvas, 24, 30, 24, 38, fg, 3)
        draw_line(canvas, 24, 38, 32, 42, fg, 3)
        draw_rect(canvas, 38, 28, 44, 34, fg)
        draw_line(canvas, 41, 34, 41, 42, fg, 3)
        draw_line(canvas, 41, 42, 32, 46, fg, 3)
        draw_rect(canvas, 26, 50, 38, 56, fg)
    elif glyph == "car":
        draw_rect(canvas, 8, 30, 56, 44, fg)
        draw_poly(canvas, [(14, 30), (20, 18), (44, 18), (50, 30)], fg)
        draw_circle(canvas, 18, 46, 5, (20, 20, 30, 255))
        draw_circle(canvas, 46, 46, 5, (20, 20, 30, 255))
    elif glyph == "plane":
        draw_poly(canvas, [(8, 32), (28, 28), (40, 12), (44, 12), (36, 30),
                            (54, 32), (36, 36), (44, 52), (40, 52), (28, 38),
                            (8, 36)], fg)
    elif glyph == "ship":
        draw_rect(canvas, 10, 40, 54, 50, fg)
        draw_poly(canvas, [(10, 40), (54, 40), (48, 50), (16, 50)], fg)
        draw_rect(canvas, 28, 16, 36, 40, fg)
        draw_line(canvas, 32, 8, 32, 18, fg, 3)
        draw_poly(canvas, [(32, 14), (44, 28), (32, 28)], fg)
    elif glyph == "brush":
        draw_poly(canvas, [(40, 12), (52, 24), (28, 48), (16, 36)], fg)
        draw_rect(canvas, 12, 40, 22, 54, fg)
        draw_poly(canvas, [(12, 54), (22, 54), (17, 60)], fg)
    elif glyph == "pencil":
        draw_poly(canvas, [(46, 10), (54, 18), (24, 48), (12, 52),
                            (16, 40)], fg)
        draw_poly(canvas, [(12, 52), (20, 50), (16, 56)], (40, 30, 20, 255))
    elif glyph == "calculator":
        draw_rect(canvas, 12, 10, 52, 56, fg)
        draw_rect(canvas, 16, 14, 48, 22, (20, 20, 30, 255))
        for row in range(26, 54, 8):
            for col in range(16, 48, 8):
                draw_rect(canvas, col, row, col + 5, row + 5, (20, 20, 30, 255))
    elif glyph == "atom":
        draw_circle(canvas, c, c, 4, fg)
        draw_ring(canvas, c, c, 22, 2, fg)
        # два эллипса под углом — упрощённо как линии-овалы
        for ang in (45, -45):
            pts = []
            for t in range(0, 360, 12):
                rx, ry = 22, 9
                x = int(rx * math.cos(math.radians(t)))
                y = int(ry * math.sin(math.radians(t)))
                xr = int(x * math.cos(math.radians(ang)) - y * math.sin(math.radians(ang))) + c
                yr = int(x * math.sin(math.radians(ang)) + y * math.cos(math.radians(ang))) + c
                pts.append((xr, yr))
            for i in range(len(pts)):
                p1 = pts[i]
                p2 = pts[(i + 1) % len(pts)]
                draw_line(canvas, p1[0], p1[1], p2[0], p2[1], fg, 1)
    elif glyph == "flask":
        draw_line(canvas, 24, 10, 40, 10, fg, 3)
        draw_poly(canvas, [(26, 10), (38, 10), (38, 26), (50, 52), (14, 52), (26, 26)], fg)
        draw_poly(canvas, [(20, 40), (44, 40), (50, 52), (14, 52)], (100, 180, 220, 255))
    elif glyph == "bulb":
        draw_circle(canvas, 32, 26, 16, fg)
        draw_rect(canvas, 24, 40, 40, 48, fg)
        draw_rect(canvas, 26, 48, 38, 52, fg)
        draw_rect(canvas, 28, 52, 36, 56, fg)
    elif glyph == "speaker":
        draw_rect(canvas, 14, 14, 50, 50, fg)
        draw_circle(canvas, 32, 26, 5, (20, 20, 30, 255))
        draw_circle(canvas, 32, 42, 9, (20, 20, 30, 255))
        draw_circle(canvas, 32, 42, 4, fg)
    elif glyph == "pin":
        draw_circle(canvas, 32, 26, 14, fg)
        draw_circle(canvas, 32, 26, 5, (20, 20, 30, 255))
        draw_poly(canvas, [(22, 36), (42, 36), (32, 56)], fg)
    elif glyph == "wifi":
        for r, w in ((26, 5), (18, 4), (10, 3)):
            draw_ring(canvas, 32, 44, r, w, fg)
        # верхняя половина — нижнюю восстанавливаем фоном (один раз, после колец)
        restore_rect(canvas, bg_snapshot, 0, 44, 63, 63)
        draw_circle(canvas, 32, 48, 3, fg)
    elif glyph == "battery":
        draw_rect(canvas, 8, 22, 50, 42, fg)
        draw_rect(canvas, 50, 28, 56, 36, fg)
        draw_rect(canvas, 12, 26, 36, 38, (60, 220, 100, 255))
    elif glyph == "hammer":
        draw_poly(canvas, [(10, 16), (30, 8), (40, 18), (20, 26)], fg)
        draw_line(canvas, 24, 22, 50, 50, fg, 6)
    # --- 0.3.2: новые глифы ---
    elif glyph == "ball":
        draw_circle(canvas, c, c, 22, fg)
        # шестиугольник в центре
        pts = []
        for i in range(6):
            a = math.radians(60 * i - 30)
            pts.append((int(c + math.cos(a) * 7), int(c + math.sin(a) * 7)))
        draw_poly(canvas, pts, (20, 20, 30, 255))
        for i in range(6):
            a = math.radians(60 * i + 30)
            x = int(c + math.cos(a) * 18)
            y = int(c + math.sin(a) * 18)
            draw_line(canvas, pts[i][0], pts[i][1], x, y, (20, 20, 30, 255), 2)
    elif glyph == "basketball":
        draw_circle(canvas, c, c, 22, fg)
        draw_line(canvas, c, 10, c, 54, (20, 20, 30, 255), 2)
        draw_line(canvas, 10, c, 54, c, (20, 20, 30, 255), 2)
        draw_ring(canvas, c, c, 22, 2, (20, 20, 30, 255))
    elif glyph == "tennis":
        draw_circle(canvas, c, c, 22, fg)
        # дуга-шов
        for t in range(-50, 51, 4):
            x = c + t
            y = int(c - 16 + (t * t) / 80)
            put_px(canvas, x, y, (20, 20, 30, 255))
            put_px(canvas, x, y + 1, (20, 20, 30, 255))
            put_px(canvas, x, 64 - y, (20, 20, 30, 255))
            put_px(canvas, x, 65 - y, (20, 20, 30, 255))
    elif glyph == "target":
        draw_ring(canvas, c, c, 24, 3, fg)
        draw_ring(canvas, c, c, 17, 3, fg)
        draw_ring(canvas, c, c, 10, 3, fg)
        draw_circle(canvas, c, c, 4, fg)
    elif glyph == "dumbbell":
        draw_rect(canvas, 8, 26, 14, 38, fg)
        draw_rect(canvas, 50, 26, 56, 38, fg)
        draw_rect(canvas, 14, 30, 50, 34, fg)
        draw_rect(canvas, 4, 28, 8, 36, fg)
        draw_rect(canvas, 56, 28, 60, 36, fg)
    elif glyph == "mountain":
        draw_poly(canvas, [(6, 50), (22, 22), (32, 38), (44, 14), (58, 50)], fg)
        draw_poly(canvas, [(38, 22), (44, 14), (50, 22)], (240, 240, 240, 255))
    elif glyph == "ocean":
        for y_off in (28, 36, 44):
            draw_line(canvas, 8, y_off, 18, y_off - 5, fg, 3)
            draw_line(canvas, 18, y_off - 5, 32, y_off, fg, 3)
            draw_line(canvas, 32, y_off, 46, y_off - 5, fg, 3)
            draw_line(canvas, 46, y_off - 5, 56, y_off, fg, 3)
    elif glyph == "rainbow":
        for i, color in enumerate([(255, 60, 60, 255), (255, 160, 40, 255),
                                    (255, 240, 60, 255), (60, 200, 80, 255),
                                    (60, 140, 240, 255), (180, 80, 220, 255)]):
            draw_ring(canvas, 32, 50, 26 - i * 3, 3, color)
        restore_rect(canvas, bg_snapshot, 0, 50, 63, 63)
    elif glyph == "drop":
        draw_poly(canvas, [(32, 8), (44, 28), (44, 44), (20, 44), (20, 28)], fg)
        draw_circle(canvas, 32, 42, 14, fg)
    elif glyph == "mushroom":
        draw_circle(canvas, c, 26, 22, fg)
        restore_rect(canvas, bg_snapshot, 0, 26, 63, 38)
        draw_rect(canvas, 26, 36, 38, 56, (240, 230, 200, 255))
        draw_circle(canvas, 24, 22, 4, (255, 255, 255, 255))
        draw_circle(canvas, 40, 26, 3, (255, 255, 255, 255))
    elif glyph == "bus":
        draw_rect(canvas, 8, 16, 56, 46, fg)
        draw_rect(canvas, 12, 20, 28, 32, (20, 20, 30, 255))
        draw_rect(canvas, 32, 20, 52, 32, (20, 20, 30, 255))
        draw_circle(canvas, 18, 48, 5, (20, 20, 30, 255))
        draw_circle(canvas, 46, 48, 5, (20, 20, 30, 255))
    elif glyph == "train":
        draw_rect(canvas, 12, 14, 52, 44, fg)
        draw_rect(canvas, 16, 18, 30, 30, (20, 20, 30, 255))
        draw_rect(canvas, 34, 18, 48, 30, (20, 20, 30, 255))
        draw_line(canvas, 12, 38, 52, 38, (20, 20, 30, 255), 2)
        draw_circle(canvas, 20, 50, 4, (20, 20, 30, 255))
        draw_circle(canvas, 44, 50, 4, (20, 20, 30, 255))
        draw_rect(canvas, 6, 48, 14, 54, fg)
        draw_rect(canvas, 50, 48, 58, 54, fg)
    elif glyph == "bicycle":
        draw_ring(canvas, 16, 44, 10, 3, fg)
        draw_ring(canvas, 48, 44, 10, 3, fg)
        draw_line(canvas, 16, 44, 32, 24, fg, 3)
        draw_line(canvas, 32, 24, 48, 44, fg, 3)
        draw_line(canvas, 22, 44, 38, 24, fg, 3)
        draw_line(canvas, 28, 18, 36, 18, fg, 3)
    elif glyph == "taxi":
        draw_rect(canvas, 8, 30, 56, 44, fg)
        draw_poly(canvas, [(14, 30), (20, 18), (44, 18), (50, 30)], fg)
        draw_rect(canvas, 18, 8, 46, 16, fg)
        draw_circle(canvas, 18, 46, 5, (20, 20, 30, 255))
        draw_circle(canvas, 46, 46, 5, (20, 20, 30, 255))
    elif glyph == "burger":
        draw_poly(canvas, [(8, 30), (32, 14), (56, 30)], fg)
        draw_rect(canvas, 8, 30, 56, 36, (120, 60, 30, 255))
        draw_rect(canvas, 8, 36, 56, 40, (60, 180, 60, 255))
        draw_rect(canvas, 8, 40, 56, 50, fg)
    elif glyph == "donut":
        draw_circle(canvas, c, c, 22, fg)
        draw_circle(canvas, c, c, 8, (40, 40, 50, 255))
        for x, y in [(18, 20), (42, 22), (24, 44), (44, 42), (32, 18), (16, 32), (48, 32)]:
            draw_circle(canvas, x, y, 2, (255, 100, 200, 255))
    elif glyph == "apple":
        draw_circle(canvas, 24, 38, 14, fg)
        draw_circle(canvas, 40, 38, 14, fg)
        draw_rect(canvas, 16, 32, 48, 50, fg)
        draw_line(canvas, 32, 14, 32, 24, (60, 40, 20, 255), 3)
        draw_poly(canvas, [(32, 16), (40, 12), (40, 18)], (40, 140, 40, 255))
    elif glyph == "icecream":
        draw_circle(canvas, 32, 22, 12, fg)
        draw_circle(canvas, 24, 18, 10, (255, 180, 200, 255))
        draw_circle(canvas, 40, 20, 10, (180, 140, 80, 255))
        draw_poly(canvas, [(20, 30), (44, 30), (32, 58)], (200, 160, 80, 255))
        for y in (36, 42, 48):
            draw_line(canvas, 24, y, 40, y, (140, 100, 50, 255), 1)
    elif glyph == "bottle":
        draw_rect(canvas, 28, 8, 36, 18, fg)
        draw_rect(canvas, 24, 18, 40, 24, fg)
        draw_poly(canvas, [(24, 24), (40, 24), (44, 36), (44, 54), (20, 54), (20, 36)], fg)
        draw_rect(canvas, 20, 40, 44, 54, (100, 180, 220, 255))
    elif glyph == "brain":
        draw_circle(canvas, 22, 26, 12, fg)
        draw_circle(canvas, 42, 26, 12, fg)
        draw_circle(canvas, 26, 40, 10, fg)
        draw_circle(canvas, 38, 40, 10, fg)
        draw_line(canvas, 32, 14, 32, 50, (200, 100, 100, 255), 2)
    elif glyph == "server":
        for y_off in (12, 28, 44):
            draw_rect(canvas, 10, y_off, 54, y_off + 10, fg)
            draw_circle(canvas, 18, y_off + 5, 2, (60, 200, 80, 255))
            draw_circle(canvas, 26, y_off + 5, 2, (200, 60, 60, 255))
            draw_rect(canvas, 36, y_off + 3, 50, y_off + 7, (20, 20, 30, 255))
    elif glyph == "network":
        draw_circle(canvas, 32, 12, 5, fg)
        draw_circle(canvas, 12, 44, 5, fg)
        draw_circle(canvas, 52, 44, 5, fg)
        draw_circle(canvas, 32, 36, 5, fg)
        draw_line(canvas, 32, 12, 12, 44, fg, 2)
        draw_line(canvas, 32, 12, 52, 44, fg, 2)
        draw_line(canvas, 32, 12, 32, 36, fg, 2)
    elif glyph == "chip":
        draw_rect(canvas, 14, 14, 50, 50, fg)
        draw_rect(canvas, 22, 22, 42, 42, (20, 20, 30, 255))
        # ножки
        for i in range(18, 49, 8):
            draw_rect(canvas, i, 8, i + 4, 14, fg)
            draw_rect(canvas, i, 50, i + 4, 56, fg)
            draw_rect(canvas, 8, i, 14, i + 4, fg)
            draw_rect(canvas, 50, i, 56, i + 4, fg)
    elif glyph == "dollar":
        # символ $
        draw_line(canvas, 32, 10, 32, 54, fg, 3)
        draw_poly(canvas, [(20, 18), (44, 18), (44, 26), (20, 30), (20, 38), (44, 42), (44, 50), (20, 50)], fg)
    elif glyph == "coin":
        draw_circle(canvas, c, c, 22, fg)
        draw_circle(canvas, c, c, 18, (160, 120, 30, 255))
        # символ $ внутри
        draw_line(canvas, 32, 18, 32, 46, fg, 2)
        draw_line(canvas, 26, 22, 38, 22, fg, 2)
        draw_line(canvas, 26, 42, 38, 42, fg, 2)
    elif glyph == "wallet":
        draw_rect(canvas, 8, 18, 56, 50, fg)
        draw_rect(canvas, 8, 26, 56, 38, (40, 80, 40, 255))
        draw_circle(canvas, 46, 32, 3, (220, 200, 80, 255))
    elif glyph == "bank":
        draw_poly(canvas, [(32, 8), (56, 22), (8, 22)], fg)
        for x in (14, 26, 38, 50):
            draw_rect(canvas, x - 3, 22, x + 3, 46, fg)
        draw_rect(canvas, 6, 46, 58, 54, fg)
    elif glyph == "pill":
        draw_poly(canvas, [(14, 22), (50, 22), (50, 42), (14, 42)], fg)
        draw_circle(canvas, 14, 32, 10, fg)
        draw_circle(canvas, 50, 32, 10, (220, 80, 80, 255))
        draw_rect(canvas, 14, 22, 32, 42, (255, 255, 255, 255))
    elif glyph == "medcross":
        draw_rect(canvas, 26, 10, 38, 54, (220, 40, 40, 255))
        draw_rect(canvas, 10, 26, 54, 38, (220, 40, 40, 255))
    elif glyph == "arrow_up":
        draw_poly(canvas, [(14, 36), (50, 36), (32, 12)], fg)
        draw_rect(canvas, 27, 36, 37, 54, fg)
    elif glyph == "arrow_down":
        draw_poly(canvas, [(14, 28), (50, 28), (32, 52)], fg)
        draw_rect(canvas, 27, 10, 37, 28, fg)
    elif glyph == "arrow_left":
        draw_poly(canvas, [(36, 14), (36, 50), (12, 32)], fg)
        draw_rect(canvas, 36, 27, 54, 37, fg)
    elif glyph == "arrow_right":
        draw_poly(canvas, [(28, 14), (28, 50), (52, 32)], fg)
        draw_rect(canvas, 10, 27, 28, 37, fg)
    elif glyph == "triangle":
        draw_poly(canvas, [(32, 10), (54, 50), (10, 50)], fg)
    elif glyph == "hexagon":
        pts = []
        for i in range(6):
            a = math.radians(60 * i)
            pts.append((int(c + math.cos(a) * 22), int(c + math.sin(a) * 22)))
        draw_poly(canvas, pts, fg)
    elif glyph == "ring":
        draw_ring(canvas, c, c, 22, 6, fg)
    elif glyph == "square_filled":
        draw_rect(canvas, 12, 12, 52, 52, fg)
    elif glyph == "home":
        draw_poly(canvas, [(8, 32), (32, 10), (56, 32)], fg)
        draw_rect(canvas, 14, 32, 50, 54, fg)
        draw_rect(canvas, 26, 38, 38, 54, (40, 60, 30, 255))
    elif glyph == "door":
        draw_rect(canvas, 16, 10, 48, 54, fg)
        draw_rect(canvas, 20, 14, 44, 50, (40, 40, 50, 255))
        draw_circle(canvas, 40, 32, 2, (220, 200, 80, 255))
    elif glyph == "key2":
        draw_ring(canvas, 18, 32, 10, 4, fg)
        draw_line(canvas, 27, 32, 54, 32, fg, 4)
        draw_line(canvas, 48, 32, 48, 42, fg, 3)
        draw_line(canvas, 54, 32, 54, 40, fg, 3)
    elif glyph == "bolt2":
        draw_poly(canvas, [(34, 8), (16, 36), (28, 36), (24, 56), (48, 28), (32, 28)], fg)
    elif glyph == "graduation":
        draw_poly(canvas, [(8, 26), (32, 14), (56, 26), (32, 38)], fg)
        draw_rect(canvas, 22, 32, 42, 46, fg)
        draw_line(canvas, 50, 26, 50, 40, fg, 2)
        draw_circle(canvas, 50, 42, 3, fg)
    elif glyph == "dice":
        draw_rect(canvas, 12, 12, 52, 52, fg)
        for x, y in [(20, 20), (32, 32), (44, 44), (20, 44), (44, 20)]:
            draw_circle(canvas, x, y, 3, (20, 20, 30, 255))
    elif glyph == "infinity":
        draw_ring(canvas, 20, 32, 10, 4, fg)
        draw_ring(canvas, 44, 32, 10, 4, fg)
    elif glyph == "question":
        # ?
        draw_ring(canvas, 32, 24, 10, 4, fg)
        draw_line(canvas, 32, 30, 32, 42, fg, 4)
        draw_circle(canvas, 32, 50, 3, fg)
    elif glyph == "exclaim":
        draw_rect(canvas, 28, 10, 36, 40, fg)
        draw_circle(canvas, 32, 50, 4, fg)
    elif glyph == "compass":
        draw_ring(canvas, c, c, 22, 3, fg)
        draw_poly(canvas, [(32, 14), (36, 32), (32, 28), (28, 32)], (220, 60, 60, 255))
        draw_poly(canvas, [(32, 50), (36, 32), (32, 36), (28, 32)], fg)
        draw_circle(canvas, c, c, 2, fg)
    # --- 0.4.0 ---
    elif glyph == "ai_chip":
        draw_rect(canvas, 14, 14, 50, 50, fg)
        draw_rect(canvas, 22, 22, 42, 42, (20, 20, 30, 255))
        # "AI" внутри
        draw_text_like(canvas, "EX", 20, 26, fg)  # пиксельный AI/EX
        for i in range(18, 49, 8):
            draw_rect(canvas, i, 8, i + 4, 14, fg)
            draw_rect(canvas, i, 50, i + 4, 56, fg)
    elif glyph == "bot":
        draw_rect(canvas, 14, 22, 50, 50, fg)
        # антенна
        draw_line(canvas, 32, 22, 32, 12, fg, 3)
        draw_circle(canvas, 32, 10, 3, fg)
        # глаза
        draw_circle(canvas, 24, 34, 4, (40, 200, 240, 255))
        draw_circle(canvas, 40, 34, 4, (40, 200, 240, 255))
        # рот
        draw_rect(canvas, 22, 42, 42, 46, (20, 20, 30, 255))
    elif glyph == "qrcode":
        draw_rect(canvas, 10, 10, 54, 54, fg)
        # белый фон внутри
        draw_rect(canvas, 12, 12, 52, 52, (250, 250, 250, 255))
        # пиксельный QR-узор
        for x, y in [(14, 14), (16, 14), (18, 14), (14, 16), (18, 16), (14, 18), (16, 18), (18, 18),
                     (42, 14), (44, 14), (46, 14), (42, 16), (46, 16), (42, 18), (44, 18), (46, 18),
                     (14, 42), (16, 42), (18, 42), (14, 44), (18, 44), (14, 46), (16, 46), (18, 46),
                     (26, 26), (28, 30), (32, 28), (36, 32), (30, 36), (40, 40), (36, 44), (44, 48)]:
            draw_rect(canvas, x, y, x + 2, y + 2, (20, 20, 30, 255))
    elif glyph == "barcode":
        for x, w in [(10, 2), (14, 4), (20, 2), (24, 1), (28, 3), (34, 2), (38, 4), (44, 1), (48, 2), (52, 4)]:
            draw_rect(canvas, x, 14, x + w, 50, fg)
    elif glyph == "antenna":
        # сигналы (верхние полукольца)
        for r, w in ((10, 3), (18, 3), (26, 3)):
            draw_ring(canvas, 32, 28, r, w, fg)
        restore_rect(canvas, bg_snapshot, 0, 28, 63, 63)
        # мачта рисуется ПОСЛЕ среза — раньше она стиралась целиком
        draw_rect(canvas, 28, 30, 36, 56, fg)
    elif glyph == "satellite":
        draw_circle(canvas, c, c, 8, fg)
        draw_poly(canvas, [(8, 8), (24, 24), (20, 28), (4, 12)], fg)
        draw_poly(canvas, [(56, 56), (40, 40), (44, 36), (60, 52)], fg)
        draw_rect(canvas, 28, 18, 36, 26, fg)
        draw_rect(canvas, 28, 38, 36, 46, fg)
    elif glyph == "microscope":
        draw_circle(canvas, 22, 18, 6, fg)
        draw_rect(canvas, 20, 22, 24, 36, fg)
        draw_rect(canvas, 16, 36, 30, 42, fg)
        draw_poly(canvas, [(30, 22), (44, 36), (40, 40), (26, 26)], fg)
        draw_rect(canvas, 14, 50, 50, 56, fg)
    elif glyph == "telescope":
        draw_poly(canvas, [(10, 50), (44, 16), (54, 26), (20, 60)], fg)
        draw_rect(canvas, 6, 54, 18, 58, fg)
        draw_circle(canvas, 50, 20, 5, (255, 255, 200, 255))
    elif glyph == "magnet":
        draw_poly(canvas, [(12, 10), (52, 10), (52, 36), (40, 36), (40, 22), (24, 22), (24, 36), (12, 36)], fg)
        draw_rect(canvas, 12, 36, 24, 50, (220, 60, 60, 255))
        draw_rect(canvas, 40, 36, 52, 50, (220, 60, 60, 255))
    elif glyph == "cloud_rain":
        draw_circle(canvas, 25, 26, 11, fg)
        draw_circle(canvas, 36, 22, 13, fg)
        draw_circle(canvas, 45, 28, 10, fg)
        draw_rect(canvas, 20, 26, 50, 36, fg)
        for x in (22, 30, 38, 46):
            draw_line(canvas, x, 42, x - 2, 52, (100, 180, 240, 255), 2)
    elif glyph == "cloud_snow":
        draw_circle(canvas, 25, 26, 11, fg)
        draw_circle(canvas, 36, 22, 13, fg)
        draw_circle(canvas, 45, 28, 10, fg)
        draw_rect(canvas, 20, 26, 50, 36, fg)
        for x, y in [(24, 46), (32, 50), (40, 46), (28, 54), (36, 54)]:
            draw_circle(canvas, x, y, 2, (240, 240, 255, 255))
    elif glyph == "sun_cloud":
        # солнце слева
        draw_circle(canvas, 22, 22, 9, (255, 220, 80, 255))
        for ang in (0, 45, 90, 135, 180, 225, 270, 315):
            x = int(22 + math.cos(math.radians(ang)) * 14)
            y = int(22 + math.sin(math.radians(ang)) * 14)
            draw_circle(canvas, x, y, 2, (255, 220, 80, 255))
        # облако справа
        draw_circle(canvas, 36, 38, 12, fg)
        draw_circle(canvas, 46, 36, 10, fg)
        draw_rect(canvas, 30, 38, 52, 48, fg)
    elif glyph == "wind":
        for y, length in ((22, 36), (32, 44), (42, 30)):
            draw_line(canvas, 10, y, 10 + length, y, fg, 3)
            draw_circle(canvas, 10 + length + 2, y, 3, fg)
    elif glyph == "tornado":
        for i, w in enumerate([42, 36, 30, 24, 18, 12, 6]):
            y = 12 + i * 6
            draw_rect(canvas, c - w // 2, y, c + w // 2, y + 4, fg)
    elif glyph == "palm":
        draw_rect(canvas, 30, 30, 36, 56, (90, 60, 30, 255))
        # листья
        draw_poly(canvas, [(33, 30), (12, 18), (10, 26), (28, 26)], fg)
        draw_poly(canvas, [(33, 30), (54, 18), (56, 26), (38, 26)], fg)
        draw_poly(canvas, [(33, 30), (22, 8), (32, 8)], fg)
        draw_poly(canvas, [(33, 30), (44, 8), (34, 8)], fg)
    elif glyph == "cactus":
        draw_rect(canvas, 28, 16, 36, 56, fg)
        draw_rect(canvas, 12, 30, 28, 36, fg)
        draw_rect(canvas, 12, 22, 18, 36, fg)
        draw_rect(canvas, 36, 26, 52, 32, fg)
        draw_rect(canvas, 46, 16, 52, 32, fg)
    elif glyph == "pine":
        draw_poly(canvas, [(32, 6), (20, 22), (28, 22), (16, 36), (28, 36), (12, 50), (52, 50), (36, 36), (48, 36), (36, 22), (44, 22)], fg)
        draw_rect(canvas, 28, 50, 36, 58, (90, 60, 30, 255))
    elif glyph == "footprint":
        draw_circle(canvas, 18, 24, 7, fg)
        draw_circle(canvas, 14, 14, 3, fg)
        draw_circle(canvas, 20, 12, 3, fg)
        draw_circle(canvas, 26, 16, 3, fg)
        draw_circle(canvas, 44, 44, 8, fg)
        draw_circle(canvas, 40, 32, 3, fg)
        draw_circle(canvas, 48, 30, 3, fg)
        draw_circle(canvas, 54, 36, 3, fg)
    elif glyph == "cat":
        draw_circle(canvas, c, 34, 18, fg)
        draw_poly(canvas, [(16, 22), (22, 32), (12, 32)], fg)
        draw_poly(canvas, [(48, 22), (52, 32), (42, 32)], fg)
        draw_circle(canvas, 26, 32, 2, (20, 20, 30, 255))
        draw_circle(canvas, 38, 32, 2, (20, 20, 30, 255))
        draw_poly(canvas, [(30, 38), (34, 38), (32, 42)], (240, 100, 130, 255))
    elif glyph == "dog":
        draw_circle(canvas, c, 36, 18, fg)
        draw_poly(canvas, [(12, 18), (24, 30), (16, 38)], fg)
        draw_poly(canvas, [(52, 18), (40, 30), (48, 38)], fg)
        draw_circle(canvas, 26, 34, 2, (20, 20, 30, 255))
        draw_circle(canvas, 38, 34, 2, (20, 20, 30, 255))
        draw_circle(canvas, 32, 42, 3, (20, 20, 30, 255))
    elif glyph == "fish":
        draw_poly(canvas, [(8, 32), (40, 18), (52, 32), (40, 46)], fg)
        draw_poly(canvas, [(48, 32), (60, 22), (60, 42)], fg)
        draw_circle(canvas, 18, 28, 2, (20, 20, 30, 255))
    elif glyph == "bird":
        draw_circle(canvas, 22, 24, 12, fg)
        draw_poly(canvas, [(22, 22), (40, 18), (44, 32), (24, 32)], fg)
        draw_poly(canvas, [(32, 18), (38, 22), (32, 24)], (240, 180, 40, 255))
        draw_circle(canvas, 18, 22, 2, (20, 20, 30, 255))
        draw_line(canvas, 24, 36, 22, 50, fg, 2)
        draw_line(canvas, 28, 36, 30, 50, fg, 2)
    elif glyph == "paw":
        draw_circle(canvas, 16, 30, 6, fg)
        draw_circle(canvas, 26, 22, 6, fg)
        draw_circle(canvas, 38, 22, 6, fg)
        draw_circle(canvas, 48, 30, 6, fg)
        draw_circle(canvas, 32, 44, 12, fg)
    elif glyph == "smile":
        draw_circle(canvas, c, c, 24, fg)
        draw_circle(canvas, 24, 26, 3, (20, 20, 30, 255))
        draw_circle(canvas, 40, 26, 3, (20, 20, 30, 255))
        # улыбка
        for x in range(22, 43, 1):
            y = int(38 + math.sin((x - 22) / 20 * math.pi) * 6)
            put_px(canvas, x, y, (20, 20, 30, 255))
            put_px(canvas, x, y + 1, (20, 20, 30, 255))
    elif glyph == "sad":
        draw_circle(canvas, c, c, 24, fg)
        draw_circle(canvas, 24, 26, 3, (20, 20, 30, 255))
        draw_circle(canvas, 40, 26, 3, (20, 20, 30, 255))
        for x in range(22, 43, 1):
            y = int(46 - math.sin((x - 22) / 20 * math.pi) * 6)
            put_px(canvas, x, y, (20, 20, 30, 255))
            put_px(canvas, x, y + 1, (20, 20, 30, 255))
    elif glyph == "wink":
        draw_circle(canvas, c, c, 24, fg)
        draw_circle(canvas, 40, 26, 3, (20, 20, 30, 255))
        draw_line(canvas, 20, 26, 28, 26, (20, 20, 30, 255), 2)
        for x in range(22, 43, 1):
            y = int(38 + math.sin((x - 22) / 20 * math.pi) * 6)
            put_px(canvas, x, y, (20, 20, 30, 255))
    elif glyph == "cool":
        draw_circle(canvas, c, c, 24, fg)
        draw_rect(canvas, 16, 22, 30, 30, (20, 20, 30, 255))
        draw_rect(canvas, 34, 22, 48, 30, (20, 20, 30, 255))
        draw_rect(canvas, 30, 26, 34, 28, (20, 20, 30, 255))
        for x in range(22, 43, 1):
            y = int(38 + math.sin((x - 22) / 20 * math.pi) * 4)
            put_px(canvas, x, y, (20, 20, 30, 255))
    elif glyph == "notes":
        draw_line(canvas, 22, 12, 22, 46, fg, 3)
        draw_line(canvas, 42, 8, 42, 42, fg, 3)
        draw_line(canvas, 22, 12, 42, 8, fg, 2)
        draw_circle(canvas, 18, 46, 6, fg)
        draw_circle(canvas, 38, 42, 6, fg)
    elif glyph == "drum":
        draw_rect(canvas, 10, 22, 54, 50, fg)
        draw_circle(canvas, 12, 32, 4, (20, 20, 30, 255))
        for x in (16, 24, 32, 40, 48):
            draw_line(canvas, x, 22, x - 4, 36, (20, 20, 30, 255), 2)
            draw_line(canvas, x, 50, x - 4, 36, (20, 20, 30, 255), 2)
        draw_line(canvas, 14, 16, 40, 8, fg, 2)
        draw_line(canvas, 50, 16, 24, 8, fg, 2)
    elif glyph == "guitar":
        draw_circle(canvas, 24, 42, 16, fg)
        draw_circle(canvas, 24, 42, 6, (20, 20, 30, 255))
        draw_line(canvas, 28, 32, 56, 6, fg, 5)
        draw_rect(canvas, 50, 4, 60, 14, fg)
    elif glyph == "vinyl":
        draw_circle(canvas, c, c, 26, fg)
        for r in (22, 18, 14, 10):
            draw_ring(canvas, c, c, r, 1, (60, 60, 60, 255))
        draw_circle(canvas, c, c, 6, (220, 60, 60, 255))
        draw_circle(canvas, c, c, 2, (20, 20, 30, 255))
    elif glyph == "film":
        draw_rect(canvas, 12, 12, 52, 52, fg)
        for y in (16, 28, 40, 52):
            draw_rect(canvas, 14, y, 18, y + 4, (20, 20, 30, 255))
            draw_rect(canvas, 46, y, 50, y + 4, (20, 20, 30, 255))
        draw_rect(canvas, 22, 18, 42, 30, (20, 20, 30, 255))
        draw_rect(canvas, 22, 34, 42, 46, (20, 20, 30, 255))
    elif glyph == "print":
        draw_rect(canvas, 16, 12, 48, 22, fg)
        draw_rect(canvas, 8, 22, 56, 44, fg)
        draw_rect(canvas, 16, 40, 48, 56, (250, 250, 250, 255))
        for y in (44, 48, 52):
            draw_line(canvas, 20, y, 44, y, (100, 100, 100, 255), 1)
        draw_circle(canvas, 48, 30, 2, (220, 60, 60, 255))
    elif glyph == "scan":
        draw_rect(canvas, 10, 16, 54, 48, fg)
        draw_rect(canvas, 14, 20, 50, 30, (250, 250, 250, 255))
        draw_line(canvas, 14, 32, 50, 32, (220, 60, 60, 255), 2)
    elif glyph == "fax":
        draw_rect(canvas, 8, 28, 56, 50, fg)
        draw_rect(canvas, 20, 16, 44, 28, fg)
        draw_rect(canvas, 12, 36, 32, 46, (20, 20, 30, 255))
        draw_circle(canvas, 46, 38, 2, (60, 200, 80, 255))
        draw_circle(canvas, 46, 44, 2, (220, 60, 60, 255))
    elif glyph == "drone":
        draw_circle(canvas, 16, 16, 6, fg)
        draw_circle(canvas, 48, 16, 6, fg)
        draw_circle(canvas, 16, 48, 6, fg)
        draw_circle(canvas, 48, 48, 6, fg)
        draw_line(canvas, 16, 16, 48, 48, fg, 3)
        draw_line(canvas, 48, 16, 16, 48, fg, 3)
        draw_rect(canvas, 24, 24, 40, 40, fg)
    elif glyph == "chat":
        draw_rect(canvas, 8, 14, 56, 42, fg)
        draw_poly(canvas, [(16, 42), (16, 54), (28, 42)], fg)
        for x in (22, 32, 42):
            draw_circle(canvas, x, 28, 2, (20, 20, 30, 255))
    elif glyph == "chat2":
        draw_poly(canvas, [(10, 14), (54, 14), (54, 40), (24, 40), (16, 50)], fg)
    elif glyph == "hashtag":
        draw_line(canvas, 16, 16, 12, 50, fg, 4)
        draw_line(canvas, 32, 16, 28, 50, fg, 4)
        draw_line(canvas, 8, 24, 50, 22, fg, 4)
        draw_line(canvas, 8, 40, 50, 38, fg, 4)
    elif glyph == "at":
        draw_ring(canvas, c, c, 22, 3, fg)
        draw_ring(canvas, c, c, 10, 3, fg)
        draw_line(canvas, 42, 32, 42, 44, fg, 3)
        draw_line(canvas, 42, 44, 50, 44, fg, 3)
    elif glyph == "share":
        draw_circle(canvas, 16, 14, 6, fg)
        draw_circle(canvas, 16, 50, 6, fg)
        draw_circle(canvas, 48, 32, 6, fg)
        draw_line(canvas, 22, 18, 42, 28, fg, 3)
        draw_line(canvas, 22, 46, 42, 36, fg, 3)
    elif glyph == "thumbsup":
        draw_rect(canvas, 10, 30, 22, 54, fg)
        draw_poly(canvas, [(22, 30), (32, 8), (40, 16), (36, 30)], fg)
        draw_rect(canvas, 22, 30, 50, 54, fg)
    elif glyph == "thumbsdown":
        draw_rect(canvas, 10, 10, 22, 34, fg)
        draw_poly(canvas, [(22, 34), (32, 56), (40, 48), (36, 34)], fg)
        draw_rect(canvas, 22, 10, 50, 34, fg)
    elif glyph == "dots3":
        for x in (16, 32, 48):
            draw_circle(canvas, x, c, 5, fg)
    elif glyph == "menu_lines":
        for y in (18, 32, 46):
            draw_rect(canvas, 12, y, 52, y + 4, fg)
    elif glyph == "grid":
        for r in (0, 1, 2):
            for col in (0, 1, 2):
                draw_rect(canvas, 12 + col * 14, 12 + r * 14, 22 + col * 14, 22 + r * 14, fg)
    elif glyph == "list":
        for y in (18, 30, 42, 54):
            draw_circle(canvas, 14, y, 2, fg)
            draw_rect(canvas, 20, y - 2, 52, y + 2, fg)
    elif glyph == "layers":
        draw_poly(canvas, [(32, 10), (54, 22), (32, 34), (10, 22)], fg)
        draw_poly(canvas, [(32, 26), (54, 38), (32, 50), (10, 38)], fg)
    elif glyph == "sliders":
        for y in (18, 32, 46):
            draw_line(canvas, 10, y, 54, y, fg, 2)
        draw_circle(canvas, 24, 18, 5, fg)
        draw_circle(canvas, 42, 32, 5, fg)
        draw_circle(canvas, 18, 46, 5, fg)
    elif glyph == "circle_filled":
        draw_circle(canvas, c, c, 22, fg)
    elif glyph == "halfmoon":
        draw_circle(canvas, c, c, 22, fg)
        draw_rect(canvas, c, 0, 64, 64, (20, 20, 30, 255))
    elif glyph == "yinyang":
        draw_circle(canvas, c, c, 24, fg)
        draw_rect(canvas, c, 0, 64, 64, (20, 20, 30, 255))
        draw_circle(canvas, c, 20, 12, fg)
        draw_circle(canvas, c, 44, 12, (20, 20, 30, 255))
        draw_circle(canvas, c, 20, 3, (20, 20, 30, 255))
        draw_circle(canvas, c, 44, 3, fg)
    elif glyph == "plus_circle":
        draw_circle(canvas, c, c, 22, fg)
        draw_rect(canvas, c - 12, c - 3, c + 12, c + 3, (20, 20, 30, 255))
        draw_rect(canvas, c - 3, c - 12, c + 3, c + 12, (20, 20, 30, 255))
    elif glyph == "minus_circle":
        draw_circle(canvas, c, c, 22, fg)
        draw_rect(canvas, c - 12, c - 3, c + 12, c + 3, (20, 20, 30, 255))
    elif glyph == "file":
        draw_poly(canvas, [(14, 8), (40, 8), (52, 20), (52, 56), (14, 56)], fg)
        draw_poly(canvas, [(40, 8), (40, 20), (52, 20)], (200, 200, 220, 255))
    elif glyph == "file_plus":
        draw_poly(canvas, [(14, 8), (40, 8), (52, 20), (52, 56), (14, 56)], fg)
        draw_poly(canvas, [(40, 8), (40, 20), (52, 20)], (200, 200, 220, 255))
        draw_rect(canvas, 30, 30, 34, 50, (60, 200, 100, 255))
        draw_rect(canvas, 22, 38, 42, 42, (60, 200, 100, 255))
    elif glyph == "file_code":
        draw_poly(canvas, [(14, 8), (40, 8), (52, 20), (52, 56), (14, 56)], fg)
        draw_line(canvas, 28, 36, 22, 44, (60, 180, 240, 255), 2)
        draw_line(canvas, 22, 44, 28, 50, (60, 180, 240, 255), 2)
        draw_line(canvas, 38, 36, 44, 44, (60, 180, 240, 255), 2)
        draw_line(canvas, 44, 44, 38, 50, (60, 180, 240, 255), 2)
    elif glyph == "file_zip":
        draw_poly(canvas, [(14, 8), (40, 8), (52, 20), (52, 56), (14, 56)], fg)
        draw_rect(canvas, 30, 14, 34, 50, (200, 150, 30, 255))
        for y in (16, 22, 28, 34, 40, 46):
            draw_rect(canvas, 30, y, 34, y + 2, (140, 100, 20, 255))
    # --- 0.7.9: новые глифы ---
    elif glyph == "anchor":
        draw_ring(canvas, 32, 14, 6, 3, fg)
        draw_line(canvas, 32, 20, 32, 50, fg, 4)
        draw_line(canvas, 22, 26, 42, 26, fg, 3)
        draw_ring(canvas, 32, 38, 18, 4, fg)
        restore_rect(canvas, bg_snapshot, 8, 14, 55, 37)
        draw_line(canvas, 32, 20, 32, 50, fg, 4)  # шток поверх среза
        draw_line(canvas, 22, 26, 42, 26, fg, 3)
        draw_ring(canvas, 32, 14, 6, 3, fg)
    elif glyph == "umbrella":
        draw_circle(canvas, 32, 30, 22, fg)
        restore_rect(canvas, bg_snapshot, 0, 30, 63, 63)
        draw_line(canvas, 32, 30, 32, 50, fg, 3)
        draw_line(canvas, 32, 50, 38, 54, fg, 3)
        draw_circle(canvas, 40, 52, 3, fg)
    elif glyph == "hourglass":
        draw_poly(canvas, [(18, 12), (46, 12), (32, 32)], fg)
        draw_poly(canvas, [(32, 32), (46, 52), (18, 52)], fg)
        draw_rect(canvas, 16, 8, 48, 12, fg)
        draw_rect(canvas, 16, 52, 48, 56, fg)
    elif glyph == "puzzle":
        draw_rect(canvas, 14, 20, 44, 50, fg)
        draw_circle(canvas, 44, 28, 6, fg)      # выступ справа
        draw_circle(canvas, 29, 20, 6, fg)      # выступ сверху
        draw_circle(canvas, 14, 42, 6, (30, 30, 40, 255))  # паз слева
    elif glyph == "planet":
        draw_circle(canvas, c, c, 15, fg)
        for t in range(0, 360, 8):
            rx, ry = 26, 8
            x = int(rx * math.cos(math.radians(t)))
            y = int(ry * math.sin(math.radians(t)))
            ang = 20
            xr = int(x * math.cos(math.radians(ang)) - y * math.sin(math.radians(ang))) + c
            yr = int(x * math.sin(math.radians(ang)) + y * math.cos(math.radians(ang))) + c
            draw_circle(canvas, xr, yr, 1, (240, 220, 160, 255))
    elif glyph == "ufo":
        draw_circle(canvas, 32, 26, 10, (150, 220, 250, 255))   # купол
        restore_rect(canvas, bg_snapshot, 0, 27, 63, 63)
        draw_poly(canvas, [(10, 34), (54, 34), (44, 26), (20, 26)], fg)
        draw_poly(canvas, [(10, 34), (54, 34), (46, 42), (18, 42)], fg)
        for x in (20, 32, 44):
            draw_circle(canvas, x, 38, 2, (255, 240, 120, 255))
        draw_circle(canvas, 32, 24, 7, (150, 220, 250, 255))
    elif glyph == "gem":
        draw_poly(canvas, [(18, 14), (46, 14), (54, 26), (32, 54), (10, 26)], fg)
        draw_line(canvas, 18, 14, 26, 26, (255, 255, 255, 120), 1)
        draw_line(canvas, 46, 14, 38, 26, (255, 255, 255, 120), 1)
        draw_line(canvas, 10, 26, 54, 26, (255, 255, 255, 120), 1)
        draw_line(canvas, 26, 26, 32, 54, (255, 255, 255, 120), 1)
        draw_line(canvas, 38, 26, 32, 54, (255, 255, 255, 120), 1)
    elif glyph == "megaphone":
        draw_poly(canvas, [(14, 26), (40, 14), (40, 46), (14, 36)], fg)
        draw_rect(canvas, 8, 26, 14, 36, fg)
        draw_rect(canvas, 16, 36, 24, 50, fg)
        for r in (6, 11):
            draw_ring(canvas, 44, 30, r, 2, fg)
        restore_rect(canvas, bg_snapshot, 38, 12, 44, 48)
        draw_poly(canvas, [(40, 14), (40, 46), (38, 45), (38, 15)], fg)
    elif glyph == "power":
        draw_ring(canvas, c, c + 2, 18, 5, fg)
        restore_rect(canvas, bg_snapshot, 24, 8, 40, 22)
        draw_line(canvas, 32, 8, 32, 30, fg, 5)
    elif glyph == "signal":
        for x, h in ((12, 10), (24, 20), (36, 32), (48, 44)):
            draw_rect(canvas, x, 54 - h, x + 8, 54, fg)
    elif glyph == "chart_bars":
        draw_line(canvas, 10, 54, 54, 54, fg, 2)
        draw_line(canvas, 10, 54, 10, 10, fg, 2)
        draw_rect(canvas, 16, 38, 24, 52, fg)
        draw_rect(canvas, 28, 24, 36, 52, fg)
        draw_rect(canvas, 40, 14, 48, 52, fg)
    elif glyph == "chart_line":
        draw_line(canvas, 10, 54, 54, 54, fg, 2)
        draw_line(canvas, 10, 54, 10, 10, fg, 2)
        pts = [(14, 46), (26, 32), (36, 40), (52, 16)]
        for i in range(len(pts) - 1):
            draw_line(canvas, *pts[i], *pts[i + 1], fg, 3)
        for x, y in pts:
            draw_circle(canvas, x, y, 3, fg)
    elif glyph == "chart_pie":
        draw_circle(canvas, c, c, 21, fg)
        # вырезаем правый верхний квадрант (восстанавливаем фон)
        for yy in range(c - 21, c + 1):
            for xx in range(c, c + 22):
                if (xx - c) ** 2 + (yy - c) ** 2 <= 441:
                    canvas[yy][xx] = bg_snapshot[yy][xx]
        # отделённый «ломтик» со сдвигом
        draw_poly(canvas, [(c + 5, c - 5), (c + 21, c - 5), (c + 5, c - 21)],
                  (255, 210, 90, 255))
    elif glyph == "chain":
        draw_ring(canvas, 24, 24, 11, 4, fg)
        draw_ring(canvas, 40, 40, 11, 4, fg)
        draw_line(canvas, 28, 28, 36, 36, fg, 4)
    elif glyph == "sword":
        draw_poly(canvas, [(40, 8), (54, 10), (56, 24), (26, 44), (20, 38)], fg)
        draw_line(canvas, 14, 32, 32, 50, (180, 140, 60, 255), 4)
        draw_line(canvas, 12, 46, 18, 52, (120, 80, 40, 255), 5)
    elif glyph == "potion":
        draw_rect(canvas, 28, 8, 36, 20, fg)
        draw_circle(canvas, 32, 38, 17, fg)
        draw_circle(canvas, 32, 42, 13, (180, 90, 220, 255))
        draw_circle(canvas, 26, 32, 3, (255, 255, 255, 140))
    elif glyph == "joystick":
        draw_circle(canvas, 32, 18, 9, fg)
        draw_line(canvas, 32, 26, 32, 42, fg, 5)
        draw_rect(canvas, 14, 42, 50, 54, fg)
        draw_poly(canvas, [(14, 42), (50, 42), (54, 54), (10, 54)], fg)
        draw_circle(canvas, 44, 47, 3, (220, 70, 70, 255))
    elif glyph == "moon_star":
        draw_circle(canvas, 28, 36, 17, fg)
        # серп: «выкусываем» смещённый круг, восстанавливая фон
        for yy in range(14, 46):
            for xx in range(20, 56):
                if (xx - 37) ** 2 + (yy - 30) ** 2 <= 15 * 15:
                    canvas[yy][xx] = bg_snapshot[yy][xx]
        pts = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            r = 8 if i % 2 == 0 else 3
            pts.append((int(48 + math.cos(angle) * r), int(16 + math.sin(angle) * r)))
        draw_poly(canvas, pts, (255, 230, 120, 255))
    elif glyph == "cursor":
        draw_poly(canvas, [(20, 10), (20, 46), (30, 38), (36, 52), (42, 48), (36, 36), (46, 34)], fg)
    elif glyph == "cloud_bolt":
        draw_circle(canvas, 25, 24, 11, fg)
        draw_circle(canvas, 36, 20, 13, fg)
        draw_circle(canvas, 45, 26, 10, fg)
        draw_rect(canvas, 20, 24, 50, 34, fg)
        draw_poly(canvas, [(36, 34), (26, 48), (33, 48), (29, 58), (42, 44), (35, 44)], (255, 220, 80, 255))
    elif glyph == "hexnut":
        pts = []
        for i in range(6):
            a = math.radians(60 * i - 30)
            pts.append((int(c + math.cos(a) * 22), int(c + math.sin(a) * 22)))
        draw_poly(canvas, pts, fg)
        draw_circle(canvas, c, c, 9, (30, 30, 40, 255))
    elif glyph == "radar":
        for r in (22, 15, 8):
            draw_ring(canvas, c, c, r, 2, fg)
        draw_line(canvas, c, c, 48, 16, fg, 2)
        draw_circle(canvas, 42, 40, 3, (120, 255, 140, 255))
    # --- 0.7.16: новые глифы ---
    elif glyph == "hearts":
        draw_circle(canvas, 21, 22, 8, fg)
        draw_circle(canvas, 33, 22, 8, fg)
        draw_poly(canvas, [(14, 26), (40, 26), (27, 42)], fg)
        small = (255, 255, 255, 255) if fg[:3] != (255, 255, 255) else (255, 170, 190, 255)
        draw_circle(canvas, 39, 37, 6, small)
        draw_circle(canvas, 48, 37, 6, small)
        draw_poly(canvas, [(34, 40), (53, 40), (43, 52)], small)
    elif glyph == "broken_heart":
        draw_circle(canvas, 24, 25, 10, fg)
        draw_circle(canvas, 40, 25, 10, fg)
        draw_poly(canvas, [(14, 30), (50, 30), (32, 53)], fg)
        # трещина-молния
        draw_line(canvas, 32, 15, 27, 25, (30, 30, 40, 255), 3)
        draw_line(canvas, 27, 25, 36, 33, (30, 30, 40, 255), 3)
        draw_line(canvas, 36, 33, 30, 46, (30, 30, 40, 255), 3)
    elif glyph == "valentine":
        draw_rect(canvas, 12, 18, 52, 48, fg)
        draw_line(canvas, 12, 18, 32, 34, (30, 30, 40, 255), 2)
        draw_line(canvas, 52, 18, 32, 34, (30, 30, 40, 255), 2)
        draw_circle(canvas, 28, 36, 4, (235, 60, 110, 255))
        draw_circle(canvas, 36, 36, 4, (235, 60, 110, 255))
        draw_poly(canvas, [(23, 38), (41, 38), (32, 48)], (235, 60, 110, 255))
    elif glyph == "butterfly":
        draw_circle(canvas, 22, 24, 11, fg)
        draw_circle(canvas, 42, 24, 11, fg)
        draw_circle(canvas, 24, 42, 8, fg)
        draw_circle(canvas, 40, 42, 8, fg)
        draw_rect(canvas, 30, 18, 34, 48, (60, 40, 30, 255))
        draw_line(canvas, 32, 18, 26, 8, (60, 40, 30, 255), 2)
        draw_line(canvas, 32, 18, 38, 8, (60, 40, 30, 255), 2)
        draw_circle(canvas, 22, 24, 4, (30, 30, 40, 255))
        draw_circle(canvas, 42, 24, 4, (30, 30, 40, 255))
    elif glyph == "clover":
        draw_circle(canvas, 24, 22, 9, fg)
        draw_circle(canvas, 40, 22, 9, fg)
        draw_circle(canvas, 32, 34, 9, fg)
        draw_line(canvas, 32, 40, 38, 56, (40, 120, 40, 255), 3)
    elif glyph == "candle":
        draw_rect(canvas, 25, 26, 39, 54, fg)
        draw_line(canvas, 32, 20, 32, 26, (80, 60, 40, 255), 2)
        draw_circle(canvas, 32, 15, 6, (255, 190, 70, 255))
        draw_circle(canvas, 32, 17, 3, (255, 240, 160, 255))
        draw_rect(canvas, 25, 30, 39, 33, (255, 255, 255, 90))
    elif glyph == "balloon":
        draw_circle(canvas, 32, 24, 14, fg)
        draw_circle(canvas, 27, 19, 4, (255, 255, 255, 130))
        draw_poly(canvas, [(29, 37), (35, 37), (32, 42)], fg)
        draw_line(canvas, 32, 42, 28, 50, (120, 120, 130, 255), 2)
        draw_line(canvas, 28, 50, 33, 58, (120, 120, 130, 255), 2)
    elif glyph == "cake":
        draw_rect(canvas, 14, 34, 50, 52, fg)
        draw_rect(canvas, 14, 30, 50, 38, (250, 245, 235, 255))
        for x in (22, 32, 42):
            draw_line(canvas, x, 18, x, 30, (250, 220, 120, 255), 3)
            draw_circle(canvas, x, 15, 2, (255, 120, 60, 255))
        draw_line(canvas, 14, 44, 50, 44, (30, 30, 40, 255), 2)
    elif glyph == "tulip":
        draw_circle(canvas, 25, 21, 7, fg)
        draw_circle(canvas, 39, 21, 7, fg)
        draw_circle(canvas, 32, 18, 7, fg)
        draw_poly(canvas, [(19, 22), (45, 22), (39, 36), (25, 36)], fg)
        draw_line(canvas, 32, 36, 32, 54, (40, 130, 50, 255), 3)
        draw_poly(canvas, [(32, 46), (20, 40), (24, 50)], (40, 130, 50, 255))
    elif glyph == "snowman":
        white = (246, 248, 252, 255)
        draw_circle(canvas, 32, 46, 12, white)
        draw_circle(canvas, 32, 30, 9, white)
        draw_circle(canvas, 32, 15, 7, white)
        draw_circle(canvas, 29, 14, 1, (30, 30, 40, 255))
        draw_circle(canvas, 35, 14, 1, (30, 30, 40, 255))
        draw_poly(canvas, [(32, 16), (40, 18), (32, 20)], (250, 140, 50, 255))
        for y in (28, 33):
            draw_circle(canvas, 32, y, 1, (30, 30, 40, 255))
        draw_line(canvas, 24, 27, 12, 20, (110, 70, 40, 255), 2)
        draw_line(canvas, 40, 27, 52, 20, (110, 70, 40, 255), 2)
    elif glyph == "kite":
        draw_poly(canvas, [(32, 8), (46, 24), (32, 40), (18, 24)], fg)
        draw_line(canvas, 32, 8, 32, 40, (30, 30, 40, 255), 1)
        draw_line(canvas, 18, 24, 46, 24, (30, 30, 40, 255), 1)
        draw_line(canvas, 32, 40, 26, 56, (150, 150, 160, 255), 2)
        draw_circle(canvas, 29, 46, 2, fg)
        draw_circle(canvas, 26, 52, 2, fg)
    elif glyph == "bee":
        draw_circle(canvas, 24, 18, 7, (235, 240, 255, 255))
        draw_circle(canvas, 40, 18, 7, (235, 240, 255, 255))
        draw_circle(canvas, 32, 36, 12, (250, 200, 60, 255))
        draw_rect(canvas, 24, 30, 40, 33, (35, 30, 25, 255))
        draw_rect(canvas, 22, 38, 42, 41, (35, 30, 25, 255))
        draw_circle(canvas, 32, 24, 5, (35, 30, 25, 255))
        draw_poly(canvas, [(30, 47), (34, 47), (32, 54)], (35, 30, 25, 255))
    elif glyph == "ladybug":
        draw_circle(canvas, 32, 36, 14, (225, 60, 60, 255))
        draw_circle(canvas, 32, 19, 7, (35, 30, 30, 255))
        draw_line(canvas, 32, 24, 32, 50, (35, 30, 30, 255), 2)
        for x, y in ((25, 32), (39, 32), (23, 42), (41, 42), (30, 46), (35, 38)):
            draw_circle(canvas, x, y, 2, (35, 30, 30, 255))
    elif glyph == "turtle":
        draw_circle(canvas, 30, 32, 14, fg)
        draw_circle(canvas, 48, 27, 5, (110, 160, 90, 255))
        for x, y in ((18, 43), (28, 47), (38, 46), (44, 40)):
            draw_circle(canvas, x, y, 3, (110, 160, 90, 255))
        draw_ring(canvas, 30, 32, 9, 2, (30, 60, 30, 255))
        draw_line(canvas, 24, 26, 37, 39, (30, 60, 30, 255), 1)
        draw_line(canvas, 37, 26, 24, 39, (30, 60, 30, 255), 1)
    elif glyph == "rabbit":
        draw_poly(canvas, [(23, 8), (29, 8), (29, 28), (23, 28)], fg)
        draw_poly(canvas, [(35, 8), (41, 8), (41, 28), (35, 28)], fg)
        draw_rect(canvas, 25, 10, 27, 26, (255, 190, 200, 255))
        draw_rect(canvas, 37, 10, 39, 26, (255, 190, 200, 255))
        draw_circle(canvas, 32, 38, 13, fg)
        draw_circle(canvas, 27, 35, 2, (30, 30, 40, 255))
        draw_circle(canvas, 37, 35, 2, (30, 30, 40, 255))
        draw_circle(canvas, 32, 41, 2, (255, 150, 170, 255))
        draw_line(canvas, 32, 43, 32, 46, (30, 30, 40, 255), 1)
    elif glyph == "duck":
        draw_circle(canvas, 29, 39, 13, fg)
        draw_circle(canvas, 41, 23, 8, fg)
        draw_poly(canvas, [(47, 21), (59, 24), (47, 28)], (250, 150, 50, 255))
        draw_circle(canvas, 42, 21, 2, (30, 30, 40, 255))
        draw_circle(canvas, 26, 39, 6, (255, 255, 255, 90))
    elif glyph == "penguin":
        draw_circle(canvas, 32, 38, 14, fg)
        draw_circle(canvas, 32, 20, 9, fg)
        draw_circle(canvas, 32, 40, 9, (245, 245, 250, 255))
        draw_circle(canvas, 29, 18, 2, (245, 245, 250, 255))
        draw_circle(canvas, 35, 18, 2, (245, 245, 250, 255))
        draw_poly(canvas, [(29, 22), (35, 22), (32, 27)], (250, 150, 50, 255))
        draw_poly(canvas, [(24, 52), (30, 52), (27, 57)], (250, 150, 50, 255))
        draw_poly(canvas, [(34, 52), (40, 52), (37, 57)], (250, 150, 50, 255))
    elif glyph == "glasses":
        draw_ring(canvas, 21, 34, 10, 3, fg)
        draw_ring(canvas, 43, 34, 10, 3, fg)
        draw_line(canvas, 30, 32, 34, 32, fg, 3)
        draw_line(canvas, 11, 32, 4, 26, fg, 3)
        draw_line(canvas, 53, 32, 60, 26, fg, 3)
    elif glyph == "tshirt":
        draw_poly(canvas, [(22, 12), (42, 12), (52, 20), (46, 30), (42, 26),
                            (42, 52), (22, 52), (22, 26), (18, 30), (12, 20)], fg)
        draw_line(canvas, 27, 12, 37, 12, (30, 30, 40, 255), 3)
    elif glyph == "ring_gem":
        draw_ring(canvas, 32, 40, 13, 4, fg)
        draw_poly(canvas, [(32, 10), (41, 19), (32, 28), (23, 19)], (160, 220, 250, 255))
        draw_line(canvas, 27, 19, 37, 19, (255, 255, 255, 140), 1)
    elif glyph == "crystal_ball":
        draw_circle(canvas, 32, 28, 17, (170, 200, 250, 255))
        draw_circle(canvas, 26, 22, 5, (255, 255, 255, 130))
        draw_poly(canvas, [(19, 47), (45, 47), (41, 56), (23, 56)], fg)
    elif glyph == "tophat":
        draw_rect(canvas, 21, 12, 43, 42, fg)
        draw_rect(canvas, 12, 42, 52, 48, fg)
        draw_rect(canvas, 21, 34, 43, 41, (170, 40, 50, 255))
    else:
        draw_circle(canvas, c, c, 19, fg)


def _blur_mask_1d(mask, radius, horizontal):
    """Один проход сепарабельного box-blur по маске 0..255."""
    size = len(mask)
    out = [[0] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            acc = n = 0
            for k in range(-radius, radius + 1):
                xx = x + k if horizontal else x
                yy = y if horizontal else y + k
                if 0 <= xx < size and 0 <= yy < size:
                    acc += mask[yy][xx]
                    n += 1
            out[y][x] = acc // n
    return out


def apply_neon_glow(canvas, bg_canvas, glow_rgb, radius=4, strength=0.85):
    """Добавляет свечение (bloom) вокруг глифа.
    Глиф = пиксели, отличающиеся от bg_canvas. Маска глифа размывается
    и аддитивно подмешивается цветом glow_rgb в фоновые пиксели."""
    size = len(canvas)
    mask = [[0] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            if canvas[y][x] != bg_canvas[y][x]:
                mask[y][x] = 255
    blur = _blur_mask_1d(mask, radius, True)
    blur = _blur_mask_1d(blur, radius, False)
    blur = _blur_mask_1d(blur, radius, True)
    blur = _blur_mask_1d(blur, radius, False)
    gr, gg, gb = glow_rgb
    for y in range(size):
        for x in range(size):
            g = blur[y][x]
            if not g or mask[y][x]:
                continue  # сам глиф не трогаем
            r, gc, b, a = canvas[y][x]
            if a == 0:
                continue  # прозрачные углы (circle/rounded) не светятся
            k = (g / 255.0) * strength
            canvas[y][x] = (
                min(255, int(r + gr * k)),
                min(255, int(gc + gg * k)),
                min(255, int(b + gb * k)),
                a,
            )


def downscale_canvas(canvas, target):
    """Уменьшает канву усреднением блоков (box-фильтр, с учётом альфы)."""
    src = len(canvas)
    out = []
    for ty in range(target):
        y0 = ty * src // target
        y1 = max(y0 + 1, (ty + 1) * src // target)
        row = []
        for tx in range(target):
            x0 = tx * src // target
            x1 = max(x0 + 1, (tx + 1) * src // target)
            r = g = b = a = n = 0
            for yy in range(y0, y1):
                for xx in range(x0, x1):
                    pr, pg, pb, pa = canvas[yy][xx]
                    # Взвешиваем цвет альфой, чтобы прозрачные края не темнили.
                    r += pr * pa
                    g += pg * pa
                    b += pb * pa
                    a += pa
                    n += 1
            if a:
                row.append((r // a, g // a, b // a, a // n))
            else:
                row.append((0, 0, 0, 0))
        out.append(row)
    return out


def _ico_image_bytes(canvas):
    """BITMAPINFOHEADER + XOR (BGRA снизу вверх) + AND-маска для одной канвы."""
    size = len(canvas)
    bit_count = 32
    xor_bytes = bytearray()
    for y in range(size - 1, -1, -1):
        for x in range(size):
            r, g, b, a = canvas[y][x]
            xor_bytes.extend([b, g, r, a])

    mask_row_bytes = ((size + 31) // 32) * 4
    and_mask = bytes(mask_row_bytes * size)

    return struct.pack(
        "<IIIHHIIIIII",
        40, size, size * 2, 1, bit_count, 0,
        len(xor_bytes) + len(and_mask), 0, 0, 0, 0,
    ) + bytes(xor_bytes) + and_mask


ICO_SIZES = (64, 48, 32, 24, 16)


def write_ico(path, preset_name, size=64, style_override=None):
    """Пишет МУЛЬТИРАЗМЕРНЫЙ .ico: рисует size×size, остальные размеры —
    даунскейл. Windows сам выберет подходящее изображение (таскбар,
    заголовок окна, проводник) — без «мыла» на мелких размерах.
    style_override — принудительный стиль фона (любой из ICON_STYLES),
    None — использовать стиль пресета."""
    preset = BUILTIN_ICONS[preset_name]
    bg1 = hex_to_rgb(preset["bg1"])
    bg2 = hex_to_rgb(preset["bg2"])
    fg = (*hex_to_rgb(preset["fg"]), 255)
    style = style_override if style_override in ICON_STYLES else preset.get("style", "gradient")

    canvas = make_canvas(size, bg1, bg2, style)
    if style == "neon":
        # Глиф — яркий акцент (bg2 «на максималках», чуть подбелённый) + bloom.
        accent = _neon_accent(bg2)
        fg = (*blend(accent, (255, 255, 255), 0.25), 255)
        bg_copy = [row[:] for row in canvas]
        draw_glyph(canvas, preset["glyph"], fg)
        apply_neon_glow(canvas, bg_copy, accent)
    else:
        draw_glyph(canvas, preset["glyph"], fg)

    canvases = [canvas] + [downscale_canvas(canvas, s) for s in ICO_SIZES if s < size]
    images = [_ico_image_bytes(cv) for cv in canvases]

    count = len(images)
    icon_dir = struct.pack("<HHH", 0, 1, count)
    entries = bytearray()
    offset = 6 + 16 * count
    for cv, img in zip(canvases, images):
        s = len(cv)
        entries += struct.pack(
            "<BBBBHHII",
            s if s < 256 else 0,
            s if s < 256 else 0,
            0, 0, 1, 32,
            len(img), offset,
        )
        offset += len(img)

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(icon_dir + bytes(entries) + b"".join(images))
    return Path(path)


def safe_icon_filename(name):
    result = []
    for ch in name.lower().replace(" ", "_"):
        if ch.isalnum() or ch in {"_", "-"}:
            result.append(ch)
    return "".join(result) or "icon"


def generate_builtin_icon_file(output_dir, preset_name, style_override=None):
    icons_dir = Path(output_dir) / "_builtin_icons"
    # Стиль входит в имя файла, чтобы кэш разных стилей не конфликтовал.
    suffix = f"_{style_override}" if style_override in ICON_STYLES else ""
    icon_path = icons_dir / f"{safe_icon_filename(preset_name)}{suffix}.ico"
    return write_ico(icon_path, preset_name, style_override=style_override)


def export_all_builtin_icons(output_dir):
    icons_dir = Path(output_dir) / "builtin_icons_export"
    icons_dir.mkdir(parents=True, exist_ok=True)
    created = []
    for name in BUILTIN_ICONS:
        icon_path = icons_dir / f"{safe_icon_filename(name)}.ico"
        write_ico(icon_path, name)
        created.append(icon_path)
    return icons_dir, created


# ----------------------- Qt-превью иконок -----------------------
def _preview_glyph_text(glyph):
    return {
        "terminal": ">_", "code": "{}", "package": "□", "rocket": "▲", "bolt": "⚡",
        "shield": "⬟", "star": "★", "gear": "⚙", "robot": "☻", "video": "▶",
        "music": "♪", "download": "↓", "folder": "▰", "magic": "✦", "cloud": "☁",
        "fire": "▲", "cube": "◆", "database": "DB", "lock": "▣", "key": "⚿",
        "camera": "●", "image": "▧", "book": "▤", "wrench": "⚒", "globe": "◎",
        "heart": "♥", "check": "✓", "cross": "×", "plus": "+", "gamepad": "✚",
        "bug": "●", "browser": "◉", "wave": "≈", "diamond": "◆", "play": "▶",
        "pause": "Ⅱ", "stop": "■", "upload": "↑", "scissors": "✂", "search": "⌕",
        "spark": "✦", "window": "▣",
        # 0.3.0
        "sun": "☀", "moon": "☾", "snowflake": "❄", "leaf": "🍃", "tree": "🌲",
        "flower": "✿", "coffee": "☕", "pizza": "🍕", "headphones": "🎧",
        "microphone": "🎤", "phone": "☎", "mail": "✉", "bell": "🔔",
        "calendar": "▦", "clock": "⏰", "flag": "⚑", "tag": "🏷",
        "bookmark": "🔖", "filter": "▼", "refresh": "↻", "eye": "👁",
        "trophy": "🏆", "medal": "🏅", "crown": "♛", "gift": "🎁", "cart": "🛒",
        "monitor": "🖥", "keyboard": "⌨", "mouse": "🖱", "cpu": "▤",
        "hdd": "▤", "usb": "USB", "car": "🚗", "plane": "✈", "ship": "⛵",
        "brush": "🖌", "pencil": "✎", "calculator": "🧮", "atom": "⚛",
        "flask": "⚗", "bulb": "💡", "speaker": "🔊", "pin": "📍",
        "wifi": "📶", "battery": "🔋", "hammer": "🔨",
        # 0.3.2
        "ball": "⚽", "basketball": "🏀", "tennis": "🎾", "target": "◎",
        "dumbbell": "🏋", "mountain": "⛰", "ocean": "≋", "rainbow": "🌈",
        "drop": "💧", "mushroom": "🍄", "bus": "🚌", "train": "🚆",
        "bicycle": "🚲", "taxi": "🚕", "burger": "🍔", "donut": "🍩",
        "apple": "🍎", "icecream": "🍦", "bottle": "🍼", "brain": "🧠",
        "server": "▤", "network": "⌬", "chip": "▦", "dollar": "$",
        "coin": "◉", "wallet": "💼", "bank": "🏦", "pill": "💊",
        "medcross": "✚", "arrow_up": "↑", "arrow_down": "↓",
        "arrow_left": "←", "arrow_right": "→", "triangle": "▲",
        "hexagon": "⬡", "ring": "○", "square_filled": "■",
        "home": "⌂", "door": "🚪", "key2": "🗝", "bolt2": "⚡",
        "graduation": "🎓", "dice": "🎲", "infinity": "∞",
        "question": "?", "exclaim": "!", "compass": "❖",
        # 0.4.0
        "ai_chip": "AI", "bot": "🤖", "qrcode": "▣", "barcode": "│║│║",
        "antenna": "📡", "satellite": "🛰", "microscope": "🔬",
        "telescope": "🔭", "magnet": "🧲", "cloud_rain": "🌧",
        "cloud_snow": "🌨", "sun_cloud": "⛅", "wind": "💨", "tornado": "🌪",
        "palm": "🌴", "cactus": "🌵", "pine": "🌲", "footprint": "👣",
        "cat": "🐱", "dog": "🐶", "fish": "🐟", "bird": "🐦", "paw": "🐾",
        "smile": "☺", "sad": "☹", "wink": "😉", "cool": "😎",
        "notes": "♫", "drum": "🥁", "guitar": "🎸", "vinyl": "💿",
        "film": "🎬", "print": "🖨", "scan": "🖨", "fax": "📠", "drone": "🛸",
        "chat": "💬", "chat2": "💭", "hashtag": "#", "at": "@", "share": "↗",
        "thumbsup": "👍", "thumbsdown": "👎", "dots3": "⋯", "menu_lines": "☰",
        "grid": "▦", "list": "☰", "layers": "▤", "sliders": "⫶",
        "circle_filled": "●", "halfmoon": "◐", "yinyang": "☯",
        "plus_circle": "⊕", "minus_circle": "⊖",
        "file": "📄", "file_plus": "📄+", "file_code": "{}", "file_zip": "🗜",
        # 0.7.9
        "anchor": "⚓", "umbrella": "☂", "hourglass": "⌛", "puzzle": "🧩",
        "planet": "🪐", "ufo": "🛸", "gem": "💎", "megaphone": "📣",
        "power": "⏻", "signal": "📶", "chart_bars": "📊", "chart_line": "📈",
        "chart_pie": "◔", "chain": "🔗", "sword": "⚔", "potion": "🧪",
        "joystick": "🕹", "moon_star": "🌙", "cursor": "➤",
        "cloud_bolt": "🌩", "hexnut": "⬡", "radar": "📡",
        # 0.7.16
        "hearts": "💕", "broken_heart": "💔", "valentine": "💌",
        "butterfly": "🦋", "clover": "🍀", "candle": "🕯", "balloon": "🎈",
        "cake": "🎂", "tulip": "🌷", "snowman": "⛄", "kite": "🪁",
        "bee": "🐝", "ladybug": "🐞", "turtle": "🐢", "rabbit": "🐰",
        "duck": "🦆", "penguin": "🐧", "glasses": "👓", "tshirt": "👕",
        "ring_gem": "💍", "crystal_ball": "🔮", "tophat": "🎩",
    }.get(glyph, glyph[:2].upper())


# Кэш превью: (имя, размер, стиль) → QPixmap. Каждое превью рисуется
# один раз за сессию — окно выбора и панели стилей открываются быстро.
_PREVIEW_PM_CACHE = {}


def make_preview_pixmap(preset_name, size=56, style_override=None):
    cache_key = (preset_name, size, style_override or "")
    cached = _PREVIEW_PM_CACHE.get(cache_key)
    if cached is not None:
        return cached
    preset = BUILTIN_ICONS.get(preset_name)
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    if not preset:
        return pm
    if style_override in ICON_STYLES:
        preset = dict(preset, style=style_override)

    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setRenderHint(QPainter.TextAntialiasing, True)

    bg1 = QColor(preset["bg1"])
    bg2 = QColor(preset["bg2"])
    fg = QColor(preset["fg"])
    style = preset.get("style", "gradient")

    pad = 3
    rect = (pad, pad, size - pad * 2, size - pad * 2)

    # Кисть фона по стилю пресета.
    if style == "neon":
        brush = QBrush(QColor(bg1.red() // 7, bg1.green() // 7, bg1.blue() // 7))
        # Глиф в превью — яркий акцент из bg2.
        m = max(bg2.red(), bg2.green(), bg2.blue()) or 1
        fg = QColor(
            min(255, bg2.red() * 255 // m),
            min(255, bg2.green() * 255 // m),
            min(255, bg2.blue() * 255 // m),
        )
    elif style == "flat":
        brush = QBrush(bg1)
    elif style == "vgrad":
        g = QLinearGradient(0, 0, 0, size)
        g.setColorAt(0.0, bg1)
        g.setColorAt(1.0, bg2)
        brush = QBrush(g)
    elif style == "radial":
        g = QRadialGradient(size / 2, size / 2, size * 0.62)
        g.setColorAt(0.0, bg2)
        g.setColorAt(1.0, bg1)
        brush = QBrush(g)
    elif style == "split":
        g = QLinearGradient(0, 0, size, size)
        g.setColorAt(0.0, bg1)
        g.setColorAt(0.499, bg1)
        g.setColorAt(0.501, bg2)
        g.setColorAt(1.0, bg2)
        brush = QBrush(g)
    else:  # gradient / circle / rounded
        g = QLinearGradient(0, 0, size, size)
        g.setColorAt(0.0, bg1)
        g.setColorAt(1.0, bg2)
        brush = QBrush(g)

    p.setBrush(brush)
    p.setPen(QColor("#222222"))
    if style == "circle":
        p.drawEllipse(rect[0], rect[1], rect[2], rect[3])
    elif style == "rounded":
        p.drawRoundedRect(rect[0], rect[1], rect[2], rect[3], int(size * 0.22), int(size * 0.22))
    else:
        p.drawRoundedRect(rect[0], rect[1], rect[2], rect[3], 8, 8)

    if style not in ("flat", "split", "neon"):
        hi = QRadialGradient(size * 0.32, size * 0.28, size * 0.6)
        hi.setColorAt(0.0, QColor(255, 255, 255, 80))
        hi.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(hi))
        p.setPen(Qt.NoPen)
        if style == "circle":
            p.drawEllipse(rect[0], rect[1], rect[2], rect[3])
        else:
            p.drawRoundedRect(rect[0], rect[1], rect[2], rect[3], 8, 8)

    font = QFont("Segoe UI", max(10, int(size * 0.34)))
    font.setBold(True)
    p.setFont(font)
    text = _preview_glyph_text(preset["glyph"])
    if style == "neon":
        # Имитация свечения: полупрозрачные копии текста со смещением.
        halo = QColor(fg)
        halo.setAlpha(60)
        p.setPen(halo)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            p.drawText(dx, dy, size, size, Qt.AlignCenter, text)
    p.setPen(fg)
    p.drawText(0, 0, size, size, Qt.AlignCenter, text)
    p.end()
    _PREVIEW_PM_CACHE[cache_key] = pm
    return pm


# ----------------------- Авто-оптимизация для Qt-байндингов -----------------------
# Полный список модулей PySide6 (актуальный для 6.x).
# Если модуль не в "используемых" — добавим его в --exclude-module.
QT_ALL_MODULES = {
    "QtCore", "QtGui", "QtWidgets", "QtNetwork", "QtPrintSupport", "QtSvg",
    "QtSvgWidgets", "QtOpenGL", "QtOpenGLWidgets", "QtConcurrent", "QtDBus",
    "QtXml", "QtTest", "QtSql", "QtUiTools", "QtStateMachine", "QtHelp",
    "QtMultimedia", "QtMultimediaWidgets", "QtSpatialAudio",
    "QtWebEngineCore", "QtWebEngineQuick", "QtWebEngineWidgets",
    "QtWebChannel", "QtWebSockets", "QtWebView", "QtHttpServer",
    "QtNetworkAuth", "QtBluetooth", "QtNfc",
    "QtSerialPort", "QtSerialBus",
    "QtCharts", "QtDataVisualization", "QtGraphs", "QtGraphsWidgets",
    "QtDesigner",
    "QtLocation", "QtPositioning", "QtSensors", "QtRemoteObjects",
    "QtScxml", "QtTextToSpeech",
    "QtPdf", "QtPdfWidgets",
    "QtQml", "QtQuick", "QtQuick3D", "QtQuickControls2", "QtQuickWidgets",
    "QtQuickTest", "QtCanvasPainter",
    "Qt3DAnimation", "Qt3DCore", "Qt3DExtras", "Qt3DInput",
    "Qt3DLogic", "Qt3DRender",
    "QtAsyncio", "QtAxContainer",
}

# Минимальный набор, который чаще всего тянется hooks автоматически даже когда не импортирован.
# Не исключаем их явно, чтобы не сломать сборку.
QT_KEEP_ALWAYS = {"QtCore", "QtGui", "QtWidgets"}

QT_BINDINGS = ("PySide6", "PyQt6", "PySide2", "PyQt5")

# Пакеты, которые на рантайме требуют ffmpeg/ffprobe.
# Если хотя бы один импортирован в проекте — авто-включаем bundle ffmpeg.
FFMPEG_DEPENDENT_PACKAGES = {
    "yt_dlp", "youtube_dl", "youtube_dlc",
    "moviepy", "imageio_ffmpeg", "pydub",
    "ffmpeg", "ffmpeg_python",
    "whisper", "openai_whisper", "faster_whisper",
}


def project_needs_ffmpeg(third_party_imports):
    """Возвращает True, если проект использует пакеты, которым нужен ffmpeg."""
    third_set = {n.replace("-", "_") for n in third_party_imports}
    return bool(third_set & FFMPEG_DEPENDENT_PACKAGES)


def detect_used_qt_modules(binding, dotted_imports):
    """Из множества dotted-импортов выбирает реально используемые подмодули Qt."""
    used = set()
    prefix = binding + "."
    for d in dotted_imports:
        if not d.startswith(prefix):
            continue
        # PySide6.QtCore  -> 'QtCore'
        # PySide6.QtGui.QPalette -> 'QtGui'
        parts = d[len(prefix):].split(".")
        first = parts[0]
        if first in QT_ALL_MODULES:
            used.add(first)
    return used


def build_qt_exclude_list(binding, used_modules):
    """Возвращает список (без префикса) Qt-модулей которые надо исключить."""
    keep = set(used_modules) | QT_KEEP_ALWAYS
    return sorted(QT_ALL_MODULES - keep)


# ============== Универсальный EXE: VC++ runtime + ffmpeg + crash logger ==============

# Список VC++ Redistributable DLL, нужных для запуска PySide6/любых нативных
# Python-расширений на «голой» Windows без установленного VC++ Redistributable.
VC_RUNTIME_DLLS = [
    "vcruntime140.dll",
    "vcruntime140_1.dll",
    "msvcp140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
    "concrt140.dll",
    "vccorlib140.dll",
]


def find_vc_runtime_dlls(arch="amd64"):
    """Ищет VC++ runtime DLL ПОД РАЗРЯДНОСТЬ ЦЕЛИ. Возвращает список (имя, путь).
    amd64 → 64-битный System32 (через Sysnative, если сборщик 32-битный);
    win32 → SysWOW64 на 64-бит ОС (или System32 на 32-бит ОС);
    arm64 → не бандлим (в System32 x64/ARM64 смесь — риск не той архитектуры)."""
    sysroot = Path(os.environ.get("SystemRoot", r"C:\Windows"))
    if arch == "arm64":
        return []
    if arch == "win32":
        wow = sysroot / "SysWOW64"
        search_dirs = [wow] if wow.exists() else [sysroot / "System32"]
    else:
        native = sysroot / "Sysnative"  # виден только 32-битному процессу на 64-бит ОС
        search_dirs = [native if native.exists() else sysroot / "System32"]
    found = []
    seen = set()
    for d in search_dirs:
        if not d.exists():
            continue
        for dll in VC_RUNTIME_DLLS:
            if dll in seen:
                continue
            p = d / dll
            if p.exists():
                found.append((dll, str(p)))
                seen.add(dll)
    return found


def find_ffmpeg_binaries():
    """Ищет ffmpeg.exe и ffprobe.exe в PATH. Возвращает список путей."""
    result = []
    for name in ("ffmpeg.exe", "ffprobe.exe"):
        p = shutil.which(name)
        if p:
            result.append(p)
    return result


# Runtime hook, который перехватывает все необработанные исключения и пишет
# полный traceback в файл рядом с exe + показывает нативный MessageBox.
# Запускается ДО загрузки приложения, поэтому работает даже если упал импорт PySide6.
CRASH_LOGGER_HOOK_CODE = r'''# -*- coding: utf-8 -*-
"""Crash logger runtime hook (auto-generated by Py To EXE Builder)."""
import sys
import os
import traceback
import datetime


def _crash_excepthook(exc_type, exc_value, exc_tb):
    try:
        if getattr(sys, "frozen", False):
            exe_path = sys.executable
            exe_dir = os.path.dirname(exe_path)
            exe_name = os.path.splitext(os.path.basename(exe_path))[0]
        else:
            exe_path = sys.argv[0] if sys.argv else "app"
            exe_dir = os.path.dirname(os.path.abspath(exe_path)) or "."
            exe_name = os.path.splitext(os.path.basename(exe_path))[0] or "app"

        log_path = os.path.join(exe_dir, exe_name + "_crash.log")
        try:
            f = open(log_path, "a", encoding="utf-8")
        except Exception:
            # Нет прав рядом с exe (Program Files) — пишем в LOCALAPPDATA/TEMP.
            import tempfile
            alt = os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
            log_path = os.path.join(alt, exe_name + "_crash.log")
            f = open(log_path, "a", encoding="utf-8")

        with f:
            f.write("=" * 70 + "\n")
            f.write("CRASH at " + datetime.datetime.now().isoformat() + "\n")
            f.write("Python: " + sys.version + "\n")
            f.write("Executable: " + str(exe_path) + "\n")
            f.write("Platform: " + sys.platform + "\n")
            f.write("=" * 70 + "\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
            f.write("\n")

        try:
            import ctypes
            short_tb = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
            msg = (
                "Программа аварийно завершилась.\n\n"
                + short_tb
                + "\n\nПолный отчёт сохранён в:\n" + log_path
            )
            ctypes.windll.user32.MessageBoxW(0, msg, "Ошибка приложения", 0x10)
        except Exception:
            pass
    except Exception:
        pass

    try:
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    except Exception:
        pass


sys.excepthook = _crash_excepthook

try:
    import threading
    if hasattr(threading, "excepthook"):
        def _thread_excepthook(args):
            _crash_excepthook(args.exc_type, args.exc_value, args.exc_traceback)
        threading.excepthook = _thread_excepthook
except Exception:
    pass
'''


def write_crash_logger_hook(workspace_dir):
    """Сохраняет runtime hook и возвращает путь к нему."""
    hooks_dir = Path(workspace_dir) / "_runtime_hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "crash_logger.py"
    hook_path.write_text(CRASH_LOGGER_HOOK_CODE, encoding="utf-8")
    return hook_path


# ----------------------- Воркеры -----------------------
class AnalyzeWorker(QThread):
    log = Signal(str)
    done = Signal(dict)   # {third, unknown, local, stdlib, py_files_count}
    failed = Signal(str)

    def __init__(self, main_file, project_dir, output_dir, parent=None):
        super().__init__(parent)
        self.main_file = Path(main_file)
        self.project_dir = Path(project_dir)
        self.output_dir = Path(output_dir)

    def run(self):
        try:
            self.log.emit("")
            self.log.emit("=== Анализ проекта ===")
            self.log.emit(f"Главный файл: {self.main_file}")
            self.log.emit(f"Папка проекта: {self.project_dir}")

            tops, dotted, py_files = collect_project_imports(self.project_dir)
            tops = sorted(tops)
            self.log.emit(f"Python-файлов найдено: {len(py_files)}")
            if len(py_files) >= MAX_SCAN_PY_FILES:
                self.log.emit(f"⚠ Достигнут лимит {MAX_SCAN_PY_FILES} файлов — анализ неполный. "
                              "Выбери папку проекта точнее (не корень диска).")
            self.log.emit(f"Импортов (top-level): {len(tops)}")
            self.log.emit(f"Импортов (полных dotted): {len(dotted)}")

            third, unknown, local, stdlib = [], [], [], []
            _local_names = local_module_names(self.project_dir, (self.main_file.parent,))  # кэш
            # Frozen-сборщик (EXE): find_spec внутри него ничего не находит —
            # классифицируем через настоящий python во внешнем процессе.
            ext_kinds = {}
            if getattr(sys, "frozen", False):
                real_py = real_python_exe()
                if real_py:
                    ext_kinds = classify_imports_external(
                        real_py, [n for n in tops if n not in _local_names])
                    self.log.emit(f"🐍 Классификация импортов через: {real_py}")
                else:
                    self.log.emit("⚠ Сборщик запущен как EXE и не нашёл python в системе — "
                                  "классификация импортов неточная.")
            for name in tops:
                if name in _local_names:
                    k = "local"
                elif name in ext_kinds:
                    k = ext_kinds[name]
                else:
                    k = classify_import(name, self.project_dir, _local_names)
                if k == "third-party":
                    third.append(name)
                elif k == "unknown":
                    unknown.append(name)
                elif k == "local":
                    local.append(name)
                else:
                    stdlib.append(name)

            self.log.emit("")
            self.log.emit("Внешние библиотеки:")
            self.log.emit(", ".join(third) if third else "нет")
            self.log.emit("")
            self.log.emit("Не найдены / динамические импорты:")
            self.log.emit(", ".join(unknown) if unknown else "нет")

            # Авто-определение используемых Qt-модулей.
            qt_summary = []
            for binding in QT_BINDINGS:
                if binding in third:
                    used = detect_used_qt_modules(binding, dotted)
                    if used:
                        qt_summary.append((binding, sorted(used)))
                    else:
                        qt_summary.append((binding, sorted(QT_KEEP_ALWAYS)))

            if qt_summary:
                self.log.emit("")
                self.log.emit("Авто-обнаружение Qt-модулей:")
                for binding, used in qt_summary:
                    self.log.emit(f"  {binding}: используется {len(used)} модулей → {', '.join(used)}")

            # Авто-детект tkinter (stdlib, поэтому отдельно от third-party).
            uses_tkinter = ("tkinter" in tops)
            if uses_tkinter:
                self.log.emit("")
                self.log.emit("🧩 Обнаружен tkinter → при сборке добавятся --collect-all tkinter "
                              "и hidden-imports (иначе «No module named tkinter» на чужом ПК).")

            req_lines = []
            for name in third:
                line = package_version(name)
                if line and line not in req_lines:
                    req_lines.append(line)

            self.output_dir.mkdir(parents=True, exist_ok=True)
            req_path = self.output_dir / "requirements_detected.txt"
            req_path.write_text(
                "\n".join(sorted(req_lines)) + ("\n" if req_lines else ""),
                encoding="utf-8",
            )

            report_path = self.output_dir / "analysis_report.txt"
            report = [
                f"{APP_NAME} v{APP_VERSION}",
                "=== Analysis Report ===",
                f"main_file={self.main_file}",
                f"project_dir={self.project_dir}",
                f"python_files={len(py_files)}",
                "", "[third-party]", *third,
                "", "[unknown]", *unknown,
                "", "[local]", *local,
                "", "[stdlib]", *stdlib,
                "", "[dotted_imports_sample]", *sorted(dotted)[:200],
            ]
            report_path.write_text("\n".join(report), encoding="utf-8")

            self.log.emit("")
            self.log.emit(f"Сохранено: {req_path}")
            self.log.emit(f"Сохранено: {report_path}")

            self.done.emit({
                "third": third, "unknown": unknown,
                "local": local, "stdlib": stdlib,
                "dotted": sorted(dotted),
                "qt_used": {b: u for b, u in qt_summary},
                "uses_tkinter": uses_tkinter,
                "py_files_count": len(py_files),
            })
        except Exception as exc:
            self.failed.emit(str(exc))


# ----------------------- Custom Python interpreter -----------------------

def _hide_window_kwargs():
    """Возвращает kwargs для subprocess: скрыть консольное окно (Win)."""
    kwargs = {}
    if sys.platform.startswith("win"):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        kwargs["startupinfo"] = si
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    return kwargs


_REAL_PYTHON_CACHE = []


def real_python_exe():
    """Путь к НАСТОЯЩЕМУ python.exe. Если сборщик не frozen — sys.executable.
    Если frozen (сам сборщик собран в EXE) — sys.executable указывает на
    сборщик, и `-m PyInstaller` запустил бы вторую копию GUI. Тогда ищем
    python через `py -3` и PATH. None, если не найден."""
    if not getattr(sys, "frozen", False):
        return sys.executable
    if _REAL_PYTHON_CACHE:
        return _REAL_PYTHON_CACHE[0]
    probe = "import sys; print(sys.executable)"
    cands = []
    if sys.platform.startswith("win") and shutil.which("py"):
        cands.append([shutil.which("py"), "-3", "-c", probe])
    for n in ("python", "python3"):
        w = shutil.which(n)
        if w:
            cands.append([w, "-c", probe])
    found = None
    for c in cands:
        try:
            r = subprocess.run(c, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=15, **_hide_window_kwargs())
            out = (r.stdout or "").strip().splitlines()
            if r.returncode == 0 and out and Path(out[-1]).is_file():
                found = out[-1]
                break
        except Exception:
            continue
    _REAL_PYTHON_CACHE.append(found)
    return found


_CLASSIFY_PROBE = r"""
import sys, json, os, importlib.util, sysconfig
names = json.loads(sys.stdin.read())
std = os.path.normcase(os.path.realpath(sysconfig.get_paths().get('stdlib', '')))
out = {}
for n in names:
    if n in sys.builtin_module_names:
        out[n] = 'stdlib'; continue
    try:
        s = importlib.util.find_spec(n)
    except Exception:
        out[n] = 'unknown'; continue
    if s is None:
        out[n] = 'unknown'; continue
    o = s.origin or ''
    if o in ('built-in', 'frozen'):
        out[n] = 'stdlib'; continue
    locs = list(s.submodule_search_locations or [])
    p = os.path.normcase(os.path.realpath(o if o and o != 'namespace' else (locs[0] if locs else '')))
    if 'site-packages' in p or 'dist-packages' in p:
        out[n] = 'third-party'
    elif std and p.startswith(std):
        out[n] = 'stdlib'
    else:
        out[n] = 'third-party'
print(json.dumps(out))
"""


def classify_imports_external(python_exe, names):
    """Классифицирует импорты в ДРУГОМ интерпретаторе. {name: kind} или {}."""
    if not names:
        return {}
    try:
        r = subprocess.run(
            [python_exe, "-c", _CLASSIFY_PROBE], input=json.dumps(list(names)),
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=60, cwd=tempfile.gettempdir(), **_hide_window_kwargs(),
        )
        if r.returncode == 0:
            return json.loads((r.stdout or "").strip().splitlines()[-1])
    except Exception:
        pass
    return {}


def missing_imports_external(python_exe, names):
    """Какие из import-имён НЕ находятся в python_exe (find_spec is None)."""
    if not names:
        return []
    kinds = classify_imports_external(python_exe, names)
    if not kinds:
        return list(names)
    return [n for n in names if kinds.get(n, "unknown") == "unknown"]


def detect_python_info(python_exe):
    """Запускает `python_exe -c ...` и возвращает dict с информацией:
       {ok, version, arch, has_pyinstaller, error}.
       python_exe='' или None → возвращает данные текущего sys.executable."""
    target = (python_exe or "").strip() or real_python_exe() or ""
    info = {"ok": False, "version": "", "arch": "", "has_pyinstaller": False,
            "has_tkinter": False, "error": "", "exe": target}
    p = Path(target) if target else None
    if not p or not p.is_file():
        info["error"] = "Файл не найден"
        return info

    probe = (
        "import sys, struct, importlib.util as u;"
        "print('VER=' + '.'.join(map(str, sys.version_info[:3])));"
        "print('ARCH=' + str(struct.calcsize('P') * 8));"
        "print('PI=' + ('1' if u.find_spec('PyInstaller') else '0'));"
        "print('TK=' + ('1' if u.find_spec('_tkinter') else '0'))"
    )
    try:
        r = subprocess.run(
            [target, "-c", probe],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=15, **_hide_window_kwargs(),
        )
        if r.returncode != 0:
            info["error"] = (r.stderr or r.stdout or "").strip()[:300] or f"код {r.returncode}"
            return info
        for line in (r.stdout or "").splitlines():
            line = line.strip()
            if line.startswith("VER="):
                info["version"] = line[4:]
            elif line.startswith("ARCH="):
                info["arch"] = line[5:] + "-bit"
            elif line.startswith("PI="):
                info["has_pyinstaller"] = (line[3:] == "1")
            elif line.startswith("TK="):
                info["has_tkinter"] = (line[3:] == "1")
        info["ok"] = True
    except subprocess.TimeoutExpired:
        info["error"] = "Таймаут запуска"
    except Exception as exc:
        info["error"] = str(exc)
    return info


# ----------------------- Portable embeddable Python -----------------------
# Скачиваются и кэшируются в app_base_dir() / "_portable_pythons".
# НЕ ставятся в систему. Удаляются вместе с папкой сборщика.

PORTABLE_PYTHONS = {
    "current": {
        "label": "🐍 Текущий Python (по умолчанию)",
        "version": None,
        "note": "Сборка через интерпретатор, в котором запущен сам сборщик.",
    },
    "win7": {
        "label": "🪟 Windows 7 / 8 / 8.1  →  Python 3.8.10 (авто-скачать)",
        "version": "3.8.10",
        "note": "Python 3.8.10 — последняя версия с поддержкой Windows 7. "
                "На Win7 целевой ПК должен иметь SP1 + KB2999226 (UCRT).",
    },
    "win10": {
        "label": "🪟 Windows 10+   →  Python 3.11.9 (авто-скачать)",
        "version": "3.11.9",
        "note": "Python 3.11 — стабильная актуальная версия для Win10/11.",
    },
    "win11": {
        "label": "🪟 Windows 11 (новейший)  →  Python 3.13.10 (авто-скачать)",
        "version": "3.13.10",
        "note": "Python 3.13 — последняя стабильная.",
    },
    "custom": {
        "label": "📁 Свой Python (указать путь)",
        "version": None,
        "note": "Использовать python.exe по указанному пути.",
    },
}

# Архитектуры Windows для авто-скачиваемого embeddable Python.
# Суффикс "zip" совпадает с именем файла на python.org:
#   python-{version}-embed-{zip}.zip
# "min" — минимальная версия Python, под которую эта архитектура
# вообще выпускается (arm64 embeddable появился только в 3.11).
PORTABLE_ARCHES = {
    "amd64": {"label": "x64 (64-бит, обычный ПК)",        "zip": "amd64", "min": (3, 5)},
    "win32": {"label": "x86 (32-бит, старые/слабые ПК)",  "zip": "win32", "min": (3, 5)},
    "arm64": {"label": "ARM64 (планшеты/ноутбуки на ARM)", "zip": "arm64", "min": (3, 11)},
}

# Версионные ограничения зависимостей для старых Python (Win7 = 3.8).
# Если в проекте detected эти пакеты — pip install получит пин-версию.
#
# Qt 6.2+ официально требует Windows 10. Последний PySide6, который реально
# работает на Win7 — 6.1.3 (декабрь 2021). PySide6 6.2.x уже падает с
# «DLL load failed while importing QtCore».
PY38_PINS = {
    "PySide6":    "PySide6==6.1.3",       # Последняя версия с поддержкой Win7
    "PySide2":    "PySide2",              # Qt 5.15 LTS — поддерживает Win7
    "PyQt6":      "PyQt6<6.2",            # PyQt6 6.2+ тоже требует Win10
    "PyQt5":      "PyQt5",                # Qt 5 — Win7 OK
    "shiboken6":  "shiboken6==6.1.3",     # совпадает с PySide6
    "numpy":      "numpy<1.25",           # 1.25+ требует Python 3.9+
    "pandas":     "pandas<2.1",           # 2.1+ требует Python 3.9+
    "scipy":      "scipy<1.11",
    "matplotlib": "matplotlib<3.8",
}

# Имена импортов != имена pip-пакетов. Маппинг для корректной установки.
IMPORT_TO_PIP = {
    "PIL":          "Pillow",
    "Crypto":       "pycryptodome",
    "Cryptodome":   "pycryptodomex",
    "OpenSSL":      "pyOpenSSL",
    "cv2":          "opencv-python",
    "yaml":         "PyYAML",
    "bs4":          "beautifulsoup4",
    "sklearn":      "scikit-learn",
    "skimage":      "scikit-image",
    "dateutil":     "python-dateutil",
    "dotenv":       "python-dotenv",
    "win32api":     "pywin32",
    "win32com":     "pywin32",
    "win32con":     "pywin32",
    "win32cred":    "pywin32",
    "win32gui":     "pywin32",
    "pywintypes":   "pywin32",
    "google":       "google-api-python-client",
    "jwt":          "PyJWT",
    "serial":       "pyserial",
    "usb":          "pyusb",
    "magic":        "python-magic",
    "ffmpeg":       "ffmpeg-python",
    "kivy":         "kivy",
}

# НЕ пытаемся ставить через pip эти имена — это либо stdlib C-расширения,
# либо инфраструктура сборки (PyInstaller и его deps приходят сами).
INSTALL_DENYLIST = {
    "PyInstaller", "pyinstaller", "pip", "setuptools", "wheel",
    "altgraph", "pefile", "pywin32_ctypes", "pywin32-ctypes",
    "distutils", "_distutils_hack", "_pyinstaller_hooks_contrib",
    "pkg_resources", "_distutils", "external",
    "future",  # обычно ставится зависимостью, имя часто конфликтное
}

# Названия, начинающиеся с _ или эти — почти всегда stdlib C-extensions.
STDLIB_C_EXT = {
    "_socket", "_ssl", "_brotli", "_tkinter", "_curses",
    "_overlapped", "_multiprocessing", "_decimal", "_ctypes",
    "_lzma", "_bz2", "_sqlite3", "_winapi",
    "select", "unicodedata", "readline",
}

# tkinter — stdlib, поэтому НЕ попадает в third_list и не идёт в --collect-all
# (тот применяется только к сторонним пакетам). Встроенный хук PyInstaller не
# всегда тянет tcl/tk рантайм → «No module named tkinter» на чужом ПК.
# Если проект использует tkinter, добавляем этот список как hidden-imports
# ВМЕСТЕ с явным `--collect-all tkinter`.
TKINTER_SUBMODULES = [
    "tkinter", "tkinter.ttk", "tkinter.filedialog", "tkinter.messagebox",
    "tkinter.simpledialog", "tkinter.scrolledtext", "tkinter.colorchooser",
    "tkinter.commondialog", "tkinter.font", "tkinter.dnd", "_tkinter",
]


def import_to_pip_name(import_name):
    """Маппит имя импорта в имя pip-пакета."""
    return IMPORT_TO_PIP.get(import_name, import_name)


def is_installable_dep(name):
    """True, если имя имеет смысл передавать в `pip install`."""
    if not name:
        return False
    if name.startswith("_"):
        return False  # stdlib C-extensions
    if name in STDLIB_C_EXT:
        return False
    if name in INSTALL_DENYLIST:
        return False
    return True


def _path_is_ascii(p):
    """True если в пути нет non-ASCII символов."""
    try:
        str(p).encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def portable_python_root():
    """Папка с portable Python-ами. ВСЕГДА в ASCII-пути.
    PyInstaller-хуки Qt падают, если PySide6 установлен в папке с кириллицей —
    subprocess не может корректно передать путь обратно (см. issue #7385).
    Поэтому держим кэш portable Python отдельно от папки сборщика/проекта."""
    # Базовая папка: %LOCALAPPDATA%\Py-To-EXE-Builder\portable_pythons\
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data and _path_is_ascii(local_app_data):
        return Path(local_app_data) / "Py-To-EXE-Builder" / "portable_pythons"
    # Fallback 1: домашняя папка пользователя (если ASCII).
    home = Path.home()
    if _path_is_ascii(home):
        return home / ".py_to_exe_builder" / "portable_pythons"
    # Fallback 2: рядом со сборщиком, ЕСЛИ его путь ASCII.
    base = app_base_dir()
    if _path_is_ascii(base):
        return base / "_portable_pythons"
    # Fallback 3: TEMP (всегда есть на Windows, обычно ASCII).
    tmp = os.environ.get("TEMP") or os.environ.get("TMP") or "C:\\Temp"
    return Path(tmp) / "Py-To-EXE-Builder" / "portable_pythons"


def portable_python_dir(version, arch="amd64"):
    return portable_python_root() / f"py-{version}-{arch}"


def is_portable_python_ready(version, arch="amd64"):
    """Готов ли кэшированный portable Python (есть .exe и pip)."""
    pdir = portable_python_dir(version, arch)
    if not (pdir / "python.exe").is_file():
        return False
    if not (pdir / "Lib" / "site-packages" / "pip").is_dir():
        return False
    return True


# ----------------- nicolaasjan/yt-dlp (Win7-compat standalone exe) -----------

NICOLAASJAN_REPO = "nicolaasjan/yt-dlp"
NICOLAASJAN_ASSET = "yt-dlp_win7.exe"


def nicolaasjan_cache_dir():
    """ASCII-папка для кэша скачанного yt-dlp_win7.exe."""
    base = portable_python_root().parent  # %LOCALAPPDATA%\Py-To-EXE-Builder
    return base / "nicolaasjan_ytdlp"


def nicolaasjan_cached_exe():
    return nicolaasjan_cache_dir() / NICOLAASJAN_ASSET


def nicolaasjan_cached_tag_file():
    return nicolaasjan_cache_dir() / "release_tag.txt"


def read_cached_nicolaasjan_tag():
    try:
        return nicolaasjan_cached_tag_file().read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def write_cached_nicolaasjan_tag(tag):
    try:
        nicolaasjan_cached_tag_file().write_text(tag, encoding="utf-8")
    except Exception:
        pass


USER_AGENT = f"Py-To-EXE-Builder/{APP_VERSION}"


class DownloadCancelled(Exception):
    pass


# Эталонные SHA256 скачиваемых файлов (url → hex). Если для url хеш задан —
# файл проверяется; иначе в лог пишется «⚠ SHA256 не проверено».
KNOWN_SHA256 = {}


def download_file(url, dest, on_progress=None, cancel_check=None, timeout=60):
    """Скачивает url → dest. on_progress(got, total). Возвращает sha256 (hex).
    cancel_check() → True прерывает скачивание (DownloadCancelled)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        total = int(resp.headers.get("Content-Length") or 0)
        got = 0
        with open(dest, "wb") as f:
            while True:
                if cancel_check and cancel_check():
                    raise DownloadCancelled("Отменено пользователем")
                buf = resp.read(64 * 1024)
                if not buf:
                    break
                f.write(buf)
                h.update(buf)
                got += len(buf)
                if on_progress:
                    on_progress(got, total)
    return h.hexdigest()


def verify_sha256(url, digest, log):
    """True, если хеш совпал или эталона нет (с предупреждением)."""
    expected = KNOWN_SHA256.get(url)
    if not expected:
        log(f"  ⚠ SHA256 не проверено (нет эталона): {Path(url).name} sha256={digest[:16]}…")
        return True
    if expected.lower() != digest.lower():
        log(f"❌ SHA256 НЕ совпал для {url}: ожидался {expected}, получен {digest}")
        return False
    log(f"  ✓ SHA256 совпал: {Path(url).name}")
    return True


def _make_temp_path(suffix):
    """Уникальный временный файл (вместо фиксированного имени в %TEMP%)."""
    fd, name = tempfile.mkstemp(prefix="py2exe_", suffix=suffix)
    os.close(fd)
    return Path(name)


SHIM_MARKER = "# Auto-generated by Py To EXE Builder."
SUBPROCESS_HIDE_SHIM_CODE = (
    SHIM_MARKER + "\n"
    "# Hides console windows for all subprocess calls in this Python\n"
    "# process (used to suppress upx.exe console flashes during UPX).\n"
    "import sys\n"
    "import os\n"
    "import subprocess as _sp\n"
    "if sys.platform.startswith('win'):\n"
    "    _orig_init = _sp.Popen.__init__\n"
    "    def _patched_init(self, *args, **kwargs):\n"
    "        if 'startupinfo' not in kwargs or kwargs['startupinfo'] is None:\n"
    "            si = _sp.STARTUPINFO()\n"
    "            si.dwFlags |= _sp.STARTF_USESHOWWINDOW\n"
    "            si.wShowWindow = _sp.SW_HIDE\n"
    "            kwargs['startupinfo'] = si\n"
    "        cf = kwargs.get('creationflags', 0) or 0\n"
    "        kwargs['creationflags'] = cf | _sp.CREATE_NO_WINDOW\n"
    "        return _orig_init(self, *args, **kwargs)\n"
    "    _sp.Popen.__init__ = _patched_init\n"
    "# Цепочка: выполняем «настоящий» sitecustomize пользователя, если он есть.\n"
    "_here = os.path.dirname(os.path.abspath(__file__))\n"
    "for _p in list(sys.path):\n"
    "    try:\n"
    "        if os.path.abspath(_p or '.') == _here:\n"
    "            continue\n"
    "        _f = os.path.join(_p, 'sitecustomize.py')\n"
    "        if os.path.isfile(_f):\n"
    "            with open(_f, encoding='utf-8') as _fh:\n"
    "                exec(compile(_fh.read(), _f, 'exec'), {'__name__': 'sitecustomize', '__file__': _f})\n"
    "            break\n"
    "    except Exception:\n"
    "        break\n"
)


class ConvertWorker(QThread):
    log = Signal(str)
    stage = Signal(str)       # текущий этап — в строку статуса
    done = Signal(int, str)   # exit_code (-2 = остановлено), exe_path_or_empty
    failed = Signal(str)

    def __init__(self, params, parent=None):
        super().__init__(parent)
        self.p = params  # dict с настройками
        self._proc = None
        self._cancelled = False
        self._info_cache = {}

    def cancel(self):
        """Останавливает сборку: флаг + убийство текущего процесса (с деревом)."""
        self._cancelled = True
        p = self._proc
        if p is not None and p.poll() is None:
            try:
                if sys.platform.startswith("win"):
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)],
                                   capture_output=True, timeout=15, **_hide_window_kwargs())
                else:
                    p.kill()
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass

    def _pyinfo(self, py_exe):
        """detect_python_info с кэшем на время сборки."""
        key = str(py_exe)
        if key not in self._info_cache:
            self._info_cache[key] = detect_python_info(key)
        return self._info_cache[key]

    def _write_subprocess_hide_shim(self, workspace_dir):
        """Создаёт sitecustomize.py с патчем subprocess.Popen, скрывающим окна.
        Возвращает путь к папке, которую надо добавить в PYTHONPATH."""
        shim_dir = Path(workspace_dir) / "_subprocess_hide_shim"
        shim_dir.mkdir(parents=True, exist_ok=True)
        shim_path = shim_dir / "sitecustomize.py"
        shim_path.write_text(SUBPROCESS_HIDE_SHIM_CODE, encoding="utf-8")
        return str(shim_dir)

    def _run_command(self, cmd, cwd=None):
        if self._cancelled:
            return -1
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # На Windows: скрываем все консольные окна (для самого PyInstaller
        # и для всех его дочерних процессов: upx.exe, pip и т.п.).
        if sys.platform.startswith("win"):
            # Подключаем sitecustomize-шим: при старте PyInstaller автоматически
            # импортируется sitecustomize, который патчит subprocess.Popen.
            # (embeddable Python игнорирует PYTHONPATH — для него шим кладётся
            # прямо в site-packages, см. run()).
            shim_dir = getattr(self, "_site_shim_dir", None)
            if shim_dir:
                cur_pp = env.get("PYTHONPATH", "")
                env["PYTHONPATH"] = shim_dir + os.pathsep + cur_pp if cur_pp else shim_dir

        process = subprocess.Popen(
            cmd, cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
            text=True, encoding="utf-8", errors="replace",
            env=env, **_hide_window_kwargs(),
        )
        self._proc = process
        try:
            assert process.stdout is not None
            for line in process.stdout:
                self.log.emit(line.rstrip())
            code = process.wait()
        finally:
            self._proc = None
        return -1 if self._cancelled else code

    # ---------- Portable Python setup ----------

    def _download_with_progress(self, url, dest, label="файл"):
        """Скачивает url → dest, эмитит прогресс в лог, проверяет SHA256 (если известен)."""
        state = {"last": -10}

        def prog(got, total):
            if total > 0:
                pct = int(got * 100 / total)
                if pct >= state["last"] + 10:
                    state["last"] = pct
                    self.log.emit(f"  ⬇ {label}: {pct}% ({got / 1048576:.1f}/{total / 1048576:.1f} MB)")

        digest = download_file(url, dest, prog, lambda: self._cancelled)
        if not verify_sha256(url, digest, self.log.emit):
            try:
                Path(dest).unlink()
            except Exception:
                pass
            raise RuntimeError(f"SHA256 не совпал: {label}")
        self.log.emit(f"  ✓ {label} скачан: {dest}")

    def _patch_embed_pth(self, pdir, version):
        """Раскомментировать 'import site' и добавить Lib/site-packages в python3X._pth."""
        # Имя файла: python38._pth, python311._pth, python313._pth
        major_minor = "".join(version.split(".")[:2])
        pth = pdir / f"python{major_minor}._pth"
        if not pth.exists():
            cands = list(pdir.glob("python*._pth"))
            if not cands:
                self.log.emit("⚠ python*._pth не найден — пропускаю патч.")
                return
            pth = cands[0]
        try:
            txt = pth.read_text(encoding="utf-8")
            new_txt = txt
            if "#import site" in new_txt:
                new_txt = new_txt.replace("#import site", "import site")
            elif "import site" not in new_txt:
                new_txt = new_txt.rstrip() + "\nimport site\n"
            if "Lib\\site-packages" not in new_txt and "Lib/site-packages" not in new_txt:
                new_txt = new_txt.rstrip() + "\nLib\\site-packages\n"
            if new_txt != txt:
                pth.write_text(new_txt, encoding="utf-8")
                self.log.emit(f"  ✓ Пропатчен {pth.name} (site-packages активирован)")
        except Exception as exc:
            self.log.emit(f"⚠ Не удалось пропатчить {pth.name}: {exc}")

    def _setup_portable_python(self, version, arch="amd64"):
        """Скачивает (если нужно) embed-сборку Python, ставит pip. Возвращает путь к python.exe или None."""
        arch_spec = PORTABLE_ARCHES.get(arch)
        if not arch_spec:
            self.log.emit(f"❌ Неизвестная архитектура: {arch}")
            return None
        try:
            mm = tuple(int(x) for x in version.split(".")[:2])
        except Exception:
            mm = (0, 0)
        if mm < arch_spec["min"]:
            self.log.emit(
                f"❌ Python {version} не выпускается под {arch} "
                f"(нужен ≥ {arch_spec['min'][0]}.{arch_spec['min'][1]}). "
                f"Выбери x64/x86 или более новую целевую ОС (Win10/11)."
            )
            return None

        host = platform.machine().lower()
        if sys.platform.startswith("win"):
            if arch == "arm64" and "arm" not in host:
                self.log.emit(f"❌ ARM64-Python нельзя запустить на этом ПК ({host}): PyInstaller не "
                              "умеет кросс-сборку. Собирай ARM64 на ARM-устройстве или выбери x64/x86.")
                return None
            if arch == "amd64" and host in ("x86", "i386", "i686"):
                self.log.emit("❌ x64-Python не запустится на 32-битной Windows. Выбери x86.")
                return None

        pdir = portable_python_dir(version, arch)
        pexe = pdir / "python.exe"

        if is_portable_python_ready(version, arch):
            self.log.emit(f"🐍 Portable Python {version} ({arch}) уже готов: {pdir}")
            return str(pexe)

        self.log.emit("")
        self.log.emit(f"=== Подготовка Python {version} ({arch}, embeddable) ===")
        self.log.emit(f"📁 Папка кэша (ASCII-only): {pdir}")
        pdir.mkdir(parents=True, exist_ok=True)

        # 1. Скачать и распаковать embed.zip (если ещё нет python.exe)
        if not pexe.exists():
            zip_suffix = arch_spec["zip"]
            url = f"https://www.python.org/ftp/python/{version}/python-{version}-embed-{zip_suffix}.zip"
            zip_path = pdir / "python-embed.zip"
            self.log.emit(f"⬇ Скачивание Python {version}: {url}")
            try:
                self._download_with_progress(url, zip_path, f"Python {version}")
            except Exception as exc:
                self.log.emit(f"❌ Не удалось скачать Python {version}: {exc}")
                return None
            self.log.emit("📦 Распаковка...")
            try:
                with zipfile.ZipFile(zip_path) as z:
                    z.extractall(pdir)
                zip_path.unlink(missing_ok=True)
            except Exception as exc:
                self.log.emit(f"❌ Не удалось распаковать: {exc}")
                return None
            self.log.emit(f"  ✓ Распаковано в {pdir}")

        # 2. Патч ._pth для активации site-packages
        self._patch_embed_pth(pdir, version)

        # 3. get-pip.py
        if not (pdir / "Lib" / "site-packages" / "pip").is_dir():
            # Главный bootstrap (https://bootstrap.pypa.io/get-pip.py) только для 3.10+.
            # Для 3.8/3.9 — версионный URL: https://bootstrap.pypa.io/pip/3.8/get-pip.py
            major_minor_tuple = tuple(int(x) for x in version.split(".")[:2])
            if major_minor_tuple < (3, 10):
                getpip_url = f"https://bootstrap.pypa.io/pip/{major_minor_tuple[0]}.{major_minor_tuple[1]}/get-pip.py"
            else:
                getpip_url = "https://bootstrap.pypa.io/get-pip.py"
            gp_path = pdir / "get-pip.py"
            self.log.emit(f"⬇ Скачивание get-pip.py: {getpip_url}")
            try:
                self._download_with_progress(getpip_url, gp_path, "get-pip.py")
            except Exception as exc:
                self.log.emit(f"❌ Не удалось скачать get-pip.py: {exc}")
                return None
            self.log.emit("📦 Установка pip...")
            self.stage.emit("Установка pip...")
            if self._run_command([str(pexe), str(gp_path), "--no-warn-script-location"]) != 0:
                self.log.emit("❌ get-pip.py завершился с ошибкой.")
                return None
            try:
                gp_path.unlink()
            except Exception:
                pass
            self.log.emit("  ✓ pip установлен")

        return str(pexe)

    def _resolve_build_pins(self, py_version_tuple, dep_names):
        """Превращает import-имена в pip-спецификаторы:
        - выкидывает denylist / stdlib C-extensions;
        - применяет алиас import→pip (PIL→Pillow и т.п.);
        - применяет пин-версию для старых Python (PySide6==6.1.3 и т.п.).
        Возвращает список pip-спецификаторов."""
        major, minor = py_version_tuple[:2]
        pins = PY38_PINS if (major, minor) <= (3, 8) else {}
        result = []
        seen_pkg = set()  # дедупликация (несколько win32* → один pywin32)
        skipped = []
        for name in dep_names:
            if not is_installable_dep(name):
                skipped.append(name)
                continue
            pkg = import_to_pip_name(name)
            if pkg in seen_pkg:
                continue
            seen_pkg.add(pkg)
            # Если в пинах указано имя ИМПОРТА — берём пин-спецификатор
            if name in pins:
                result.append(pins[name])
            elif pkg in pins:
                result.append(pins[pkg])
            else:
                result.append(pkg)
        return result, skipped

    def _install_project_deps(self, py_exe, workspace_dir):
        """Ставит НЕДОСТАЮЩИЕ зависимости проекта в выбранный python (список
        подтверждён пользователем: params["install_names"]). Без -U для чужого
        Python — не обновляем рабочее окружение пользователя. Хеш набора
        кэшируется в workspace: если не менялся — pip не запускается.
        Возвращает True даже если часть пакетов не поставилась (warning)."""
        names = self.p.get("install_names")
        if names is None:
            names = self.p.get("third") or []
        names = sorted({n for n in names if is_installable_dep(n)})
        if not names:
            self.log.emit("Нет зависимостей для установки.")
            return True

        info = self._pyinfo(py_exe)
        if not info["ok"]:
            self.log.emit(f"❌ Python не отвечает: {info['error']}")
            return False
        try:
            ver_tuple = tuple(int(x) for x in info["version"].split("."))
        except Exception:
            ver_tuple = (3, 8, 0)

        portable = self.p.get("python_mode") in ("win7", "win10", "win11")
        specs_all, skipped = self._resolve_build_pins(ver_tuple, names)
        dep_hash = hashlib.sha256("\n".join([str(py_exe)] + sorted(specs_all)).encode("utf-8")).hexdigest()
        hash_file = Path(workspace_dir) / "deps_hash.txt"
        try:
            if hash_file.read_text(encoding="utf-8").strip() == dep_hash:
                self.log.emit("✓ Набор зависимостей не менялся (кэш) — pip пропущен.")
                return True
        except Exception:
            pass

        self.log.emit("")
        self.log.emit("=== Установка зависимостей проекта ===")
        self.stage.emit("Установка зависимостей...")
        self.log.emit(f"🐍 Python {info['version']} ({info['arch']})")

        # Логируем алиасы и пины.
        alias_msgs = []
        pin_msgs = []
        for orig in names:
            pkg = import_to_pip_name(orig)
            pinned = (PY38_PINS.get(orig) or PY38_PINS.get(pkg)) if ver_tuple[:2] <= (3, 8) else None
            if pkg != orig:
                alias_msgs.append(f"{orig} → {pkg}")
            if pinned and pinned != pkg and pinned != orig:
                pin_msgs.append(f"{orig} → {pinned}")
        if alias_msgs:
            self.log.emit(f"  🔀 Алиасы import→pip: {', '.join(alias_msgs[:8])}"
                          + (f", +{len(alias_msgs) - 8}..." if len(alias_msgs) > 8 else ""))
        if pin_msgs:
            self.log.emit(f"  📌 Пин-версии для Python {info['version']}: {', '.join(pin_msgs)}")
            self.log.emit("  ℹ Для запуска на Windows 7 нужны старые версии библиотек "
                          "(Qt 6.2+ официально требует Win10).")

        missing = missing_imports_external(py_exe, names)
        if not missing:
            self.log.emit("✓ Все зависимости уже установлены.")
            try:
                hash_file.write_text(dep_hash, encoding="utf-8")
            except Exception:
                pass
            return True
        specs, _ = self._resolve_build_pins(ver_tuple, missing)
        self.log.emit(f"📦 Импортов: {len(names)}, отсутствует: {len(missing)}, к установке: {len(specs)}")

        if portable:
            # Своё окружение сборщика — можно обновлять pip/setuptools.
            self._run_command([py_exe, "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])
        upgrade = ["-U"] if portable else []

        if not specs:
            return True
        cmd = [py_exe, "-m", "pip", "install", *upgrade, "--no-warn-script-location"] + specs
        rc = self._run_command(cmd)
        failed = []
        if rc != 0 and not self._cancelled:
            self.log.emit("⚠ Часть зависимостей не поставилась. Пробую по одному...")
            for spec in specs:
                if self._cancelled:
                    break
                rc1 = self._run_command(
                    [py_exe, "-m", "pip", "install", *upgrade, "--no-warn-script-location", spec]
                )
                if rc1 != 0:
                    failed.append(spec)
            if failed:
                self.log.emit(f"⚠ Не удалось поставить (не критично, если это опциональные): {', '.join(failed)}")
                # НЕ возвращаем False — пусть PyInstaller всё равно попробует.
        if not failed and not self._cancelled:
            try:
                hash_file.write_text(dep_hash, encoding="utf-8")
            except Exception:
                pass
        self.log.emit("✓ Зависимости готовы")
        return True

    def _ensure_nicolaasjan_ytdlp(self):
        """Качает (или берёт из кэша) свежий yt-dlp_win7.exe от nicolaasjan/yt-dlp.
        Возвращает путь к exe или None при ошибке."""
        cache_dir = nicolaasjan_cache_dir()
        cache_dir.mkdir(parents=True, exist_ok=True)
        cached_exe = nicolaasjan_cached_exe()

        self.log.emit("")
        self.log.emit("=== Win7-режим: подготовка yt-dlp_win7.exe (nicolaasjan/yt-dlp) ===")

        # 1. Запрос GitHub API: получить tag и URL свежего ассета.
        api_url = f"https://api.github.com/repos/{NICOLAASJAN_REPO}/releases/latest"
        latest_tag = ""
        asset_url = ""
        try:
            req = urllib.request.Request(
                api_url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/vnd.github+json",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            latest_tag = (data.get("tag_name") or "").strip()
            for asset in data.get("assets") or []:
                if asset.get("name") == NICOLAASJAN_ASSET:
                    asset_url = asset.get("browser_download_url") or ""
                    break
            if not asset_url:
                self.log.emit(f"⚠ {NICOLAASJAN_ASSET} не найден в последнем релизе. "
                              f"Использую кэш если есть.")
        except Exception as exc:
            self.log.emit(f"⚠ GitHub API недоступен: {exc}. Использую кэш если есть.")

        cached_tag = read_cached_nicolaasjan_tag()

        # 2. Если кэш свежий — используем без скачивания.
        if cached_exe.is_file() and cached_tag and cached_tag == latest_tag:
            self.log.emit(f"📦 yt-dlp_win7.exe (cached, tag={cached_tag}): {cached_exe}")
            return str(cached_exe)

        # 3. Если нечего скачать (API не ответил) и кэш есть — используем старый.
        if not asset_url:
            if cached_exe.is_file():
                self.log.emit(f"📦 yt-dlp_win7.exe (cached, tag={cached_tag or '?'}): {cached_exe}")
                return str(cached_exe)
            self.log.emit("❌ Не удалось получить ни свежий, ни кэшированный yt-dlp_win7.exe.")
            return None

        # 4. Скачиваем свежую версию.
        self.log.emit(f"⬇ Скачивание {NICOLAASJAN_ASSET} (tag={latest_tag}): {asset_url}")
        tmp_path = cache_dir / f"{NICOLAASJAN_ASSET}.part"
        try:
            self._download_with_progress(asset_url, tmp_path, NICOLAASJAN_ASSET)
        except Exception as exc:
            self.log.emit(f"❌ Не удалось скачать: {exc}")
            if cached_exe.is_file():
                self.log.emit(f"📦 Использую старый кэш: {cached_exe}")
                return str(cached_exe)
            return None

        try:
            if cached_exe.exists():
                cached_exe.unlink()
            tmp_path.rename(cached_exe)
            write_cached_nicolaasjan_tag(latest_tag)
        except Exception as exc:
            self.log.emit(f"❌ Не удалось сохранить exe: {exc}")
            return None

        size_mb = cached_exe.stat().st_size / 1024 / 1024
        self.log.emit(f"  ✓ Готово: {cached_exe} ({size_mb:.1f} MB)")
        return str(cached_exe)

    def _resolve_build_python(self):
        """Возвращает путь к python.exe для сборки. None при ошибке."""
        mode = (self.p.get("python_mode") or "current").strip()

        if mode == "current":
            py = real_python_exe()
            if not py:
                self.log.emit("❌ Сборщик запущен как EXE, а python в системе не найден "
                              "(py -3 / PATH). Выбери «Свой Python» или portable-режим.")
                return None
            if py == sys.executable:
                self.log.emit(
                    f"🐍 Python для сборки: текущий "
                    f"({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})"
                )
            else:
                self.log.emit(f"🐍 Python для сборки (найден в системе): {py}")
            return py

        if mode == "custom":
            custom = (self.p.get("python_exe") or "").strip()
            if not custom or not Path(custom).is_file():
                self.log.emit("❌ Свой Python: путь не задан или файл не найден.")
                return None
            info = self._pyinfo(custom)
            if not info["ok"]:
                self.log.emit(f"❌ Свой Python не отвечает: {info['error']}")
                return None
            self.log.emit(f"🐍 Свой Python: {info['version']} ({info['arch']}) — {custom}")
            return custom

        spec = PORTABLE_PYTHONS.get(mode)
        if not spec or not spec.get("version"):
            self.log.emit(f"❌ Неизвестный режим Python: {mode}")
            return None
        arch = (self.p.get("build_arch") or "amd64").strip()
        return self._setup_portable_python(spec["version"], arch)

    def _ensure_pyinstaller(self):
        """Резолвит python_exe + ставит зависимости проекта + ставит PyInstaller."""
        py_exe = self._resolve_build_python()
        if not py_exe:
            return None  # ошибка — каллер обработает

        is_current = (py_exe == sys.executable)

        # Для portable/custom (и python, найденного frozen-сборщиком) — поставить зависимости.
        if not is_current:
            ws = project_workspace_dir(self.p["project_dir"])
            ws.mkdir(parents=True, exist_ok=True)
            if not self._install_project_deps(py_exe, ws):
                return None
        if self._cancelled:
            return None

        # Проверка PyInstaller.
        if is_current:
            has_pi = importlib.util.find_spec("PyInstaller") is not None
        else:
            info = self._pyinfo(py_exe)
            has_pi = bool(info["ok"] and info["has_pyinstaller"])

        if has_pi:
            self.log.emit("PyInstaller найден.")
            return py_exe

        if not self.p["install_pyinstaller"]:
            self.log.emit("PyInstaller не найден.")
            self.log.emit(f'Установи вручную: "{py_exe}" -m pip install -U pyinstaller')
            return None

        self.log.emit("PyInstaller не найден. Ставлю автоматически...")
        self.stage.emit("Установка PyInstaller...")
        if self._run_command([py_exe, "-m", "pip", "install", "-U", "pyinstaller"]) != 0:
            self.log.emit("❌ Не удалось установить PyInstaller.")
            return None
        return py_exe

    def _get_icon(self, workspace_dir):
        custom = (self.p["custom_icon"] or "").strip()
        if custom:
            return custom
        preset = (self.p["builtin_icon"] or "").strip()
        if not preset or preset == NO_BUILTIN_ICON or preset not in BUILTIN_ICONS:
            return ""
        style = (self.p.get("icon_style") or "").strip() or None
        path = generate_builtin_icon_file(workspace_dir, preset, style)
        style_txt = f" (стиль: {ICON_STYLE_LABELS.get(style, style)})" if style else ""
        self.log.emit(f"Встроенная иконка создана{style_txt}: {path}")
        return str(path)

    def run(self):
        try:
            main_file = Path(self.p["main_file"])
            project_dir = Path(self.p["project_dir"])
            output_dir = Path(self.p["output_dir"])
            app_name = self.p["app_name"]

            # Win7-режим: добавляем суффикс _win7 к имени и качаем bundled yt-dlp_win7.exe.
            is_win7_mode = (self.p.get("python_mode") == "win7")
            if is_win7_mode and not app_name.endswith("_win7"):
                app_name = f"{app_name}_win7"
                self.log.emit(f"🪟 Win7-режим: имя exe → {app_name}.exe")

            # Арх-суффикс для авто-скачиваемых Python (кроме amd64), чтобы
            # x86/ARM64-сборка не затирала x64-версию в той же папке вывода.
            build_arch = (self.p.get("build_arch") or "amd64").strip()
            if self.p.get("python_mode") in ("win7", "win10", "win11") and build_arch != "amd64":
                arch_tag = "_x86" if build_arch == "win32" else f"_{build_arch}"
                if not app_name.endswith(arch_tag):
                    app_name = f"{app_name}{arch_tag}"
                    self.log.emit(f"🏗 Арх. {build_arch}: имя exe → {app_name}.exe")

            self.stage.emit("Подготовка Python...")
            build_python = self._ensure_pyinstaller()
            if self._cancelled:
                self.done.emit(-2, "")
                return
            if not build_python:
                self.log.emit("Сборка остановлена: не удалось подготовить Python/PyInstaller.")
                self.done.emit(-1, "")
                return

            # ------- tkinter-пререквизит: проверяем целевой Python ЗАРАНЕЕ -------
            # embeddable/portable Python (режимы win7/win10/win11) идёт БЕЗ
            # tkinter/tcl/tk — тогда никакой --collect-all не спасёт. Предупреждаем
            # до сборки, а не после её падения.
            if self.p.get("uses_tkinter"):
                tk_info = self._pyinfo(build_python)
                if tk_info.get("ok") and not tk_info.get("has_tkinter"):
                    self.log.emit("")
                    self.log.emit("⚠ ВНИМАНИЕ: проект использует tkinter, но в выбранном Python "
                                  "нет модуля _tkinter (tcl/tk).")
                    self.log.emit("   Embeddable/portable Python (режимы win7/win10/win11) идёт БЕЗ "
                                  "tkinter. Для tkinter-приложения выбери обычный установленный "
                                  "Python («Текущий Python» или путь к полному python.exe).")
                    self.log.emit("   Иначе готовый exe упадёт с «No module named tkinter» несмотря "
                                  "на --collect-all.")

            workspace_dir = project_workspace_dir(project_dir)
            workspace_dir.mkdir(parents=True, exist_ok=True)
            icon = self._get_icon(workspace_dir)
            build_dir = workspace_dir / "build"
            spec_dir = workspace_dir / "spec"
            dist_dir = output_dir
            self.log.emit(f"Рабочая папка сборщика: {workspace_dir}")

            # Предупреждение про не-ASCII в пути: некоторые хуки PyInstaller
            # (особенно PySide6 хуки на Win) плохо работают с кириллическим путём.
            if not _path_is_ascii(project_dir):
                self.log.emit("")
                self.log.emit("⚠ Внимание: в пути проекта есть не-ASCII символы (кириллица и т.п.).")
                self.log.emit("  Это может вызвать ошибки PyInstaller-хуков (Qt и т.д.).")
                self.log.emit("  Если сборка упадёт — перенеси проект в ASCII-путь, например C:\\Projects\\.")

            # Создаём sitecustomize.py шим, который пропатчит subprocess внутри
            # PyInstaller-процесса: ВСЕ его вызовы (upx, pip, любые) пойдут со
            # скрытым окном. Это убирает мелькание чёрных консолей при UPX.
            if sys.platform.startswith("win"):
                self._site_shim_dir = self._write_subprocess_hide_shim(workspace_dir)
                # embeddable Python (._pth) игнорирует PYTHONPATH — кладём шим
                # прямо в его site-packages (только если там нет чужого sitecustomize).
                if self.p.get("python_mode") in ("win7", "win10", "win11"):
                    sp_shim = Path(build_python).parent / "Lib" / "site-packages" / "sitecustomize.py"
                    try:
                        if (not sp_shim.exists()
                                or sp_shim.read_text(encoding="utf-8", errors="ignore").startswith(SHIM_MARKER)):
                            sp_shim.parent.mkdir(parents=True, exist_ok=True)
                            sp_shim.write_text(SUBPROCESS_HIDE_SHIM_CODE, encoding="utf-8")
                    except Exception as exc:
                        self.log.emit(f"⚠ Не удалось установить шим скрытия окон: {exc}")
            else:
                self._site_shim_dir = None

            if self.p["clean"]:
                self.log.emit("")
                self.log.emit("Очистка старой сборки...")
                shutil.rmtree(build_dir, ignore_errors=True)
                shutil.rmtree(spec_dir, ignore_errors=True)
                old_exe = dist_dir / f"{app_name}.exe"
                if old_exe.exists():
                    try:
                        old_exe.unlink()
                    except Exception as exc:
                        self.log.emit(f"⚠ Не удалось удалить старый {old_exe.name} ({exc}). "
                                      "Закрой запущенный exe — иначе сборка упадёт с PermissionError.")

            self.stage.emit("Подготовка команды сборки...")
            cmd = [
                build_python, "-m", "PyInstaller",
                "--name", app_name,
                "--distpath", str(dist_dir),
                "--workpath", str(build_dir),
                "--specpath", str(spec_dir),
            ]

            max_compat = bool(self.p.get("max_compat"))
            auto_opt = bool(self.p.get("auto_optimize"))
            universal = bool(self.p.get("universal"))
            debug_mode = bool(self.p.get("debug_mode"))
            bundle_ffmpeg = bool(self.p.get("bundle_ffmpeg"))

            # В Win7-режиме НЕ бандлим ffmpeg: современные сборки крашатся
            # с 0xc0000005 на CPU без SSE4.1/AVX (Celeron T-серии и т.п.).
            # Пусть лучше не будет ffmpeg, чем popup-ошибка при каждом запуске.
            if is_win7_mode and bundle_ffmpeg:
                self.log.emit("")
                self.log.emit("🚫 Win7-режим: bundle ffmpeg ОТКЛЮЧЕН (современный ffmpeg крашится "
                              "на старых CPU без SSE4.1/AVX).")
                self.log.emit("   Если нужен MP3-экстракт — положи Win7-совместимый ffmpeg.exe "
                              "рядом с готовым EXE вручную.")
                bundle_ffmpeg = False

            onefile = self.p["onefile"] or max_compat or auto_opt or universal
            collect_all = self.p["collect_all"] or max_compat
            # Отладочный режим: НЕ windowed, чтобы видеть консоль и stdout/stderr.
            windowed = self.p["windowed"] and not debug_mode

            if onefile:
                cmd.append("--onefile")
            if windowed:
                cmd.append("--windowed")
            else:
                cmd.append("--console")
            if self.p["clean"]:
                cmd.append("--clean")
            # ВСЕГДА --noconfirm: stdin=DEVNULL, интерактивное подтверждение
            # перезаписи dist/ повесило бы/уронило бы сборку.
            cmd.append("--noconfirm")
            if icon:
                cmd.extend(["--icon", icon])

            # ------- Универсальный режим: VC++ runtime DLLs -------
            if universal:
                if self.p.get("python_mode") in ("win7", "win10", "win11"):
                    target_arch = build_arch
                else:
                    target_arch = "win32" if self._pyinfo(build_python).get("arch") == "32-bit" else "amd64"
                rt_dlls = find_vc_runtime_dlls(target_arch)
                if rt_dlls:
                    self.log.emit("")
                    self.log.emit(f"🌍 Bundle VC++ Runtime: {len(rt_dlls)} DLL найдено")
                    for name, path in rt_dlls:
                        # ;.  — кладём в корень (рядом с .exe внутри _MEI)
                        cmd.extend(["--add-binary", f"{path};."])
                        self.log.emit(f"   + {name}")
                else:
                    self.log.emit("⚠ VC++ Runtime DLL не найдены в System32 — exe может не запуститься на чужом ПК.")

            # ------- Bundle ffmpeg -------
            if bundle_ffmpeg:
                custom_ffmpeg = (self.p.get("ffmpeg_path") or "").strip()
                ffmpeg_paths = []

                # Приоритет: указанный пользователем путь.
                if custom_ffmpeg:
                    p_custom = Path(custom_ffmpeg)
                    if p_custom.is_file():
                        ffmpeg_paths = [str(p_custom)]
                        # Если рядом есть второй бинарь (ffmpeg/ffprobe) — тоже берём.
                        sibling = "ffprobe.exe" if p_custom.name.lower() == "ffmpeg.exe" else "ffmpeg.exe"
                        sib_path = p_custom.parent / sibling
                        if sib_path.exists():
                            ffmpeg_paths.append(str(sib_path))
                    elif p_custom.is_dir():
                        for n in ("ffmpeg.exe", "ffprobe.exe"):
                            pp = p_custom / n
                            if pp.exists():
                                ffmpeg_paths.append(str(pp))

                # Если не указан — ищем в PATH.
                if not ffmpeg_paths:
                    ffmpeg_paths = find_ffmpeg_binaries()

                # Дедупликация по имени файла (на случай если что-то добавилось дважды).
                seen_names = set()
                unique = []
                for fp in ffmpeg_paths:
                    name = Path(fp).name.lower()
                    if name not in seen_names:
                        seen_names.add(name)
                        unique.append(fp)
                ffmpeg_paths = unique

                if ffmpeg_paths:
                    self.log.emit("")
                    self.log.emit(f"📦 Bundle ffmpeg: {len(ffmpeg_paths)} файл(ов)")
                    for fp in ffmpeg_paths:
                        cmd.extend(["--add-binary", f"{fp};."])
                        self.log.emit(f"   + {Path(fp).name}  ←  {fp}")
                else:
                    self.log.emit("⚠ ffmpeg.exe не найден в PATH. Скачай и положи рядом с проектом или укажи путь.")

            # ------- Win7-режим: bundle yt-dlp_win7.exe (nicolaasjan) -------
            uses_ytdlp = "yt_dlp" in set(self.p.get("third") or []) | set(self.p.get("unknown") or [])
            if is_win7_mode and uses_ytdlp:
                ytdlp_exe = self._ensure_nicolaasjan_ytdlp()
                if ytdlp_exe:
                    cmd.extend(["--add-binary", f"{ytdlp_exe};."])
                    self.log.emit(f"🪟 Bundle yt-dlp_win7.exe → внутрь EXE: {ytdlp_exe}")
                    self.log.emit("   Приложение найдёт его через sys._MEIPASS и будет вызывать как subprocess.")
                    # Также НЕ нужно ставить упоминание UPX-исключения через подстановку —
                    # bundled exe не пакуется UPX (большой и сжат уже).
                    cmd.extend(["--upx-exclude", "yt-dlp_win7.exe"])
                    cmd.extend(["--upx-exclude", "yt-dlp.exe"])
                else:
                    self.log.emit("⚠ yt-dlp_win7.exe не получен. Win7-сборка пройдёт, но без актуального yt-dlp — "
                                  "Win7 не сможет качать с YouTube.")

            # ------- Crash logger runtime hook -------
            if universal or debug_mode:
                hook_path = write_crash_logger_hook(workspace_dir)
                cmd.extend(["--runtime-hook", str(hook_path)])
                self.log.emit("")
                self.log.emit("🐞 Crash-logger подключён: при ошибке создастся <имя>_crash.log рядом с exe.")

            # ------- UPX-сжатие -------
            upx_enabled = bool(self.p.get("upx_enabled"))
            if upx_enabled:
                upx_dir = find_upx(workspace_dir)
                if upx_dir:
                    cmd.extend(["--upx-dir", upx_dir])
                    # Безопасные exclude для проблемных DLL/pyd.
                    for pat in UPX_EXCLUDE_PATTERNS:
                        cmd.extend(["--upx-exclude", pat])
                    self.log.emit("")
                    self.log.emit(f"🗜 UPX-сжатие включено: {upx_dir}")
                    self.log.emit(f"   Исключения: {len(UPX_EXCLUDE_PATTERNS)} паттернов (Qt6Core/Gui/Widgets, vcruntime, python3xx и др.)")
                else:
                    self.log.emit("")
                    self.log.emit("⚠ UPX не найден — сжатие отключено.")
                    cmd.append("--noupx")
            else:
                cmd.append("--noupx")

            third_list = sorted(set(self.p["third"]))
            qt_used = self.p.get("qt_used") or {}  # {binding: [QtCore, QtGui, ...]}

            # ------- Авто-оптимизация: исключения для лишних Qt-модулей -------
            qt_excluded_total = []
            if auto_opt:
                for binding, used in qt_used.items():
                    excludes = build_qt_exclude_list(binding, set(used))
                    for mod in excludes:
                        cmd.extend(["--exclude-module", f"{binding}.{mod}"])
                        qt_excluded_total.append(f"{binding}.{mod}")

            # ------- Hidden imports -------
            hidden = set(self.p["third"]) | set(self.p["unknown"])

            if max_compat or auto_opt:
                # Базовые stdlib-encodings, безопасно везде.
                hidden |= {"encodings", "encodings.idna", "encodings.utf_8", "_cffi_backend"}

            if max_compat or auto_opt:
                # Явно указываем используемые подмодули Qt.
                for binding, used in qt_used.items():
                    for mod in used:
                        hidden.add(f"{binding}.{mod}")

            for name in sorted(n for n in hidden if n):
                cmd.extend(["--hidden-import", name])

            # ------- Collect all -------
            if max_compat:
                # Полная сборка всех найденных пакетов (большой exe, но "точно работает").
                for name in third_list:
                    cmd.extend(["--collect-all", name])
                # И submodules — на случай рантайм-импортов.
                for name in third_list:
                    cmd.extend(["--collect-submodules", name])
            elif auto_opt:
                # Точечная сборка: для Qt-байндингов НЕ collect-all (он тянет ВСЁ —
                # qml/, plugins/, translations/ — даже несмотря на --exclude-module,
                # это даёт +300-400 МБ в exe).
                # Стандартные PyInstaller хуки (hook-PySide6.QtCore.py и др.) сами
                # подтягивают plugins/translations ТОЛЬКО для нужных модулей.
                # Просто перечисляем нужные модули через --hidden-import (это уже
                # сделано выше), и не мешаем хукам своей дополнительной сборкой.
                # Для не-Qt пакетов: submodules + data (без лишних бинарников).
                # Полный --collect-all — только для пакетов, которые грузят DLL
                # вручную (ctypes) и иначе не работают.
                for name in third_list:
                    if name in QT_BINDINGS:
                        continue
                    if name in AUTO_OPT_COLLECT_ALL:
                        cmd.extend(["--collect-all", name])
                    else:
                        cmd.extend(["--collect-submodules", name, "--collect-data", name])
            elif collect_all:
                for name in third_list:
                    cmd.extend(["--collect-all", name])

            # ------- tkinter: явный сбор tcl/tk рантайма (во ВСЕХ режимах) -------
            # tkinter — stdlib, поэтому не входит в third_list и не собирается
            # выше. Встроенный хук PyInstaller не всегда тянет tcl/tk
            # (_tkinter.pyd, tcl86t.dll/tk86t.dll, папки tcl/ tk/) → на чужом ПК
            # exe падает с «No module named tkinter». Если проект использует
            # tkinter — добавляем явно, независимо от выбранного режима.
            if self.p.get("uses_tkinter"):
                for name in TKINTER_SUBMODULES:
                    cmd.extend(["--hidden-import", name])
                cmd.extend(["--collect-all", "tkinter"])
                self.log.emit("")
                self.log.emit("🧩 tkinter: добавлен --collect-all tkinter + hidden-imports "
                              "(tcl/tk рантайм). Чинит «No module named tkinter» на чужом ПК.")

            # ------- Логирование режима -------
            if auto_opt:
                self.log.emit("")
                self.log.emit("Режим: АВТО-ОПТИМИЗАЦИЯ EXE")
                self.log.emit("EXE содержит интерпретатор Python и только нужные зависимости.")
                self.log.emit("Запустится на любом ПК с Windows без установки Python.")
                if qt_excluded_total:
                    self.log.emit(f"Исключено лишних Qt-модулей: {len(qt_excluded_total)}")
                    self.log.emit("  " + ", ".join(qt_excluded_total[:8])
                                  + (f", +{len(qt_excluded_total) - 8}..." if len(qt_excluded_total) > 8 else ""))
                qt_in_proj = [n for n in third_list if n in QT_BINDINGS]
                if qt_in_proj:
                    self.log.emit(
                        f"Qt-байндинг ({', '.join(qt_in_proj)}): только нужные модули + "
                        f"стандартные хуки PyInstaller (без --collect-all qml/plugins/translations)."
                    )
            elif max_compat:
                self.log.emit("")
                self.log.emit("Режим: Максимальная совместимость EXE (всё включено)")
                self.log.emit("EXE будет содержать интерпретатор Python и все зависимости.")
                self.log.emit("Запустится на любом ПК с Windows без установки Python.")

            cmd.append(str(main_file))

            self.log.emit("")
            self.log.emit("=== Команда сборки ===")
            self.log.emit(subprocess.list2cmdline([str(x) for x in cmd]))
            self.log.emit("")
            self.log.emit("=== Сборка ===")
            self.stage.emit("Сборка PyInstaller...")

            build_start = time.time()
            code = self._run_command(cmd, cwd=str(project_dir))
            if self._cancelled:
                self.done.emit(-2, "")
                return
            # onedir: dist/<name>/<name>.exe; onefile: dist/<name>.exe.
            exe_path = dist_dir / f"{app_name}.exe" if onefile else dist_dir / app_name / f"{app_name}.exe"
            fresh = exe_path.exists() and exe_path.stat().st_mtime >= build_start - 2
            self.done.emit(code, str(exe_path) if fresh else "")
        except Exception as exc:
            self.failed.emit(str(exc))


# ----------------------- Авто-скачивание ffmpeg -----------------------

# Официальные Windows-сборки от BtbN — стабильный source без зеркал.
# essentials build — только ffmpeg/ffprobe без лишнего.
FFMPEG_DOWNLOAD_URL = (
    "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/"
    "ffmpeg-master-latest-win64-gpl.zip"
)


class FfmpegDownloadWorker(QThread):
    """Скачивает официальную Win64-сборку ffmpeg и распаковывает в указанную папку."""
    progress = Signal(int)        # 0..100
    log = Signal(str)
    done = Signal(str)            # путь к папке с ffmpeg.exe/ffprobe.exe
    failed = Signal(str)

    def __init__(self, target_dir, parent=None):
        super().__init__(parent)
        self.target_dir = Path(target_dir)
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        tmp_zip = None
        try:
            self.target_dir.mkdir(parents=True, exist_ok=True)

            # Если уже есть — ничего не делаем.
            existing_ffmpeg = self.target_dir / "ffmpeg.exe"
            existing_ffprobe = self.target_dir / "ffprobe.exe"
            if existing_ffmpeg.exists() and existing_ffprobe.exists():
                self.log.emit(f"ffmpeg уже на месте: {self.target_dir}")
                self.progress.emit(100)
                self.done.emit(str(self.target_dir))
                return

            tmp_zip = _make_temp_path(".zip")
            self.log.emit(f"Скачивание: {FFMPEG_DOWNLOAD_URL}")
            self.log.emit(f"Во временный файл: {tmp_zip}")

            state = {"last": -1, "got": 0}

            def prog(got, total):
                state["got"] = got
                if total > 0:
                    pct = int(got * 100 / total)
                    if pct != state["last"]:
                        state["last"] = pct
                        self.progress.emit(pct)

            digest = download_file(FFMPEG_DOWNLOAD_URL, tmp_zip, prog, lambda: self._cancelled)
            if not verify_sha256(FFMPEG_DOWNLOAD_URL, digest, self.log.emit):
                self.failed.emit("SHA256 архива ffmpeg не совпал.")
                return
            self.log.emit(f"Скачано: {state['got'] // (1024 * 1024)} МБ. Распаковка...")

            # Распаковываем только нужные exe'шники (не всю папку с doc/presets).
            extracted = 0
            with zipfile.ZipFile(tmp_zip) as zf:
                for member in zf.namelist():
                    name = Path(member).name.lower()
                    if name in ("ffmpeg.exe", "ffprobe.exe"):
                        dest = self.target_dir / Path(member).name
                        with zf.open(member) as src, open(dest, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                        self.log.emit(f"  + {dest.name}")
                        extracted += 1

            if extracted == 0:
                self.failed.emit("В архиве не найдены ffmpeg.exe / ffprobe.exe.")
                return

            self.progress.emit(100)
            self.log.emit(f"Готово. ffmpeg распакован в: {self.target_dir}")
            self.done.emit(str(self.target_dir))

        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            if tmp_zip is not None:
                try:
                    tmp_zip.unlink()
                except Exception:
                    pass


# ----------------------- Авто-скачивание UPX -----------------------

# Версия UPX закреплена (а не «latest»): воспроизводимость + supply-chain.
UPX_VERSION = "4.2.4"
UPX_DOWNLOAD_URL = (f"https://github.com/upx/upx/releases/download/v{UPX_VERSION}/"
                    f"upx-{UPX_VERSION}-win64.zip")

# Пакеты, которым в режиме авто-оптимизации всё-таки нужен --collect-all
# (DLL/данные грузятся вручную через ctypes/пути).
AUTO_OPT_COLLECT_ALL = {
    "customtkinter", "tkinterdnd2", "imageio_ffmpeg", "pyzbar", "vlc",
    "sounddevice", "soundfile", "certifi",
}

# DLL/PYD, которые НЕ нужно сжимать UPX'ом (могут не запуститься после).
# Это известные проблемные точки для PySide6 и нативных Python-расширений.
UPX_EXCLUDE_PATTERNS = [
    "vcruntime140.dll", "vcruntime140_1.dll",
    "msvcp140.dll", "msvcp140_1.dll", "msvcp140_2.dll",
    "concrt140.dll", "vccorlib140.dll",
    "python3*.dll",
    "Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll",
    "Qt6Network.dll", "Qt6Svg.dll",
    "shiboken6.*",
    "PySide6.*.pyd",
    "_ssl.pyd", "_socket.pyd", "_hashlib.pyd",
    "select.pyd", "unicodedata.pyd",
    "libcrypto-*.dll", "libssl-*.dll",
]


def find_upx(workspace_dir):
    """Ищет upx.exe: в workspace/upx (ограниченно) и в PATH.
    Раньше был rglob по всему workspace, включая build/ с тысячами файлов."""
    name = "upx.exe" if sys.platform.startswith("win") else "upx"

    if workspace_dir:
        base = Path(workspace_dir) / "upx"
        cands = [base / name]
        try:
            # UPX может лежать в подпапке с версией в имени (upx-4.2.4-win64).
            cands += [d / name for d in base.iterdir() if d.is_dir()]
        except OSError:
            pass
        for p in cands:
            if p.is_file():
                return str(p.parent)

    # PATH
    in_path = shutil.which(name)
    if in_path:
        return str(Path(in_path).parent)
    return None


class UpxDownloadWorker(QThread):
    """Скачивает закреплённую версию UPX с GitHub и распаковывает upx.exe."""
    progress = Signal(int)
    log = Signal(str)
    done = Signal(str)         # путь к папке с upx.exe
    failed = Signal(str)

    def __init__(self, target_dir, parent=None):
        super().__init__(parent)
        self.target_dir = Path(target_dir)
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        tmp_zip = None
        try:
            self.target_dir.mkdir(parents=True, exist_ok=True)

            # Если уже есть — выходим.
            if (self.target_dir / "upx.exe").exists():
                self.log.emit(f"UPX уже на месте: {self.target_dir}")
                self.progress.emit(100)
                self.done.emit(str(self.target_dir))
                return

            self.log.emit(f"Скачивание UPX {UPX_VERSION}: {UPX_DOWNLOAD_URL}")
            tmp_zip = _make_temp_path(".zip")
            state = {"last": -1, "got": 0}

            def prog(got, total):
                state["got"] = got
                if total > 0:
                    pct = int(got * 100 / total)
                    if pct != state["last"]:
                        state["last"] = pct
                        self.progress.emit(pct)

            digest = download_file(UPX_DOWNLOAD_URL, tmp_zip, prog, lambda: self._cancelled)
            if not verify_sha256(UPX_DOWNLOAD_URL, digest, self.log.emit):
                self.failed.emit("SHA256 архива UPX не совпал.")
                return
            self.log.emit(f"Скачано: {state['got'] // 1024} КБ. Распаковка...")

            extracted_upx_dir = None
            with zipfile.ZipFile(tmp_zip) as zf:
                for member in zf.namelist():
                    if Path(member).name.lower() == "upx.exe":
                        dest = self.target_dir / "upx.exe"
                        with zf.open(member) as src, open(dest, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                        extracted_upx_dir = str(self.target_dir)
                        self.log.emit(f"  + upx.exe → {dest}")
                        break

            if not extracted_upx_dir:
                self.failed.emit("upx.exe не найден в архиве.")
                return

            self.progress.emit(100)
            self.log.emit(f"Готово. UPX установлен: {extracted_upx_dir}")
            self.done.emit(extracted_upx_dir)

        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            if tmp_zip is not None:
                try:
                    tmp_zip.unlink()
                except Exception:
                    pass


class PythonProbeWorker(QThread):
    """detect_python_info в фоне (не блокирует окно до 15 с)."""
    done = Signal(str, dict)   # (путь, info)

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path

    def run(self):
        try:
            info = detect_python_info(self.path)
        except Exception as exc:
            info = {"ok": False, "error": str(exc)}
        self.done.emit(self.path, info)


# ----------------------- Диалог выбора встроенной иконки -----------------------
class IconPickerDialog(QDialog):
    chosen = Signal(str, str)   # (имя пресета, ключ стиля)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Просмотр иконок — {APP_NAME} v{APP_VERSION}")
        self.resize(820, 620)
        self.setMinimumSize(620, 420)

        root = QVBoxLayout(self)
        top = QHBoxLayout()
        title = QLabel("Кликни на иконку — рядом откроются все её стили")
        f = title.font(); f.setPointSize(11); f.setBold(True); title.setFont(f)
        top.addWidget(title)
        top.addStretch(1)
        self._count_lbl = QLabel("")
        top.addWidget(self._count_lbl)
        root.addLayout(top)

        # Поиск по имени — при ~300 иконках без него уже никак.
        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("🔍"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск: сердечко, звезда, машина, rocket, star...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self._apply_filter)
        search_row.addWidget(self.search_edit, 1)
        root.addLayout(search_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        holder = QWidget()
        self._grid = QGridLayout(holder)
        self._grid.setSpacing(8)
        self._columns = 5
        self._cells = []  # [(glyph, имя-представитель, строка-для-поиска, QFrame)]

        # ГРУППИРОВКА: один глиф = одна плитка. Цветовые варианты
        # (Star Red/Blue/Pink...) показываются в панели по клику.
        self._glyph_groups = {}   # glyph -> [имена пресетов]
        for name, spec in BUILTIN_ICONS.items():
            self._glyph_groups.setdefault(spec["glyph"], []).append(name)

        self.setUpdatesEnabled(False)  # без перерисовок на время построения
        for glyph, variants in self._glyph_groups.items():
            rep = variants[0]  # представитель группы
            cell = QFrame()
            cell.setFrameShape(QFrame.StyledPanel)
            cell.setCursor(Qt.PointingHandCursor)
            if len(variants) > 1:
                cell.setToolTip("Кликни — варианты цвета и стили:\n• " + "\n• ".join(variants))
            else:
                cell.setToolTip(f"Кликни — откроются все стили «{rep}»")
            cl = QVBoxLayout(cell)
            cl.setContentsMargins(6, 6, 6, 6)
            cl.setSpacing(4)

            img = QLabel()
            img.setPixmap(make_preview_pixmap(rep, 56))
            img.setAlignment(Qt.AlignCenter)
            cl.addWidget(img)

            cap = rep if len(variants) == 1 else f"{rep}  ({len(variants)})"
            lbl = QLabel(cap)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            cl.addWidget(lbl)

            # Кликабельна ВСЯ плитка — без отдельной кнопки.
            cell.mousePressEvent = (
                lambda event, g=glyph, c=cell: self._open_style_popup(g, c)
            )

            search_str = (
                " ".join(variants) + " " + glyph + " "
                + RU_GLYPH_KEYWORDS.get(glyph, "")
            ).lower()
            self._cells.append((glyph, rep, search_str, cell))

        self._apply_filter("")  # первичная раскладка
        self.setUpdatesEnabled(True)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)

    def _open_style_popup(self, glyph, anchor):
        """Панель рядом с плиткой: строки = цветовые варианты этой иконки,
        столбцы = 8 стилей. Один клик — выбраны и вариант, и стиль.
        Клик мимо панели — она закрывается."""
        variants = self._glyph_groups.get(glyph) or []
        if not variants:
            return
        popup = QFrame(self, Qt.Popup)
        popup.setFrameShape(QFrame.StyledPanel)
        lay = QGridLayout(popup)
        lay.setContentsMargins(10, 8, 10, 10)
        lay.setSpacing(4)

        cap = QLabel(f"«{variants[0]}» — кликни на нужный вариант:")
        cf = cap.font(); cf.setBold(True); cap.setFont(cf)
        cap.setAlignment(Qt.AlignCenter)
        lay.addWidget(cap, 0, 0, 1, 1 + len(ICON_STYLES))

        # Шапка со стилями («Градиент (классика)» → «Градиент»)
        small = QFont(); small.setPointSize(7)
        for c, key in enumerate(ICON_STYLES):
            h = QLabel(ICON_STYLE_LABELS[key].split(" (")[0])
            h.setFont(small)
            h.setAlignment(Qt.AlignCenter)
            lay.addWidget(h, 1, c + 1)

        icon_px = 44 if len(variants) > 2 else 52
        for r, preset_name in enumerate(variants):
            row_lbl = QLabel(preset_name)
            row_lbl.setFont(small)
            lay.addWidget(row_lbl, r + 2, 0)
            for c, key in enumerate(ICON_STYLES):
                b = QToolButton(popup)
                b.setIcon(QIcon(make_preview_pixmap(preset_name, icon_px, key)))
                b.setIconSize(QSize(icon_px, icon_px))
                b.setToolTip(f"{preset_name} — {ICON_STYLE_LABELS[key]}")
                b.setCursor(Qt.PointingHandCursor)
                b.clicked.connect(
                    lambda _=False, n=preset_name, s=key, p=popup: self._pick_style(p, n, s)
                )
                lay.addWidget(b, r + 2, c + 1)

        popup.adjustSize()
        # Показываем сбоку от кнопки; если не влезает справа — слева.
        pos = anchor.mapToGlobal(anchor.rect().topRight())
        screen = QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            if pos.x() + popup.width() > geo.right():
                pos = anchor.mapToGlobal(anchor.rect().topLeft())
                pos.setX(pos.x() - popup.width())
            if pos.y() + popup.height() > geo.bottom():
                pos.setY(geo.bottom() - popup.height())
        popup.move(pos)
        popup.show()

    def _pick_style(self, popup, name, style):
        popup.close()
        self.chosen.emit(name, style)
        self.accept()

    def _apply_filter(self, text):
        """Фильтрует сетку; ищет и по именам вариантов, и по имени глифа."""
        text = (text or "").strip().lower()
        self.setUpdatesEnabled(False)
        while self._grid.count():
            self._grid.takeAt(0)
        row = col = 0
        shown = 0
        for _glyph, _rep, search_str, cell in self._cells:
            ok = (not text) or (text in search_str)
            cell.setVisible(ok)
            if ok:
                self._grid.addWidget(cell, row, col)
                shown += 1
                col += 1
                if col >= self._columns:
                    col = 0
                    row += 1
        self.setUpdatesEnabled(True)
        total = len(self._cells)
        variants_total = len(BUILTIN_ICONS)
        self._count_lbl.setText(
            f"Иконок: {total} (вариантов: {variants_total})" if not text
            else f"Найдено: {shown} из {total}"
        )



# ----------------------- Главное окно -----------------------
class DropZone(QFrame):
    """Зона «перетащи .py сюда / кликни, чтобы выбрать» (0.8.0)."""
    clicked = Signal()
    pathDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dropZone")
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(92)
        self.setProperty("hover", False)
        v = QVBoxLayout(self)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(2)
        arrow = QLabel("⤓")
        arrow.setObjectName("dropArrow")
        af = arrow.font(); af.setPointSize(18); arrow.setFont(af)
        arrow.setAlignment(Qt.AlignCenter)
        title = QLabel("Перетащи .py / .pyw или папку сюда")
        title.setObjectName("dropTitle")
        tf = title.font(); tf.setBold(True); title.setFont(tf)
        title.setAlignment(Qt.AlignCenter)
        sub = QLabel("или нажми, чтобы выбрать файл")
        sub.setObjectName("dropSub")
        sub.setAlignment(Qt.AlignCenter)
        for w in (arrow, title, sub):
            w.setAttribute(Qt.WA_TransparentForMouseEvents)
            v.addWidget(w)

    @staticmethod
    def first_local_path(mime):
        if mime is None or not mime.hasUrls():
            return ""
        for url in mime.urls():
            if url.isLocalFile():
                return url.toLocalFile()
        return ""

    def _set_hover(self, on):
        self.setProperty("hover", on)
        self.style().unpolish(self)
        self.style().polish(self)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        if self.first_local_path(event.mimeData()):
            self._set_hover(True)
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._set_hover(False)
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self._set_hover(False)
        path = self.first_local_path(event.mimeData())
        if path:
            self.pathDropped.emit(path)
            event.acceptProposedAction()


class FlowLayout(QLayout):
    """Раскладка «в строку с переносом» — для опций-чипов (0.8.0)."""

    def __init__(self, parent=None, spacing=6):
        super().__init__(parent)
        self._items = []
        self._spacing = spacing
        self.setContentsMargins(0, 0, 0, 0)

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index):
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        return size

    def _do_layout(self, rect, test_only):
        x, y, line_h = rect.x(), rect.y(), 0
        for item in self._items:
            hint = item.sizeHint()
            nx = x + hint.width() + self._spacing
            if nx - self._spacing > rect.right() + 1 and line_h > 0:
                x = rect.x()
                y += line_h + self._spacing
                nx = x + hint.width() + self._spacing
                line_h = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x = nx
            line_h = max(line_h, hint.height())
        return y + line_h - rect.y()


class ExeBuilderWindow(QMainWindow):
    def __init__(self, app=None, default_style_name="", default_palette=None):
        super().__init__()
        self.app = app
        self.default_style_name = default_style_name
        self.default_palette = QPalette(default_palette) if default_palette is not None else None
        self.settings = QSettings("AI_Modules", APP_NAME)

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1000, 720)
        self.setMinimumSize(860, 600)

        self.worker = None
        self.is_busy = False
        # Отработавшие воркеры держим здесь до завершения их потоков,
        # иначе возможен «QThread: Destroyed while thread is still running».
        self._retired_workers = []
        # Флаг «пользователь отказался скачивать ffmpeg» — на одну сборку,
        # чтобы вопрос не задавался повторно после авто-скачивания UPX.
        self._ffmpeg_declined = False
        # Контекст сборки, отложенной до скачивания ffmpeg/UPX.
        self._pending_convert = None
        self._stop_requested = False
        self._upx_ready_dir = None
        self._ffmpeg_worker = None
        self._ffmpeg_worker_pre = None
        self._upx_worker_pre = None
        self._probe_workers = []
        self._restoring = False
        # Debounce карточки файла: iterdir не на каждый символ.
        self._file_card_timer = QTimer(self)
        self._file_card_timer.setSingleShot(True)
        self._file_card_timer.setInterval(300)
        self._file_card_timer.timeout.connect(self._refresh_file_card)

        self.third_party_imports = []
        self.unknown_imports = []

        self._build_ui()
        self._initial_logs()
        self._restore_style()
        self._restore_python_exe()
        self._restore_icon_style()

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("centralRoot")
        self.setCentralWidget(central)
        self.setAcceptDrops(True)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        # ---------- Шапка: название + бейдж версии + статус + шестерёнка ----------
        header = QHBoxLayout()
        title = QLabel(APP_NAME)
        title.setObjectName("appTitle")
        f = title.font(); f.setPointSize(13); f.setBold(True); title.setFont(f)
        header.addWidget(title)
        badge = QLabel(APP_VERSION)
        badge.setObjectName("versionBadge")
        header.addWidget(badge)
        header.addStretch(1)
        self.status_label = QLabel(f"Готово. Версия {APP_VERSION}")
        self.status_label.setObjectName("statusLabel")
        header.addWidget(self.status_label)

        self.style_btn = QToolButton()
        self.style_btn.setObjectName("gearBtn")
        self.style_btn.setText("⚙")
        self.style_btn.setToolTip("Сменить стиль оформления / тему")
        gf = self.style_btn.font(); gf.setPointSize(14); self.style_btn.setFont(gf)
        self.style_btn.setFixedSize(36, 32)
        self.style_btn.setPopupMode(QToolButton.InstantPopup)
        self.style_btn.setMenu(self._build_style_menu())
        header.addWidget(self.style_btn)
        root.addLayout(header)

        # ---------- Две карточки: Проект | Имя, иконка, опции ----------
        cards = QHBoxLayout()
        cards.setSpacing(12)

        # --- Карточка «Проект» ---
        proj = self._make_card()
        pl = QVBoxLayout(proj)
        pl.setContentsMargins(14, 12, 14, 14)
        pl.setSpacing(8)
        pl.addWidget(self._make_caption("Проект"))

        self.drop_zone = DropZone()
        self.drop_zone.clicked.connect(self.choose_main_file)
        self.drop_zone.pathDropped.connect(self._on_path_dropped)
        pl.addWidget(self.drop_zone)

        # Карточка выбранного файла (видна, когда файл выбран)
        self.file_card = QFrame()
        self.file_card.setObjectName("fileCard")
        fc = QHBoxLayout(self.file_card)
        fc.setContentsMargins(10, 8, 8, 8)
        self.file_card_icon = QLabel("🐍")
        self.file_card_icon.setObjectName("fileCardIcon")
        self.file_card_icon.setFixedSize(34, 34)
        self.file_card_icon.setAlignment(Qt.AlignCenter)
        fc.addWidget(self.file_card_icon)
        self.file_card_text = QLabel("")
        self.file_card_text.setObjectName("fileCardText")
        self.file_card_text.setTextFormat(Qt.RichText)
        fc.addWidget(self.file_card_text, 1)
        self.file_card_clear = QToolButton()
        self.file_card_clear.setObjectName("flatBtn")
        self.file_card_clear.setText("✕")
        self.file_card_clear.setToolTip("Сбросить выбранный файл")
        self.file_card_clear.clicked.connect(self._clear_main_file)
        fc.addWidget(self.file_card_clear)
        self.file_card.setVisible(False)
        pl.addWidget(self.file_card)

        self.main_file_edit = QLineEdit()
        self.main_file_edit.setClearButtonEnabled(True)
        self.main_file_edit.setPlaceholderText("Путь к главному .py / .pyw")
        self.main_file_edit.textChanged.connect(lambda *_: self._file_card_timer.start())
        self._add_browse_action(self.main_file_edit, self.choose_main_file, "Выбрать .py")
        pl.addWidget(self._make_field("Главный файл", self.main_file_edit))

        self.project_dir_edit = QLineEdit()
        self.project_dir_edit.setClearButtonEnabled(True)
        self.project_dir_edit.setPlaceholderText("Подставится автоматически")
        self._add_browse_action(self.project_dir_edit, self.choose_project_dir, "Выбрать папку")
        pl.addWidget(self._make_field("Папка проекта", self.project_dir_edit))

        self.output_dir_edit = QLineEdit(str(fallback_output_dir()))
        self.output_dir_edit.setClearButtonEnabled(True)
        self._add_browse_action(self.output_dir_edit, self.choose_output_dir, "Выбрать")
        pl.addWidget(self._make_field("Папка для EXE", self.output_dir_edit))
        pl.addStretch(1)
        cards.addWidget(proj, 5)

        # --- Карточка «Имя и иконка» + опции-чипы ---
        opts = self._make_card()
        ol = QVBoxLayout(opts)
        ol.setContentsMargins(14, 12, 14, 14)
        ol.setSpacing(8)
        ol.addWidget(self._make_caption("Имя и иконка"))

        self.app_name_edit = QLineEdit("MyApp")
        self.app_name_edit.setPlaceholderText("Имя EXE")
        ol.addWidget(self._make_field("Имя EXE", self.app_name_edit))

        icon_row = QHBoxLayout()
        icon_row.setSpacing(6)
        self.icon_preview = QLabel()
        self.icon_preview.setObjectName("iconPreview")
        self.icon_preview.setFixedSize(44, 44)
        self.icon_preview.setAlignment(Qt.AlignCenter)
        icon_row.addWidget(self.icon_preview)

        self.builtin_icon_combo = QComboBox()
        self.builtin_icon_combo.addItem(NO_BUILTIN_ICON)
        self.builtin_icon_combo.addItems(list(BUILTIN_ICONS.keys()))
        self.builtin_icon_combo.setCurrentText("Python Blue")
        self.builtin_icon_combo.currentTextChanged.connect(self._update_icon_preview)
        icon_row.addWidget(self.builtin_icon_combo, 1)
        ol.addLayout(icon_row)

        # Быстрая сетка иконок + «все иконки»
        _n_glyphs = len({s["glyph"] for s in BUILTIN_ICONS.values()})
        grid = QHBoxLayout()
        grid.setSpacing(6)
        self._quick_icon_btns = {}
        for name in self._quick_icon_names(5):
            qb = QToolButton()
            qb.setObjectName("iconTile")
            qb.setCheckable(True)
            qb.setAutoRaise(False)
            qb.setIcon(QIcon(make_preview_pixmap(name, 32)))
            qb.setIconSize(QSize(28, 28))
            qb.setFixedSize(40, 40)
            qb.setToolTip(name)
            qb.setCursor(Qt.PointingHandCursor)
            qb.clicked.connect(lambda _c=False, n=name: self._on_icon_picked(n, ""))
            grid.addWidget(qb)
            self._quick_icon_btns[name] = qb
        bview = QToolButton()
        bview.setObjectName("iconTile")
        bview.setText("…")
        bview.setFixedSize(40, 40)
        bview.setCursor(Qt.PointingHandCursor)
        bview.setToolTip(f"Выбрать из {_n_glyphs} иконок")
        bview.clicked.connect(self.open_icon_picker)
        grid.addWidget(bview)
        grid.addStretch(1)
        ol.addLayout(grid)

        # Скрытое поле своей .ico (показывается в «Ещё»)
        self.icon_edit = QLineEdit()
        self.icon_edit.setClearButtonEnabled(True)
        self.icon_edit.setVisible(False)

        ol.addSpacing(4)
        ol.addWidget(self._make_caption("Опции"))
        chips = FlowLayout(spacing=6)
        self.onefile_chk = self._make_chip("Один файл", True, chips)
        self.windowed_chk = self._make_chip("Без консоли", True, chips)
        self.auto_opt_chk = self._make_chip("⚡ Авто-оптимизация", True, chips)
        self.auto_opt_chk.toggled.connect(self._on_auto_opt_toggled)
        self.upx_chk = self._make_chip("🗜 UPX", True, chips)
        self.upx_chk.setToolTip(
            "Сжимает exe утилитой UPX. Для PySide6+yt-dlp+ffmpeg типичный результат:\n"
            "~250 МБ → ~140–170 МБ.\n"
            "Если UPX не установлен — автоматически скачивается с github.com/upx/upx.\n"
            "Безопасные --upx-exclude для Qt6Core/Gui/Widgets, vcruntime, python3xx.dll\n"
            "чтобы UPX не сломал чувствительные бинари."
        )
        self.universal_chk = self._make_chip("🌍 Универсальный", True, chips)
        self.universal_chk.setToolTip("Bundle VC++ Runtime + crash-logger (рекомендуется)")
        self.debug_chk = self._make_chip("🐞 Отладка", False, chips)
        self.debug_chk.setToolTip("Отладочный EXE (с консолью)")
        ol.addLayout(chips)
        ol.addStretch(1)
        cards.addWidget(opts, 4)
        root.addLayout(cards)

        # ---------- Панель действий ----------
        go = QHBoxLayout()
        go.setSpacing(8)
        self.convert_btn = QPushButton(self.CONVERT_BTN_IDLE)
        self.convert_btn.setObjectName("primaryBtn")
        self.convert_btn.setMinimumHeight(50)
        self.convert_btn.setCursor(Qt.PointingHandCursor)
        bf = self.convert_btn.font(); bf.setPointSize(14); bf.setBold(True); self.convert_btn.setFont(bf)
        self.convert_btn.setToolTip(
            "Анализирует проект и собирает универсальный EXE автоматически:\n"
            "• Универсальный EXE: bundle VC++ Runtime + crash-logger.\n"
            "• Авто-оптимизация: исключение неиспользуемых Qt-модулей (5–10× меньше размер).\n"
            "• Авто-bundle ffmpeg: если в проекте используется yt-dlp / moviepy и т.п.\n"
            "Готовый exe запускается на ЛЮБОМ ПК с Windows 7/10/11 без установки чего-либо."
        )
        self.convert_btn.clicked.connect(self.start_convert)
        go.addWidget(self.convert_btn, 1)

        self.analyze_btn = QPushButton("🔍 Анализ")
        self.analyze_btn.setObjectName("ghostBtn")
        self.analyze_btn.setMinimumHeight(50)
        self.analyze_btn.setToolTip("Анализировать проект без сборки")
        self.analyze_btn.clicked.connect(self.start_analyze)
        go.addWidget(self.analyze_btn)

        self.stop_btn = QPushButton("⏹ Стоп")
        self.stop_btn.setObjectName("ghostBtn")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setToolTip("Остановить сборку / скачивание")
        self.stop_btn.clicked.connect(self.stop_build)
        self.stop_btn.setVisible(False)
        go.addWidget(self.stop_btn)

        self.open_output_btn = QPushButton("📂")
        self.open_output_btn.setObjectName("ghostBtn")
        self.open_output_btn.setMinimumHeight(50)
        self.open_output_btn.setMinimumWidth(56)
        self.open_output_btn.setToolTip("Открыть папку EXE")
        self.open_output_btn.clicked.connect(self.open_output_dir)
        go.addWidget(self.open_output_btn)

        self.expert_btn = QPushButton(self.EXPERT_BTN_OFF)
        self.expert_btn.setObjectName("ghostBtn")
        self.expert_btn.setMinimumHeight(50)
        self.expert_btn.setCheckable(True)
        self.expert_btn.setToolTip("Эксперт-настройки (для редких случаев)")
        self.expert_btn.toggled.connect(self._toggle_expert)
        go.addWidget(self.expert_btn)
        root.addLayout(go)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("buildProgress")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        root.addWidget(self.progress_bar)

        # ---------- Эксперт-настройки (свёрнуто) ----------
        self.expert_box = QGroupBox("Эксперт-настройки (для редких случаев)")
        self.expert_box.setObjectName("expertBox")
        eg = QGridLayout(self.expert_box)

        eg.addWidget(QLabel("Своя .ico (если нужна):"), 0, 0)
        eg.addWidget(self.icon_edit, 0, 1, 1, 3)
        self.icon_edit.setVisible(True)  # внутри expert_box делаем видимым
        bi = QPushButton("...")
        bi.setFixedWidth(34)
        bi.clicked.connect(self.choose_icon)
        eg.addWidget(bi, 0, 4)

        checks = QHBoxLayout()
        self.clean_chk = QCheckBox("Очистить build/spec"); self.clean_chk.setChecked(True); checks.addWidget(self.clean_chk)
        self.install_pi_chk = QCheckBox("Автоустановка PyInstaller"); self.install_pi_chk.setChecked(True); checks.addWidget(self.install_pi_chk)
        self.collect_all_chk = QCheckBox("--collect-all для внешних библиотек"); checks.addWidget(self.collect_all_chk)
        checks.addStretch(1)
        eg.addLayout(checks, 1, 0, 1, 5)

        checks2 = QHBoxLayout()
        self.max_compat_chk = QCheckBox("Максимальная совместимость (всё-в-комплекте, exe большой)")
        self.max_compat_chk.toggled.connect(self._on_max_compat_toggled)
        checks2.addWidget(self.max_compat_chk)
        self.bundle_ffmpeg_chk = QCheckBox("📦 Включить ffmpeg вручную")
        self.bundle_ffmpeg_chk.setToolTip(
            "Обычно не нужно — авто-bundle сам решит. Включи если хочешь принудительно."
        )
        checks2.addWidget(self.bundle_ffmpeg_chk)
        checks2.addStretch(1)
        eg.addLayout(checks2, 2, 0, 1, 5)

        ffmpeg_row = QHBoxLayout()
        ffmpeg_row.addWidget(QLabel("Путь к ffmpeg (опц.):"))
        self.ffmpeg_edit = QLineEdit()
        self.ffmpeg_edit.setPlaceholderText("Авто-поиск в PATH и подпапке проекта; либо укажи вручную")
        self.ffmpeg_edit.setClearButtonEnabled(True)
        ffmpeg_row.addWidget(self.ffmpeg_edit, 1)
        ffmpeg_btn = QPushButton("...")
        ffmpeg_btn.setFixedWidth(34)
        ffmpeg_btn.clicked.connect(self._choose_ffmpeg)
        ffmpeg_row.addWidget(ffmpeg_btn)
        self.download_ffmpeg_btn = QPushButton("⬇ Скачать ffmpeg")
        self.download_ffmpeg_btn.clicked.connect(self._download_ffmpeg)
        ffmpeg_row.addWidget(self.download_ffmpeg_btn)
        eg.addLayout(ffmpeg_row, 3, 0, 1, 5)

        # --- Целевая ОС / выбор Python для сборки ---
        target_row = QHBoxLayout()
        target_row.addWidget(QLabel("Целевая ОС:"))
        self.target_os_combo = QComboBox()
        for key, spec in PORTABLE_PYTHONS.items():
            self.target_os_combo.addItem(spec["label"], userData=key)
        self.target_os_combo.setToolTip(
            "Выбери минимальную целевую ОС для EXE.\n"
            "Сборщик САМ скачает нужный Python в свою папку (не в систему!)\n"
            "и через него соберёт EXE."
        )
        self.target_os_combo.currentIndexChanged.connect(self._on_target_os_changed)
        target_row.addWidget(self.target_os_combo, 1)
        target_row.addWidget(QLabel("Арх.:"))
        self.arch_combo = QComboBox()
        for akey, aspec in PORTABLE_ARCHES.items():
            self.arch_combo.addItem(aspec["label"], userData=akey)
        self.arch_combo.setToolTip(
            "Архитектура авто-скачиваемого Python (только режимы Windows 7/10/11).\n"
            "x64 — обычные ПК. x86 — 32-битные/старые. ARM64 — устройства на ARM.\n"
            "Для «Текущий»/«Свой Python» игнорируется (берётся арх. того интерпретатора)."
        )
        self.arch_combo.currentIndexChanged.connect(self._on_build_arch_changed)
        target_row.addWidget(self.arch_combo)
        self.check_python_btn = QPushButton("🐍 Проверить")
        self.check_python_btn.clicked.connect(self._check_python_exe)
        target_row.addWidget(self.check_python_btn)
        eg.addLayout(target_row, 4, 0, 1, 5)

        # Свой путь к python.exe (виден только в режиме «Свой Python»).
        py_row = QHBoxLayout()
        self.python_path_lbl = QLabel("Путь к python.exe:")
        py_row.addWidget(self.python_path_lbl)
        self.python_exe_edit = QLineEdit()
        self.python_exe_edit.setPlaceholderText("C:\\Python38\\python.exe")
        self.python_exe_edit.setClearButtonEnabled(True)
        self.python_exe_edit.editingFinished.connect(self._on_python_exe_changed)
        py_row.addWidget(self.python_exe_edit, 1)
        self.python_browse_btn = QPushButton("...")
        self.python_browse_btn.setFixedWidth(34)
        self.python_browse_btn.clicked.connect(self._choose_python_exe)
        py_row.addWidget(self.python_browse_btn)
        eg.addLayout(py_row, 5, 0, 1, 5)

        self.python_info_lbl = QLabel("")
        self.python_info_lbl.setWordWrap(True)
        eg.addWidget(self.python_info_lbl, 6, 0, 1, 5)

        export_row = QHBoxLayout()
        self.export_icons_btn = QPushButton(f"💾 Экспорт всех {len(BUILTIN_ICONS)} иконок в .ico")
        self.export_icons_btn.setToolTip(
            "Сохраняет весь встроенный набор иконок как .ico-файлы\n"
            "в папку builtin_icons_export внутри рабочей папки сборщика."
        )
        self.export_icons_btn.clicked.connect(self.export_icons_clicked)
        export_row.addWidget(self.export_icons_btn)
        export_row.addStretch(1)
        eg.addLayout(export_row, 7, 0, 1, 5)

        eg.setColumnStretch(1, 1)
        self.expert_box.setVisible(False)
        root.addWidget(self.expert_box)

        # ---------- Лог (карточка с кнопками в шапке) ----------
        log_card = self._make_card()
        lc = QVBoxLayout(log_card)
        lc.setContentsMargins(12, 8, 12, 12)
        lc.setSpacing(6)
        log_head = QHBoxLayout()
        log_head.addWidget(self._make_caption("Лог"))
        log_head.addStretch(1)
        self.about_btn = QPushButton("О программе")
        self.copy_log_btn = QPushButton("Копировать лог")
        self.clear_log_btn = QPushButton("Очистить лог")
        for b, slot in ((self.about_btn, self.show_about),
                        (self.copy_log_btn, self.copy_log),
                        (self.clear_log_btn, self.clear_log)):
            b.setObjectName("linkBtn")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(slot)
            log_head.addWidget(b)
        lc.addLayout(log_head)

        self.log_view = QPlainTextEdit()
        self.log_view.setObjectName("logView")
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(20000)  # длинный лог PyInstaller не тормозит UI
        self.log_view.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        f2 = QFont("Consolas, monospace"); f2.setStyleHint(QFont.Monospace); self.log_view.setFont(f2)
        lc.addWidget(self.log_view)
        root.addWidget(log_card, 1)

    # ---------- UI-хелперы (0.8.0) ----------
    EXPERT_BTN_OFF = "⚙ Ещё ▾"
    EXPERT_BTN_ON = "⚙ Ещё ▴"

    @staticmethod
    def _make_card():
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.StyledPanel)
        return card

    @staticmethod
    def _make_caption(text):
        lbl = QLabel(text.upper())
        lbl.setObjectName("caption")
        return lbl

    @staticmethod
    def _make_field(label, widget):
        box = QWidget()
        v = QVBoxLayout(box)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(3)
        lbl = QLabel(label)
        lbl.setObjectName("fieldLabel")
        v.addWidget(lbl)
        v.addWidget(widget)
        return box

    def _add_browse_action(self, edit, slot, tip):
        icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        act = edit.addAction(icon, QLineEdit.TrailingPosition)
        act.setToolTip(tip)
        act.triggered.connect(slot)
        return act

    @staticmethod
    def _make_chip(text, checked, layout):
        chk = QCheckBox(text)
        chk.setObjectName("chip")
        chk.setChecked(checked)
        chk.setCursor(Qt.PointingHandCursor)
        layout.addWidget(chk)
        return chk

    @staticmethod
    def _quick_icon_names(n):
        """Первые n пресетов с разными глифами (Python Blue — первым)."""
        names, seen = [], set()
        order = list(BUILTIN_ICONS.keys())
        if "Python Blue" in BUILTIN_ICONS:
            order.remove("Python Blue")
            order.insert(0, "Python Blue")
        for name in order:
            g = BUILTIN_ICONS[name].get("glyph")
            if g in seen:
                continue
            seen.add(g)
            names.append(name)
            if len(names) >= n:
                break
        return names

    def _refresh_file_card(self, *_):
        text = self.main_file_edit.text().strip()
        p = Path(text) if text else None
        if not p or not p.is_file():
            self.file_card.setVisible(False)
            self.drop_zone.setVisible(True)
            return
        try:  # только верхний уровень — быстро даже для больших папок
            n_py = sum(1 for x in p.parent.iterdir() if x.suffix.lower() in (".py", ".pyw"))
        except Exception:
            n_py = 0
        self.file_card_text.setText(
            f"<b>{html_escape(p.name)}</b><br>"
            f"<span style='color:#8b93a1'>{html_escape(str(p.parent))} · {n_py} .py</span>"
        )
        self.file_card.setVisible(True)
        self.drop_zone.setVisible(False)

    def _clear_main_file(self):
        self.main_file_edit.clear()
        self.project_dir_edit.clear()

    def _set_main_file(self, path):
        p = Path(path)
        self.main_file_edit.setText(str(p))
        self.project_dir_edit.setText(str(p.parent))
        self._apply_project_defaults(p.parent)
        if not self.app_name_edit.text().strip() or self.app_name_edit.text().strip() == "MyApp":
            self.app_name_edit.setText(p.stem)

    def _on_path_dropped(self, path):
        p = Path(path)
        if p.is_dir():
            self.project_dir_edit.setText(str(p))
            self._apply_project_defaults(p)
            cands = [c for c in ("main.py", "main.pyw", "app.py", "app.pyw", "__main__.py")
                     if (p / c).is_file()]
            if cands:
                self._set_main_file(p / cands[0])
            self.write_log(f"Перетащена папка проекта: {p}")
        elif p.suffix.lower() in (".py", ".pyw"):
            self._set_main_file(p)
            self.write_log(f"Перетащен файл: {p}")
        elif p.suffix.lower() == ".ico":
            self.icon_edit.setText(str(p))
            self.builtin_icon_combo.setCurrentText(NO_BUILTIN_ICON)
            self.write_log(f"Своя иконка: {p}")
        else:
            self.write_log(f"⚠ Не .py/.pyw/.ico и не папка: {p}")

    # Drag & drop на всё окно
    def dragEnterEvent(self, event):
        if DropZone.first_local_path(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        path = DropZone.first_local_path(event.mimeData())
        if path:
            self._on_path_dropped(path)
            event.acceptProposedAction()

    def _initial_logs(self):
        self.write_log(f"{APP_NAME} v{APP_VERSION}  —  автор: {APP_AUTHOR}")
        self.write_log(f"Встроенный набор иконок: {len(BUILTIN_ICONS)} шт.")
        self.write_log("")
        self.write_log("Как пользоваться:")
        self.write_log("  1. Перетащи главный .py/.pyw (или папку) в окно — или нажми на зону «Проект».")
        self.write_log("  2. Нажми «🚀 Сделать EXE».")
        self.write_log("")
        self.write_log("Конвертор сам всё сделает:")
        self.write_log("  🌍 bundle VC++ Runtime → запустится на ЛЮБОМ ПК (Win 7/10/11) без установки;")
        self.write_log("  ⚡ Авто-оптимизация → exe в 5–10× меньше за счёт исключения ненужных модулей;")
        self.write_log("  🗜 UPX-сжатие → exe ещё в 1.5–2× меньше (авто-скачивается);")
        self.write_log("  📦 Авто-bundle ffmpeg → если проект использует yt-dlp / moviepy / pydub и т.п.;")
        self.write_log("  🐞 Crash-logger → при ошибке создаётся <имя>_crash.log рядом с exe.")
        self.write_log("")
        self.write_log("Основные опции — чипы справа; редкие настройки — в «⚙ Ещё».")

    # ---------- icon preview / style ----------
    def _current_icon_style(self):
        """Ключ выбранного стиля фона ('' = как в пресете).
        Задаётся кликом по стилю в окне выбора иконок."""
        return getattr(self, "_icon_style", "") or ""

    def _update_icon_preview(self, name=None):
        if name is None:
            name = self.builtin_icon_combo.currentText()
        if name and name != NO_BUILTIN_ICON and name in BUILTIN_ICONS:
            style = self._current_icon_style() or None
            self.icon_preview.setPixmap(make_preview_pixmap(name, 40, style))
            self.icon_preview.setToolTip(
                f"{name} — {ICON_STYLE_LABELS.get(style or '', 'Как в пресете')}"
            )
        else:
            self.icon_preview.clear()
            self.icon_preview.setToolTip("")
        for qn, qb in getattr(self, "_quick_icon_btns", {}).items():
            qb.setChecked(qn == name)

    def _restore_icon_style(self):
        self._icon_style = self.settings.value("icon_style", "", type=str) or ""
        self._update_icon_preview()

    # ---------- choose paths ----------
    def choose_main_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выбери главный Python-файл", "",
            "Python files (*.py *.pyw);;All files (*.*)"
        )
        if not path:
            return
        self._set_main_file(path)

    def choose_project_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Выбери папку проекта")
        if folder:
            self.project_dir_edit.setText(folder)
            self._apply_project_defaults(Path(folder))

    def _apply_project_defaults(self, folder):
        folder = Path(folder).resolve()
        out = project_output_dir(folder)
        self.output_dir_edit.setText(str(out))
        self.write_log(f"Папка EXE установлена рядом с проектом: {out}")

    def choose_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Выбери папку для готового EXE")
        if folder:
            self.output_dir_edit.setText(folder)

    def choose_icon(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выбери иконку .ico", "", "Icon files (*.ico);;All files (*.*)"
        )
        if path:
            self.icon_edit.setText(path)
            self.builtin_icon_combo.setCurrentText(NO_BUILTIN_ICON)

    # ---------- Выбор Python для сборки ----------
    def _current_python_mode(self):
        return self.target_os_combo.currentData() or "current"

    def _current_build_arch(self):
        return self.arch_combo.currentData() or "amd64"

    def _on_build_arch_changed(self):
        self.settings.setValue("build_arch", self._current_build_arch())
        self._refresh_python_info()

    def _on_target_os_changed(self):
        mode = self._current_python_mode()
        self.settings.setValue("python_mode", mode)
        # Поле «свой путь» видно только в режиме custom.
        is_custom = (mode == "custom")
        self.python_path_lbl.setVisible(is_custom)
        self.python_exe_edit.setVisible(is_custom)
        self.python_browse_btn.setVisible(is_custom)
        # Выбор архитектуры имеет смысл только для авто-скачиваемых Python.
        self.arch_combo.setEnabled(mode in ("win7", "win10", "win11"))
        self._refresh_python_info()

    def _choose_python_exe(self):
        start_dir = ""
        cur = self.python_exe_edit.text().strip()
        if cur and Path(cur).exists():
            start_dir = str(Path(cur).parent)
        path, _ = QFileDialog.getOpenFileName(
            self, "Выбери python.exe для сборки", start_dir,
            "Python executable (python.exe pythonw.exe);;All files (*.*)"
        )
        if path:
            self.python_exe_edit.setText(path)
            self._on_python_exe_changed()

    def _on_python_exe_changed(self):
        path = self.python_exe_edit.text().strip()
        self.settings.setValue("python_exe", path)
        self._refresh_python_info()

    def _check_python_exe(self):
        """Кнопка «Проверить»: показывает что будет использовано в текущем режиме."""
        mode = self._current_python_mode()
        spec = PORTABLE_PYTHONS.get(mode, {})
        if mode in ("current", "custom"):
            path = self.python_exe_edit.text().strip() if mode == "custom" else ""
            if mode == "custom" and not path:
                QMessageBox.warning(self, "Путь не задан", "Укажи путь к python.exe.")
                return
            # Проверка в фоне — окно не замирает (до 15 с на запуск python).
            self.set_status("Проверка Python...")
            self._start_probe(path, lambda p, info, m=mode: self._show_probe_result(m, info))
            return

        # Portable режим
        version = spec.get("version", "")
        arch = self._current_build_arch()
        ready = is_portable_python_ready(version, arch)
        msg = (
            f"Режим: {spec.get('label', '')}\n"
            f"Версия Python: {version} ({arch})\n"
            f"Папка кэша: {portable_python_dir(version, arch)}\n"
            f"Статус: {'✓ уже скачан и готов' if ready else '⬇ будет скачан при первой сборке (~30 МБ)'}\n\n"
            f"{spec.get('note', '')}"
        )
        QMessageBox.information(self, "Portable Python", msg)

    def _start_probe(self, path, callback):
        """Запускает PythonProbeWorker; callback(path, info) — в GUI-потоке."""
        w = PythonProbeWorker(path)
        w.done.connect(callback)
        w.finished.connect(lambda w=w: self._probe_workers.remove(w) if w in self._probe_workers else None)
        self._probe_workers.append(w)
        w.start()

    def _show_probe_result(self, mode, info):
        self.set_status("")
        title = "Текущий Python" if mode == "current" else "Свой Python"
        if info.get("ok"):
            QMessageBox.information(
                self, title,
                f"Python: {info.get('exe', '?')}\n"
                f"Версия: {info.get('version', '?')} ({info.get('arch', '?')})\n"
                f"PyInstaller: {'установлен' if info.get('has_pyinstaller') else 'НЕ установлен (будет авто-установка)'}"
            )
        else:
            QMessageBox.warning(self, "Python не работает", info.get("error") or "Неизвестная ошибка")

    def _on_probe_label(self, path, info):
        # Ответ мог устареть — пользователь уже сменил путь/режим.
        if self._current_python_mode() != "custom" or self.python_exe_edit.text().strip() != path:
            return
        if info.get("ok"):
            pi_txt = "PyInstaller: ✓" if info.get("has_pyinstaller") else "PyInstaller: ✗ (поставится авто)"
            self.python_info_lbl.setText(f"📁 {info['version']} ({info['arch']})  •  {pi_txt}")
        else:
            self.python_info_lbl.setText(f"❌ Python не работает: {info.get('error')}")

    def _refresh_python_info(self):
        mode = self._current_python_mode()
        spec = PORTABLE_PYTHONS.get(mode, {})
        if mode == "current":
            ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            self.python_info_lbl.setText(f"🐍 Будет использован текущий Python {ver}")
            return
        if mode == "custom":
            path = self.python_exe_edit.text().strip()
            if not path:
                self.python_info_lbl.setText("📁 Укажи путь к python.exe")
                return
            if self._restoring:
                # Не запускаем exe из настроек автоматически при старте.
                self.python_info_lbl.setText(f"📁 {path}  •  нажми «Проверить»")
                return
            self.python_info_lbl.setText("📁 Проверка python.exe...")
            self._start_probe(path, self._on_probe_label)
            return
        version = spec.get("version", "")
        arch = self._current_build_arch()
        ready = is_portable_python_ready(version, arch)
        status = "✓ готов (кэш)" if ready else "⬇ будет скачан при сборке (~30 МБ)"
        self.python_info_lbl.setText(f"🪟 Python {version} ({arch})  •  {status}")

    def _restore_python_exe(self):
        saved_mode = self.settings.value("python_mode", "current", type=str) or "current"
        saved_path = self.settings.value("python_exe", "", type=str) or ""
        saved_arch = self.settings.value("build_arch", "amd64", type=str) or "amd64"
        for i in range(self.target_os_combo.count()):
            if self.target_os_combo.itemData(i) == saved_mode:
                self.target_os_combo.setCurrentIndex(i)
                break
        for i in range(self.arch_combo.count()):
            if self.arch_combo.itemData(i) == saved_arch:
                self.arch_combo.setCurrentIndex(i)
                break
        if saved_path:
            self.python_exe_edit.setText(saved_path)
        self._restoring = True
        try:
            self._on_target_os_changed()
        finally:
            self._restoring = False

    def _choose_ffmpeg(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выбери ffmpeg.exe (или ffprobe.exe)", "",
            "Executables (*.exe);;All files (*.*)"
        )
        if path:
            self.ffmpeg_edit.setText(path)
            self.bundle_ffmpeg_chk.setChecked(True)

    def _download_ffmpeg(self):
        # Целевая папка — рядом с проектом (или с приложением, если проект ещё не выбран).
        base = self._current_project_or_app_dir()
        target = Path(base) / "ffmpeg"

        if self.is_busy:
            return

        # Если уже есть — просто прописать путь.
        if (target / "ffmpeg.exe").exists() and (target / "ffprobe.exe").exists():
            self.ffmpeg_edit.setText(str(target))
            self.bundle_ffmpeg_chk.setChecked(True)
            self.write_log(f"ffmpeg уже на месте: {target}")
            QMessageBox.information(self, "ffmpeg готов", f"ffmpeg уже скачан:\n{target}")
            return

        confirm = QMessageBox.question(
            self, "Скачать ffmpeg?",
            f"Скачать официальную Win64-сборку ffmpeg (~70 МБ) в папку:\n\n{target}\n\n"
            f"После скачивания «Путь к ffmpeg» и «📦 Bundle ffmpeg в EXE» включатся автоматически.\n"
            f"Продолжить?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if confirm != QMessageBox.Yes:
            return

        self._stop_requested = False
        self.set_busy(True)
        self.set_status("Скачивание ffmpeg...")
        self.download_ffmpeg_btn.setEnabled(False)
        self.download_ffmpeg_btn.setText("Скачивание...")

        self._ffmpeg_worker = FfmpegDownloadWorker(target)
        self._ffmpeg_worker.log.connect(self.write_log)
        self._ffmpeg_worker.progress.connect(
            lambda p: self.set_status(f"Скачивание ffmpeg: {p}%")
        )
        self._ffmpeg_worker.done.connect(self._on_ffmpeg_done)
        self._ffmpeg_worker.failed.connect(self._on_ffmpeg_failed)
        self._ffmpeg_worker.start()

    def _on_ffmpeg_done(self, folder):
        self.set_busy(False)
        self.download_ffmpeg_btn.setEnabled(True)
        self.download_ffmpeg_btn.setText("⬇ Скачать ffmpeg")
        self.ffmpeg_edit.setText(folder)
        self.bundle_ffmpeg_chk.setChecked(True)
        self.set_status(f"ffmpeg готов: {folder}")
        QMessageBox.information(
            self, "ffmpeg скачан",
            f"ffmpeg распакован в:\n{folder}\n\n"
            f"«📦 Bundle ffmpeg в EXE» включён автоматически. "
            f"Можно нажимать «Конвертировать в EXE»."
        )

    def _on_ffmpeg_failed(self, text):
        self.set_busy(False)
        self.download_ffmpeg_btn.setEnabled(True)
        self.download_ffmpeg_btn.setText("⬇ Скачать ffmpeg")
        if self._stop_requested:
            self.set_status("Скачивание остановлено")
            return
        self.set_status("Ошибка скачивания ffmpeg")
        QMessageBox.critical(
            self, "Не удалось скачать ffmpeg",
            f"{text}\n\nМожно скачать вручную с https://www.gyan.dev/ffmpeg/builds/ "
            f"и указать путь в поле «Путь к ffmpeg»."
        )

    # ---------- icon picker / export ----------
    def open_icon_picker(self):
        # Диалог строится один раз и переиспользуется — открытие мгновенное.
        dlg = getattr(self, "_icon_picker_dlg", None)
        if dlg is None:
            dlg = IconPickerDialog(self)
            dlg.chosen.connect(self._on_icon_picked)
            self._icon_picker_dlg = dlg
        dlg.search_edit.clear()
        dlg.exec()

    def _on_icon_picked(self, name, style=""):
        self.builtin_icon_combo.setCurrentText(name)
        self._icon_style = style
        self.settings.setValue("icon_style", style)
        self.icon_edit.clear()
        self._update_icon_preview()
        style_txt = f", стиль: {ICON_STYLE_LABELS.get(style)}" if style else ""
        self.write_log(f"Выбрана встроенная иконка: {name}{style_txt}")

    def export_icons_clicked(self):
        folder = self._current_workspace_dir()
        folder.mkdir(parents=True, exist_ok=True)
        try:
            icons_dir, created = export_all_builtin_icons(folder)
            self.write_log(f"Экспортировано иконок: {len(created)}")
            self.write_log(f"Папка: {icons_dir}")
            QMessageBox.information(self, "Готово", f"Иконки сохранены:\n{icons_dir}")
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", str(exc))

    def open_output_dir(self):
        folder = self._current_output_dir()
        try:
            folder.mkdir(parents=True, exist_ok=True)
            if sys.platform.startswith("win"):
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as exc:
            QMessageBox.warning(self, "Папка EXE", f"Не удалось открыть папку:\n{folder}\n\n{exc}")

    # ---------- helpers ----------
    def _current_project_or_app_dir(self):
        project = self.project_dir_edit.text().strip()
        if project and Path(project).exists():
            return Path(project).resolve()
        main_file = self.main_file_edit.text().strip()
        if main_file and Path(main_file).exists():
            return Path(main_file).resolve().parent
        return app_base_dir()

    def _current_workspace_dir(self):
        project = self.project_dir_edit.text().strip()
        if project and Path(project).exists():
            return project_workspace_dir(Path(project))
        main_file = self.main_file_edit.text().strip()
        if main_file and Path(main_file).exists():
            return project_workspace_dir(Path(main_file).resolve().parent)
        return fallback_workspace_dir()

    def _current_output_dir(self):
        output = self.output_dir_edit.text().strip()
        if output:
            return Path(output)
        project = self._current_project_or_app_dir()
        if project == app_base_dir():
            return fallback_output_dir()
        return project_output_dir(project)

    def clear_log(self):
        self.log_view.clear()

    def copy_log(self):
        text = self.log_view.toPlainText()
        QGuiApplication.clipboard().setText(text)
        prev = self.copy_log_btn.text()
        self.copy_log_btn.setText("Скопировано ✓")
        # Возврат текста через короткую задержку.
        QTimer.singleShot(1200, lambda: self.copy_log_btn.setText(prev))
        self.set_status(f"Лог скопирован в буфер ({len(text)} символов)")

    _LOG_COLORS = (
        (("❌", "Ошибка", "ОШИБКА", "ERROR", "Traceback", "FAILED"), "#e5534b"),
        (("⚠", "WARNING", "Предупреж", "не найден"), "#d4a72c"),
        (("✓", "✅", "Готово", "Успешно"), "#3fb950"),
    )

    def write_log(self, text=""):
        """Лог с подсветкой: ошибки — красным, предупреждения — жёлтым, успех — зелёным."""
        text = str(text)
        color = ""
        for keys, col in self._LOG_COLORS:
            if any(k in text for k in keys):
                color = col
                break
        style = "white-space:pre-wrap;"
        if color:
            style += f"color:{color};"
        self.log_view.appendHtml(f'<span style="{style}">{html_escape(text) or "&nbsp;"}</span>')

    def set_status(self, text):
        self.status_label.setText(text)

    CONVERT_BTN_IDLE = "🚀  Сделать EXE"
    CONVERT_BTN_BUSY = "⏳  Идёт сборка..."

    def set_busy(self, busy):
        self.is_busy = busy
        self.analyze_btn.setEnabled(not busy)
        # Кнопка сборки: блокируем + явно показываем состояние текстом.
        self.convert_btn.setEnabled(not busy)
        self.convert_btn.setText(self.CONVERT_BTN_BUSY if busy else self.CONVERT_BTN_IDLE)
        self.progress_bar.setVisible(busy)
        self.stop_btn.setVisible(busy)
        self.stop_btn.setEnabled(busy)

    def _set_worker(self, w):
        """Назначает нового воркера, удерживая ссылку на предыдущего до
        завершения его потока (защита от 'Destroyed while thread is still running')."""
        old = self.worker
        if old is not None and old is not w and old.isRunning():
            self._retired_workers.append(old)
            old.finished.connect(
                lambda o=old: self._retired_workers.remove(o)
                if o in self._retired_workers else None
            )
        self.worker = w

    # ---------- меню стилей ----------
    def _build_style_menu(self):
        menu = QMenu(self)
        self._style_group = QActionGroup(self)
        self._style_group.setExclusive(True)
        self._style_actions = {}

        def add(name):
            a = QAction(name, self, checkable=True)
            a.triggered.connect(lambda _checked=False, n=name: self._apply_and_save(n))
            self._style_group.addAction(a)
            menu.addAction(a)
            self._style_actions[name] = a

        menu.addSection("Современные (рекомендуется)")
        for name in MODERN_THEMES.keys():
            add(name)
        menu.addSeparator()
        add(SYSTEM_DEFAULT)
        menu.addSeparator()
        menu.addSection("Системные стили Qt")
        for name in QStyleFactory.keys():
            add(name)
        menu.addSeparator()
        menu.addSection("Темы / цвета")
        for name in CUSTOM_PALETTES.keys():
            add(name)
        return menu

    def _apply_and_save(self, name):
        if self.app is None:
            return
        apply_style(self.app, name, self.default_style_name, self.default_palette)
        self.settings.setValue("style_v2", name)
        if name in self._style_actions:
            self._style_actions[name].setChecked(True)

    def _restore_style(self):
        if self.app is None:
            return
        # 0.8.0: по умолчанию — новая тёмная карточная тема.
        saved = self.settings.value("style_v2", MODERN_DARK, type=str)
        if saved not in self._style_actions:
            saved = MODERN_DARK
        self._apply_and_save(saved)

    def _on_max_compat_toggled(self, on):
        if on:
            self.onefile_chk.setChecked(True)
            self.collect_all_chk.setChecked(True)
            # Авто-опт и макс. совместимость взаимоисключающие.
            if self.auto_opt_chk.isChecked():
                self.auto_opt_chk.setChecked(False)

    def _on_auto_opt_toggled(self, on):
        if on:
            self.onefile_chk.setChecked(True)
            if self.max_compat_chk.isChecked():
                self.max_compat_chk.setChecked(False)

    def _toggle_expert(self, on):
        self.expert_box.setVisible(on)
        self.expert_btn.setText(self.EXPERT_BTN_ON if on else self.EXPERT_BTN_OFF)

    def show_about(self):
        text = (
            f"<h3>{APP_NAME}</h3>"
            f"<p>Версия: <b>{APP_VERSION}</b></p>"
            f"<p>Автор: <b>{APP_AUTHOR}</b></p>"
            f"<p>Графический сборщик Python-проектов в Windows EXE на базе PyInstaller.</p>"
            f"<p><b>Сделано:</b></p>"
            f"<ul>"
            f"<li>🌍 <b>«Универсальный EXE» (по умолчанию):</b> bundle VC++ Runtime DLL "
            f"(vcruntime140, msvcp140 и др.) прямо в exe + автоматический crash-logger. "
            f"Запускается на ЛЮБОМ ПК с Windows без установки чего-либо; при ошибке "
            f"создаёт файл <code>&lt;имя&gt;_crash.log</code> и показывает MessageBox.</li>"
            f"<li>⚡ <b>«Авто-оптимизация EXE»:</b> AST-сканер определяет используемые "
            f"подмодули Qt; лишние (QtWebEngine, Qt3D*, QtMultimedia и др.) исключаются. "
            f"Размер exe в <b>5–10 раз меньше</b>.</li>"
            f"<li>🐞 <b>«Отладочный EXE»:</b> пересборка с консолью + полным логом ошибок.</li>"
            f"<li>📦 <b>«Bundle ffmpeg»:</b> автопоиск ffmpeg/ffprobe в PATH и упаковка в exe — "
            f"для приложений на yt-dlp (склейка видео+аудио, MP3-конвертация без внешних файлов).</li>"
            f"<li>Анализ импортов (stdlib / локальные / внешние / неизвестные + полные dotted).</li>"
            f"<li>Генерация <code>requirements_detected.txt</code> и отчёта.</li>"
            f"<li>Встроенный набор иконок ({len(BUILTIN_ICONS)} шт.) с превью; экспорт всего набора.</li>"
            f"<li>Своя .ico, автоустановка PyInstaller, темы оформления, копирование лога.</li>"
            f"</ul>"
            f"<p>Папки сборки создаются рядом с проектом: "
            f"<code>EXE_Output/</code> и <code>_py_to_exe_builder/</code>.</p>"
        )
        QMessageBox.about(self, f"О программе — {APP_NAME}", text)

    def _validate_paths(self):
        main_file = Path(self.main_file_edit.text().strip())
        project_dir = Path(self.project_dir_edit.text().strip() or main_file.parent)
        output_text = self.output_dir_edit.text().strip()
        output_dir = Path(output_text) if output_text else project_output_dir(project_dir)

        if not main_file.exists() or main_file.suffix.lower() not in {".py", ".pyw"}:
            QMessageBox.warning(self, "Нет главного файла", "Выбери главный .py или .pyw файл проекта.")
            return None
        if not project_dir.exists() or not project_dir.is_dir():
            QMessageBox.warning(self, "Нет папки проекта", "Выбери папку проекта.")
            return None

        icon_text = self.icon_edit.text().strip()
        if icon_text and (not Path(icon_text).is_file() or Path(icon_text).suffix.lower() != ".ico"):
            QMessageBox.warning(self, "Иконка", f"Своя иконка должна быть существующим .ico файлом:\n{icon_text}")
            return None

        self.output_dir_edit.setText(str(output_dir))
        app_name = self.app_name_edit.text().strip()
        if not app_name:
            app_name = main_file.stem
            self.app_name_edit.setText(app_name)
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            QMessageBox.warning(self, "Папка EXE", f"Не удалось создать папку:\n{output_dir}\n\n{exc}")
            return None
        return main_file, project_dir, output_dir, app_name

    # ---------- actions: analyze ----------
    def start_analyze(self):
        if self.is_busy:
            return
        data = self._validate_paths()
        if not data:
            return
        main_file, project_dir, output_dir, _ = data

        self._stop_requested = False
        self.set_busy(True)
        self.set_status("Анализ...")
        w = AnalyzeWorker(main_file, project_dir, output_dir)
        w.log.connect(self.write_log)
        w.done.connect(self._on_analyze_done)
        w.failed.connect(self._on_worker_failed)
        self._set_worker(w)
        w.start()

    def _on_analyze_done(self, result):
        self.third_party_imports = result["third"]
        self.unknown_imports = result["unknown"]
        self.set_busy(False)
        self.set_status("Анализ завершен")

    # ---------- actions: convert ----------
    def start_convert(self):
        if self.is_busy:
            return
        data = self._validate_paths()
        if not data:
            return
        main_file, project_dir, output_dir, app_name = data

        # Пре-флайт: режим «Свой Python» требует валидный путь — иначе сборка
        # падает только в конце, уже после скачивания UPX/ffmpeg. Проверяем сразу.
        if self._current_python_mode() == "custom":
            custom = self.python_exe_edit.text().strip()
            if not custom or not Path(custom).is_file():
                QMessageBox.warning(
                    self, "Свой Python: путь не задан",
                    "Выбран режим «📁 Свой Python», но путь к python.exe не указан "
                    "или файл не найден.\n\n"
                    "Укажи python.exe в настройках Python — либо переключись на "
                    "«🐍 Текущий Python»."
                )
                return

        # Новая сборка — сбрасываем запомненный отказ от ffmpeg и флаг «Стоп».
        self._ffmpeg_declined = False
        self._stop_requested = False
        self._upx_ready_dir = None

        # Сначала анализ, потом сборка — двумя последовательными воркерами.
        self.set_busy(True)
        self.set_status("Анализ перед сборкой...")
        pre = AnalyzeWorker(main_file, project_dir, output_dir)
        pre.log.connect(self.write_log)
        pre.failed.connect(self._on_worker_failed)
        pre.done.connect(lambda result: self._after_pre_analyze(result, main_file, project_dir, output_dir, app_name))
        self._set_worker(pre)
        pre.start()

    def _after_pre_analyze(self, result, main_file, project_dir, output_dir, app_name):
        if self._stop_requested:
            self.set_busy(False)
            self.set_status("Сборка остановлена")
            return
        self.third_party_imports = result["third"]
        self.unknown_imports = result["unknown"]
        qt_used = result.get("qt_used") or {}
        uses_tkinter = bool(result.get("uses_tkinter"))

        # --- Авто-определение нужности ffmpeg ---
        needs_ffmpeg = project_needs_ffmpeg(self.third_party_imports)
        ffmpeg_path = self.ffmpeg_edit.text().strip()

        if needs_ffmpeg and not self._ffmpeg_declined:
            ffmpeg_pkgs = sorted(set(self.third_party_imports) & FFMPEG_DEPENDENT_PACKAGES)
            self.write_log("")
            self.write_log(f"📦 Проект использует {', '.join(ffmpeg_pkgs)} → нужен ffmpeg.")

            # 1) Если путь уже указан вручную — просто включаем bundle.
            if ffmpeg_path:
                self.bundle_ffmpeg_chk.setChecked(True)
                self.write_log(f"   Используется путь: {ffmpeg_path}")
            else:
                # 2) Ищем сами: подпапка проекта, PATH.
                found = None
                cand1 = Path(project_dir) / "ffmpeg" / "ffmpeg.exe"
                cand2 = Path(project_dir) / "ffmpeg.exe"
                path_bins = find_ffmpeg_binaries()
                if cand1.exists():
                    found = str(cand1.parent)
                elif cand2.exists():
                    found = str(Path(project_dir))
                elif path_bins:
                    found = str(Path(path_bins[0]).parent)

                if found:
                    self.ffmpeg_edit.setText(found)
                    self.bundle_ffmpeg_chk.setChecked(True)
                    self.write_log(f"   ffmpeg найден: {found} → будет включён в EXE.")
                else:
                    # 3) Не найден — предлагаем скачать
                    self.write_log("   ffmpeg не найден ни в проекте, ни в PATH.")
                    reply = QMessageBox.question(
                        self, "Нужен ffmpeg",
                        f"Проект использует {', '.join(ffmpeg_pkgs)} — нужен ffmpeg.\n\n"
                        f"Скачать официальную Win64-сборку (~70 МБ) и включить в EXE?\n"
                        f"После скачивания сборка продолжится автоматически.",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
                    )
                    if reply == QMessageBox.Yes:
                        # Запускаем скачивание, после успеха — повторно вызовем _after_pre_analyze
                        self._pending_convert = (result, main_file, project_dir, output_dir, app_name)
                        target = Path(project_dir) / "ffmpeg"
                        self.set_status("Скачивание ffmpeg перед сборкой...")
                        self._ffmpeg_worker_pre = FfmpegDownloadWorker(target)
                        self._ffmpeg_worker_pre.log.connect(self.write_log)
                        self._ffmpeg_worker_pre.progress.connect(
                            lambda p: self.set_status(f"Скачивание ffmpeg: {p}%")
                        )
                        self._ffmpeg_worker_pre.done.connect(self._on_ffmpeg_pre_done)
                        self._ffmpeg_worker_pre.failed.connect(self._on_ffmpeg_pre_failed)
                        self._ffmpeg_worker_pre.start()
                        return  # выходим, сборка продолжится в _on_ffmpeg_pre_done
                    else:
                        self._ffmpeg_declined = True  # не спрашивать повторно в этой сборке
                        self.write_log("   Пользователь отказался скачивать ffmpeg. EXE будет без ffmpeg.")
                        self.write_log("   ⚠ Приложение в exe может не работать с операциями, требующими ffmpeg.")

        # --- Авто-скачивание UPX если включено сжатие ---
        if self.upx_chk.isChecked():
            workspace_dir = project_workspace_dir(project_dir)
            upx_dir = find_upx(workspace_dir) or self._upx_ready_dir
            if not upx_dir and not sys.platform.startswith("win"):
                self.write_log("⚠ UPX не найден, а авто-скачивание есть только для Windows — без UPX.")
                upx_dir = "-"
            if not upx_dir:
                self.write_log("")
                self.write_log("🗜 UPX-сжатие включено, но UPX не найден. Скачиваю...")
                # Сохраняем контекст для возврата
                self._pending_convert = (result, main_file, project_dir, output_dir, app_name)
                upx_target = workspace_dir / "upx"
                self.set_status("Скачивание UPX перед сборкой...")
                self._upx_worker_pre = UpxDownloadWorker(upx_target)
                self._upx_worker_pre.log.connect(self.write_log)
                self._upx_worker_pre.progress.connect(
                    lambda p: self.set_status(f"Скачивание UPX: {p}%")
                )
                self._upx_worker_pre.done.connect(self._on_upx_pre_done)
                self._upx_worker_pre.failed.connect(self._on_upx_pre_failed)
                self._upx_worker_pre.start()
                return  # выходим, сборка продолжится в _on_upx_pre_done
            else:
                self.write_log(f"🗜 UPX найден: {upx_dir}")

        # --- Подтверждение списка pip-пакетов (защита от typosquatting) ---
        mode = self._current_python_mode()
        install_names = []
        if mode != "current" or getattr(sys, "frozen", False):
            local = set(result.get("local") or [])
            cand = sorted({n for n in (list(self.third_party_imports) + list(self.unknown_imports))
                           if is_installable_dep(n) and n not in local})
            if cand:
                shown = [f"{n} → {import_to_pip_name(n)}" if import_to_pip_name(n) != n else n for n in cand]
                box = QMessageBox(self)
                box.setIcon(QMessageBox.Question)
                box.setWindowTitle("Установка пакетов через pip")
                box.setText(
                    "В выбранный Python будут установлены (только отсутствующие) пакеты с PyPI:\n\n"
                    + ", ".join(shown)
                    + "\n\nПроверь, что имена верные (опечатка = чужой пакет с PyPI).\n"
                    "«Да» — ставить, «Нет» — собирать без установки, «Отмена» — прервать."
                )
                box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                box.setDefaultButton(QMessageBox.Yes)
                ans = box.exec()
                if ans == QMessageBox.Cancel:
                    self.set_busy(False)
                    self.set_status("Сборка отменена")
                    return
                if ans == QMessageBox.Yes:
                    install_names = cand

        self.set_status("Сборка EXE...")
        params = {
            "install_names": install_names,
            "main_file": main_file,
            "project_dir": project_dir,
            "output_dir": output_dir,
            "app_name": app_name,
            "custom_icon": self.icon_edit.text().strip(),
            "builtin_icon": self.builtin_icon_combo.currentText(),
            "icon_style": self._current_icon_style(),
            "onefile": self.onefile_chk.isChecked(),
            "windowed": self.windowed_chk.isChecked(),
            "clean": self.clean_chk.isChecked(),
            "install_pyinstaller": self.install_pi_chk.isChecked(),
            "collect_all": self.collect_all_chk.isChecked(),
            "max_compat": self.max_compat_chk.isChecked(),
            "auto_optimize": self.auto_opt_chk.isChecked(),
            "universal": self.universal_chk.isChecked(),
            "debug_mode": self.debug_chk.isChecked(),
            "bundle_ffmpeg": self.bundle_ffmpeg_chk.isChecked(),
            "upx_enabled": self.upx_chk.isChecked(),
            "ffmpeg_path": self.ffmpeg_edit.text().strip(),
            "python_mode": self._current_python_mode(),
            "build_arch": self._current_build_arch(),
            "python_exe": self.python_exe_edit.text().strip(),
            "third": self.third_party_imports,
            "unknown": self.unknown_imports,
            "qt_used": qt_used,
            "uses_tkinter": uses_tkinter,
        }
        w = ConvertWorker(params)
        w.log.connect(self.write_log)
        w.stage.connect(self.set_status)
        w.done.connect(self._on_convert_done)
        w.failed.connect(self._on_worker_failed)
        self._set_worker(w)
        w.start()

    def _on_ffmpeg_pre_done(self, folder):
        self.ffmpeg_edit.setText(folder)
        self.bundle_ffmpeg_chk.setChecked(True)
        self.write_log(f"✓ ffmpeg готов: {folder}. Продолжаю сборку...")
        # Повторяем сборку с уже скачанным ffmpeg
        args, self._pending_convert = self._pending_convert, None
        if args:
            self._after_pre_analyze(*args)

    def _on_ffmpeg_pre_failed(self, text):
        if self._stop_requested:
            self._pending_convert = None
            self.set_busy(False)
            self.set_status("Сборка остановлена")
            return
        self.write_log(f"❌ Не удалось скачать ffmpeg: {text}")
        QMessageBox.critical(
            self, "Не удалось скачать ffmpeg",
            f"{text}\n\nСборка прервана. Можно:\n"
            f"• Скачать ffmpeg вручную с https://www.gyan.dev/ffmpeg/builds/\n"
            f"• Положить ffmpeg.exe в папку проекта\n"
            f"• Запустить сборку снова"
        )
        self.set_busy(False)
        self.set_status("Сборка прервана")
        self._pending_convert = None

    def _on_upx_pre_done(self, folder):
        self._upx_ready_dir = folder  # не ищем повторно (иначе цикл скачивания)
        self.write_log(f"✓ UPX готов: {folder}. Продолжаю сборку...")
        args, self._pending_convert = self._pending_convert, None
        if args:
            self._after_pre_analyze(*args)

    def _on_upx_pre_failed(self, text):
        # Не критично — собираем без UPX.
        self.write_log(f"⚠ Не удалось скачать UPX: {text}")
        self.write_log("Продолжаю сборку без UPX-сжатия.")
        self.upx_chk.setChecked(False)
        args, self._pending_convert = self._pending_convert, None
        if args:
            self._after_pre_analyze(*args)

    def _reveal_exe(self, exe_path):
        """Открывает папку с готовым EXE и выделяет сам файл."""
        p = Path(exe_path)
        try:
            if sys.platform.startswith("win"):
                # /select, — открыть проводник с выделенным файлом.
                # Одной строкой: путь с запятыми/пробелами в кавычках.
                subprocess.Popen(f'explorer /select,"{p}"')
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-R", str(p)])
            else:
                subprocess.Popen(["xdg-open", str(p.parent)])
            self.write_log(f"📂 Открыта папка: {p.parent}")
        except Exception as exc:
            self.write_log(f"⚠ Не удалось открыть папку с EXE: {exc}")

    def _on_convert_done(self, code, exe_path):
        self.set_busy(False)
        self.write_log("")
        if code == -2 or self._stop_requested:
            self.set_status("Сборка остановлена")
            self.write_log("⏹ Сборка остановлена пользователем.")
            return
        self.set_status("Готово")
        if code == 0:
            if exe_path:
                self.write_log(f"Готово: {exe_path}")
                self._reveal_exe(exe_path)  # папка открывается сразу, до модального окна
                QMessageBox.information(self, "Готово", f"EXE создан:\n{exe_path}")
            else:
                self.write_log("PyInstaller завершился без ошибки, но EXE не найден. Проверь лог.")
                QMessageBox.warning(self, "Проверь лог", "Сборка завершилась, но EXE не найден.")
        else:
            self.write_log(f"Ошибка сборки. Код: {code}")
            QMessageBox.critical(self, "Ошибка", "Сборка не завершилась. Проверь лог.")

    def _active_threads(self):
        ws = [self.worker, self._ffmpeg_worker, self._ffmpeg_worker_pre, self._upx_worker_pre,
              *self._retired_workers, *self._probe_workers]
        return [w for w in ws if w is not None and w.isRunning()]

    def stop_build(self):
        """Кнопка «Стоп»: отменяет текущую сборку/скачивание."""
        self._stop_requested = True
        self.stop_btn.setEnabled(False)
        self.set_status("Остановка...")
        self.write_log("⏹ Остановка...")
        for w in self._active_threads():
            cancel = getattr(w, "cancel", None)
            if cancel:
                cancel()
        if not self._active_threads():
            self.set_busy(False)
            self.set_status("Сборка остановлена")

    def closeEvent(self, event):
        """Закрытие во время работы: спросить, убить процессы, дождаться потоков."""
        if self._active_threads():
            ans = QMessageBox.question(
                self, "Идёт работа",
                "Идёт сборка или скачивание. Остановить и закрыть?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
            )
            if ans != QMessageBox.Yes:
                event.ignore()
                return
            self._stop_requested = True
            for w in self._active_threads():
                cancel = getattr(w, "cancel", None)
                if cancel:
                    cancel()
            for w in self._active_threads():
                w.wait(10000)
        event.accept()

    def _on_worker_failed(self, text):
        if self._stop_requested:
            self.set_busy(False)
            self.set_status("Сборка остановлена")
            self.write_log(f"⏹ Остановлено: {text}")
            return
        self.set_busy(False)
        self.set_status("Ошибка")
        self.write_log(f"Ошибка: {text}")
        QMessageBox.critical(self, "Ошибка", text)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    default_style_name = app.style().objectName() if app.style() else ""
    default_palette = QPalette(app.palette())
    win = ExeBuilderWindow(app, default_style_name, default_palette)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
