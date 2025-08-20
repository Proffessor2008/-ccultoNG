import hashlib
import json
import mimetypes
import os
import shutil
import sys
import tempfile
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import Tuple, Optional, List, Callable

import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

# ───────────────────────────────────────────────
# 🎨 ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ───────────────────────────────────────────────
VERSION = "0.0.7"
AUTHOR = "MustaNG"
PASSWORD_HASH = "f6ee94ecb014f74f887b9dcc52daecf73ab3e3333320cadd98bcb59d895c52f5"

# Константы для LSB-метода
HEADER_SIZE_BITS = 32  # Размер заголовка (биты)
PROGRESS_UPDATE_INTERVAL = 1000  # Частота обновления прогресса (биты)
MIN_DATA_LEN = 8  # Минимальный размер данных (биты)
MAX_DATA_LEN = 100 * 1024 * 1024 * 8  # Максимальный размер данных (100 МБ в битах)

# Улучшенные современные темы с плавными градиентами и закруглениями
THEMES = {
    "Тёмная": {
        "name": "Тёмная",
        "bg": "#0D1117",  # Очень тёмный фон (GitHub Dark)
        "fg": "#E6EDF3",  # Светлый текст
        "accent": "#58A6FF",  # Акцентный синий (GitHub Blue)
        "accent_hover": "#79B8FF",  # Акцент при наведении
        "accent_pressed": "#388BFD",  # Акцент при нажатии
        "secondary": "#161B22",  # Вторичный фон (карточки)
        "success": "#3FB950",  # Цвет успеха (зелёный)
        "error": "#F85149",  # Цвет ошибки (красный)
        "warning": "#D29922",  # Цвет предупреждения (оранжевый)
        "card": "#161B22",  # Фон карточек
        "border": "#30363D",  # Цвет границ
        "text": "#E6EDF3",  # Основной текст
        "text_secondary": "#8B949E",  # Вторичный текст
        "disabled": "#484F58",  # Отключенные элементы
        "scrollbar": "#30363D",  # Цвет полосы прокрутки
        "highlight": "#1F6FEB",  # Цвет выделения
        "shadow": "#010409",  # Цвет теней
        "radius": 8,  # Радиус закругления
        "padding": 10,  # Внутренние отступы
        "border_width": 1  # Ширина границ
    },
    "Светлая": {
        "name": "Светлая",
        "bg": "#FFFFFF",  # Белый фон
        "fg": "#24292F",  # Тёмный текст
        "accent": "#0969DA",  # Акцентный синий
        "accent_hover": "#218BFF",  # Акцент при наведении
        "accent_pressed": "#0652A5",  # Акцент при нажатии
        "secondary": "#F6F8FA",  # Вторичный фон (карточки)
        "success": "#1A7F37",  # Цвет успеха (зелёный)
        "error": "#CF222E",  # Цвет ошибки (красный)
        "warning": "#9A6700",  # Цвет предупреждения (оранжевый)
        "card": "#FFFFFF",  # Фон карточек
        "border": "#D0D7DE",  # Цвет границ
        "text": "#24292F",  # Основной текст
        "text_secondary": "#656D76",  # Вторичный текст
        "disabled": "#ABBAC5",  # Отключенные элементы
        "scrollbar": "#D0D7DE",  # Цвет полосы прокрутки
        "highlight": "#D0EBFF",  # Цвет выделения
        "shadow": "#D0D7DE",  # Цвет теней
        "radius": 8,
        "padding": 10,
        "border_width": 1
    },
    "Космос": {
        "name": "Космос",
        "bg": "#0A0A1A",  # Очень тёмный фон
        "fg": "#A0D8F1",  # Светло-голубой текст
        "accent": "#7B68EE",  # Акцентный фиолетовый
        "accent_hover": "#9B8AFF",  # Акцент при наведении
        "accent_pressed": "#5A4FCF",  # Акцент при нажатии
        "secondary": "#16213E",  # Вторичный фон (карточки)
        "success": "#00FFAA",  # Цвет успеха (зелёный)
        "error": "#FF3366",  # Цвет ошибки (красный)
        "warning": "#FFD166",  # Цвет предупреждения (жёлтый)
        "card": "#10102A",  # Фон карточек
        "border": "#3A3A8C",  # Цвет границ
        "text": "#A0D8F1",  # Основной текст
        "text_secondary": "#6A9CB5",  # Вторичный текст
        "disabled": "#4A4A8C",  # Отключенные элементы
        "scrollbar": "#2A2A5A",  # Цвет полосы прокрутки
        "highlight": "#1A1A3A",  # Цвет выделения
        "shadow": "#000000",  # Цвет теней
        "radius": 10,
        "padding": 12,
        "border_width": 1
    },
    "Океан": {
        "name": "Океан",
        "bg": "#001F3F",  # Очень тёмный фон
        "fg": "#A2D5F2",  # Светло-голубой текст
        "accent": "#0074D9",  # Акцентный синий
        "accent_hover": "#339CFF",  # Акцент при наведении
        "accent_pressed": "#0056A3",  # Акцент при нажатии
        "secondary": "#003366",  # Вторичный фон (карточки)
        "success": "#39FF14",  # Цвет успеха (зелёный)
        "error": "#FF4136",  # Цвет ошибки (красный)
        "warning": "#FFB74D",  # Цвет предупреждения (оранжевый)
        "card": "#002B5B",  # Фон карточек
        "border": "#0056B3",  # Цвет границ
        "text": "#A2D5F2",  # Основной текст
        "text_secondary": "#6A9CB5",  # Вторичный текст
        "disabled": "#005588",  # Отключенные элементы
        "scrollbar": "#004488",  # Цвет полосы прокрутки
        "highlight": "#003A66",  # Цвет выделения
        "shadow": "#000000",  # Цвет теней
        "radius": 8,
        "padding": 10,
        "border_width": 1
    },
    "Лес": {
        "name": "Лес",
        "bg": "#0D1F0A",  # Очень тёмный фон
        "fg": "#C8E6C9",  # Светло-зелёный текст
        "accent": "#4CAF50",  # Акцентный зелёный
        "accent_hover": "#81C784",  # Акцент при наведении
        "accent_pressed": "#388E3C",  # Акцент при нажатии
        "secondary": "#1B3E19",  # Вторичный фон (карточки)
        "success": "#8BC34A",  # Цвет успеха (зелёный)
        "error": "#F44336",  # Цвет ошибки (красный)
        "warning": "#FFB74D",  # Цвет предупреждения (оранжевый)
        "card": "#142811",  # Фон карточек
        "border": "#2E7D32",  # Цвет границ
        "text": "#C8E6C9",  # Основной текст
        "text_secondary": "#81C784",  # Вторичный текст
        "disabled": "#4A6947",  # Отключенные элементы
        "scrollbar": "#2E7D32",  # Цвет полосы прокрутки
        "highlight": "#1E461C",  # Цвет выделения
        "shadow": "#000000",  # Цвет теней
        "radius": 10,
        "padding": 12,
        "border_width": 1
    },
    "Ночная Неонка": {
        "name": "Ночная Неонка",
        "bg": "#0F0C29",  # Градиентный тёмный фон
        "fg": "#F0F0F0",  # Светлый текст
        "accent": "#FF00CC",  # Акцентный неоново-розовый
        "accent_hover": "#FF66FF",  # Акцент при наведении
        "accent_pressed": "#CC0099",  # Акцент при нажатии
        "secondary": "#302B63",  # Вторичный фон (карточки)
        "success": "#00FF9D",  # Цвет успеха (неоново-зелёный)
        "error": "#FF3366",  # Цвет ошибки (неоново-красный)
        "warning": "#FFD166",  # Цвет предупреждения (неоново-жёлтый)
        "card": "#24243E",  # Фон карточек
        "border": "#4A4A8C",  # Цвет границ
        "text": "#F0F0F0",  # Основной текст
        "text_secondary": "#B0B0B0",  # Вторичный текст
        "disabled": "#6A6A8C",  # Отключенные элементы
        "scrollbar": "#5A5A8C",  # Цвет полосы прокрутки
        "highlight": "#3A3A5A",  # Цвет выделения
        "shadow": "#000000",  # Цвет теней
        "radius": 12,
        "padding": 15,
        "border_width": 1
    },
    "Солнечный Закат": {
        "name": "Солнечный Закат",
        "bg": "#FFF8F0",  # Светлый фон
        "fg": "#333333",  # Тёмный текст
        "accent": "#FF6B6B",  # Акцентный оранжево-красный
        "accent_hover": "#FF8E8E",  # Акцент при наведении
        "accent_pressed": "#E55252",  # Акцент при нажатии
        "secondary": "#FFEAA7",  # Вторичный фон (карточки)
        "success": "#06D6A0",  # Цвет успеха (зелёный)
        "error": "#EF476F",  # Цвет ошибки (красный)
        "warning": "#FFD166",  # Цвет предупреждения (жёлтый)
        "card": "#FFFFFF",  # Фон карточек
        "border": "#DADADA",  # Цвет границ
        "text": "#333333",  # Основной текст
        "text_secondary": "#757575",  # Вторичный текст
        "disabled": "#BDBDBD",  # Отключенные элементы
        "scrollbar": "#CCCCCC",  # Цвет полосы прокрутки
        "highlight": "#FFF2E8",  # Цвет выделения
        "shadow": "#E0E0E0",  # Цвет теней
        "radius": 10,
        "padding": 12,
        "border_width": 1
    }
}

SUPPORTED_FORMATS = [("Изображения", "*.png *.bmp *.tiff *.tga *.jpg *.jpeg")]
STEGANO_METHODS = {
    "lsb": "Классический LSB",
    "noise": "Adaptive-Noise",
    "aelsb": "Adaptive-Edge-LSB"}
SETTINGS_FILE = "stego_settings.json"
HISTORY_FILE = "stego_history.json"
MAX_HISTORY = 10
MAX_FILE_SIZE_MB = 50  # Максимальный размер файла для скрытия (МБ)
CONFIG = {
    "MAX_FILE_SIZE_MB": MAX_FILE_SIZE_MB,
    "SETTINGS_FILE": SETTINGS_FILE,
    "HISTORY_FILE": HISTORY_FILE
}


# ───────────────────────────────────────────────
# 🛠️ УТИЛИТЫ
# ───────────────────────────────────────────────
class Utils:
    @staticmethod
    def safe_int(s: str, fallback: int = 0) -> int:
        try:
            return int(s)
        except (ValueError, TypeError):
            return fallback

    @staticmethod
    def truncate_path(path: str, max_len: int = 40) -> str:
        if len(path) <= max_len:
            return path
        return "..." + path[-(max_len - 3):]

    @staticmethod
    def format_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    @staticmethod
    def is_image_file(path: str) -> bool:
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_checksum(file_path: str) -> str:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    @staticmethod
    def get_free_space_mb(path: str) -> float:
        """Получает свободное место на диске в МБ"""
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(path),
                    ctypes.pointer(free_bytes),
                    None,
                    None
                )
                return free_bytes.value / (1024 * 1024)
            else:  # Unix
                statvfs = os.statvfs(path)
                return (statvfs.f_frsize * statvfs.f_bavail) / (1024 * 1024)
        except Exception:
            return float('inf')  # Если не удалось определить, считаем, что места достаточно

    @staticmethod
    def check_file_signature(file_path: str, expected_signatures: List[bytes]) -> bool:
        """Проверяет сигнатуру файла"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                return any(header.startswith(sig) for sig in expected_signatures)
        except Exception:
            return False

    @staticmethod
    def calculate_brightness(color: str) -> float:
        """Рассчитывает яркость цвета по формуле WCAG"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

        # sRGB to linear RGB
        def srgb_to_linear(c):
            c = c / 255.0
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4

        r_lin = srgb_to_linear(r)
        g_lin = srgb_to_linear(g)
        b_lin = srgb_to_linear(b)
        # Relative luminance
        L = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
        return L

    @staticmethod
    def get_contrast_ratio(color1: str, color2: str) -> float:
        """Рассчитывает коэффициент контраста между двумя цветами"""
        L1 = Utils.calculate_brightness(color1)
        L2 = Utils.calculate_brightness(color2)
        if L1 > L2:
            return (L1 + 0.05) / (L2 + 0.05)
        else:
            return (L2 + 0.05) / (L1 + 0.05)


# ───────────────────────────────────────────────
# 🎨 КЛАСС ДЛЯ РАБОТЫ С ТЕМАМИ
# ───────────────────────────────────────────────
class ThemeManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style()
        self.current_theme = "Тёмная"
        self.colors = THEMES[self.current_theme]

    def set_theme(self, theme_name: str) -> None:
        if theme_name not in THEMES:
            theme_name = "Тёмная"
        self.current_theme = theme_name
        self.colors = THEMES[theme_name]
        self._configure_styles()

    def _configure_styles(self) -> None:
        c = self.colors
        radius = c.get("radius", 0)
        padding = c.get("padding", 5)
        border_width = c.get("border_width", 1)

        # Настройка основного окна
        self.root.configure(bg=c["bg"])

        # Общие стили
        self.style.theme_use("clam")
        self.style.configure(".", background=c["bg"], foreground=c["fg"], font=("Segoe UI", 10))

        # Вкладки
        self.style.configure("TNotebook", background=c["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab",
                             background=c["secondary"],
                             foreground=c["fg"],
                             padding=(padding + 6, padding),
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             borderwidth=0)
        self.style.map("TNotebook.Tab",
                       background=[("selected", c["accent"]), ("active", c["secondary"])],
                       foreground=[("selected", "#ffffff"), ("active", c["accent"])])

        # Кнопки
        self.style.configure("TButton",
                             background=c["secondary"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10),
                             relief="flat",
                             padding=(padding, padding),
                             borderwidth=border_width,
                             bordercolor=c["border"])
        self.style.map("TButton",
                       background=[("active", c["accent_hover"]), ("pressed", c["accent_pressed"])],
                       foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

        # Акцентные кнопки
        self.style.configure("Accent.TButton",
                             background=c["accent"],
                             foreground="#ffffff",
                             font=("Segoe UI", 10, "bold"),
                             padding=(padding + 2, padding),
                             borderwidth=0,
                             relief="flat")
        self.style.map("Accent.TButton",
                       background=[("active", c["accent_hover"]), ("pressed", c["accent_pressed"])])

        # Карточки
        self.style.configure("Card.TFrame", background=c["card"])
        self.style.configure("Card.TLabelframe",
                             background=c["card"],
                             borderwidth=border_width,
                             relief="solid",
                             bordercolor=c["border"],
                             lightcolor=c["card"],
                             darkcolor=c["card"])
        self.style.configure("Card.TLabelframe.Label",
                             background=c["card"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10, "bold"))

        # Прогресс-бар
        self.style.configure("TProgressbar",
                             background=c["accent"],
                             troughcolor=c["secondary"],
                             bordercolor=c["border"],
                             lightcolor=c["accent"],
                             darkcolor=c["accent"],
                             thickness=12)

        # Поля ввода
        self.style.configure("TEntry",
                             fieldbackground=c["card"],
                             foreground=c["text"],
                             insertcolor=c["fg"],
                             bordercolor=c["border"],
                             lightcolor=c["card"],
                             darkcolor=c["card"],
                             relief="flat",
                             borderwidth=border_width,
                             padding=(padding, padding))

        # Выпадающие списки
        self.style.configure("TCombobox",
                             fieldbackground=c["card"],
                             foreground=c["text"],
                             selectbackground=c["accent"],
                             selectforeground="#ffffff",
                             relief="flat",
                             borderwidth=border_width,
                             arrowsize=12)
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", c["card"])])

        # Метки
        self.style.configure("TLabel",
                             background=c["bg"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10))

        # Вторичные метки
        self.style.configure("Secondary.TLabel",
                             background=c["bg"],
                             foreground=c["text_secondary"],
                             font=("Segoe UI", 9))

        # Текстовая область
        self.style.configure("TText",
                             background=c["card"],
                             foreground=c["text"],
                             insertbackground=c["fg"],
                             selectbackground=c["accent"],
                             selectforeground="#ffffff",
                             relief="flat",
                             borderwidth=border_width)

        # Радиокнопки
        self.style.configure("TRadiobutton",
                             background=c["bg"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10),
                             padding=(0, padding))

        # Чекбоксы
        self.style.configure("TCheckbutton",
                             background=c["bg"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10),
                             padding=(0, padding))

        # Стиль для области перетаскивания
        self.style.configure("DropZone.TFrame",
                             background=c["card"],
                             relief="groove",
                             borderwidth=border_width,
                             bordercolor=c["border"])

        # Стиль для заголовков групп
        self.style.configure("GroupHeader.TLabel",
                             background=c["bg"],
                             foreground=c["accent"],
                             font=("Segoe UI", 12, "bold"))

        # Стиль для кнопок с иконками
        self.style.configure("IconButton.TButton",
                             background=c["secondary"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10),
                             relief="flat",
                             padding=(padding - 2, padding - 4),
                             borderwidth=border_width,
                             bordercolor=c["border"])
        self.style.map("IconButton.TButton",
                       background=[("active", c["highlight"]), ("pressed", c["accent"])])

        # Стиль для кнопок действий (извлечь, сохранить, копировать)
        self.style.configure("Action.TButton",
                             background=c["secondary"],
                             foreground=c["fg"],
                             font=("Segoe UI", 10),
                             relief="flat",
                             padding=(padding, padding),
                             borderwidth=border_width,
                             bordercolor=c["border"])
        self.style.map("Action.TButton",
                       background=[("active", c["highlight"]), ("pressed", c["accent_pressed"])])

        # Стиль для статус-бара
        self.style.configure("StatusBar.TFrame",
                             background=c["secondary"])

        # Стиль для всплывающих уведомлений
        self.style.configure("Toast.TLabel",
                             background="#333333",
                             foreground="#ffffff",
                             font=("Segoe UI", 10),
                             relief="solid",
                             borderwidth=1)

        # Стиль для элементов истории
        self.style.configure("History.TLabel",
                             background=c["card"],
                             foreground=c["text_secondary"],
                             font=("Segoe UI", 9),
                             relief="flat",
                             borderwidth=0,
                             padding=(padding, padding // 2))
        self.style.map("History.TLabel",
                       background=[("active", c["highlight"])],
                       foreground=[("active", c["accent"])])

        # Стиль для области предпросмотра изображений
        self.style.configure("Preview.TFrame",
                             background=c["card"],
                             relief="solid",
                             borderwidth=border_width,
                             bordercolor=c["border"])

        # Стиль для текста ошибок
        self.style.configure("Error.TLabel",
                             background=c["bg"],
                             foreground=c["error"],
                             font=("Segoe UI", 10))

        # Стиль для текста успеха
        self.style.configure("Success.TLabel",
                             background=c["bg"],
                             foreground=c["success"],
                             font=("Segoe UI", 10))

        # Стиль для текста предупреждений
        self.style.configure("Warning.TLabel",
                             background=c["bg"],
                             foreground=c["warning"],
                             font=("Segoe UI", 10))

    @staticmethod
    def _adjust_color(hex_color: str, amount: int) -> str:
        """Осветлить или затемнить цвет"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        adjusted = []
        for c in rgb:
            c = max(0, min(255, c + amount))  # Ограничиваем значения от 0 до 255
            adjusted.append(c)
        return f"#{adjusted[0]:02x}{adjusted[1]:02x}{adjusted[2]:02x}"


# ───────────────────────────────────────────────
# 🖼️ КЛАСС ДЛЯ РАБОТЫ С ИЗОБРАЖЕНИЯМИ
# ───────────────────────────────────────────────
class ImageProcessor:
    @staticmethod
    def get_image_info(path: str) -> Tuple[int, int, int]:
        """Возвращает (ширина, высота, доступные биты)"""
        try:
            with Image.open(path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                w, h = img.size
                channels = len(img.getbands())  # Получаем количество каналов
                # Для RGBA учитываем только RGB каналы (3), для RGB тоже 3
                available_channels = channels  # RGB или RGBA «как есть»
                return w, h, w * h * available_channels
        except Exception as e:
            raise ValueError(f"Ошибка загрузки изображения: {str(e)}")

    @staticmethod
    def create_thumbnail(path: str, max_size: Tuple[int, int] = (200, 200)) -> ImageTk.PhotoImage:
        """Создает миниатюру изображения для предпросмотра"""
        try:
            with Image.open(path) as img:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                return ImageTk.PhotoImage(img)
        except Exception as e:
            raise ValueError(f"Ошибка создания миниатюры: {str(e)}")

    # ── 1.  НЕВИДИМОЕ СКРЫТИЕ (безопасная версия) ──
    @staticmethod
    def hide_data(container_path: str,
                  data: bytes,
                  password: str,
                  output_path: str,
                  method: str = "lsb",
                  compression_level: int = 9,
                  progress_callback: Optional[Callable[[float], None]] = None,
                  cancel_event: Optional[threading.Event] = None) -> None:
        def update(pct, msg):
            if progress_callback:
                progress_callback(pct)
            if cancel_event and cancel_event.is_set():
                raise Exception("Операция отменена")

        update(0, "Загрузка изображения")
        with Image.open(container_path) as img:
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            img_array = np.array(img, dtype=np.int16)  # int16 чтобы не было uint8-переполнения

        if method == "noise":
            # --- Adaptive-Noise---
            key = hashlib.sha512(password.encode()).digest()
            rng = np.random.default_rng(np.frombuffer(key, dtype=np.uint64))
            header = len(data).to_bytes(4, "big")
            payload = header + data
            bits = ''.join(f"{b:08b}" for b in payload)
            work = img_array[:, :, :3]
            flat = work.reshape(-1)
            # Canny без ошибки
            gray = cv2.cvtColor(img_array[:, :, :3].astype(np.uint8), cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 40, 80).reshape(-1)
            safe = np.where(edges == 0)[0]
            if len(safe) < len(bits):
                raise ValueError("Изображение слишком мало для невидимого метода")
            positions = rng.choice(safe, size=len(bits), replace=False)
            for i, bit_chr in enumerate(bits):
                if i % 2000 == 0:
                    update(100 * i / len(bits), "Скрытие…")
                pos = positions[i]
                bit = int(bit_chr)
                val = flat[pos]
                lsb = val & 1
                if lsb != bit:
                    delta = rng.choice([-1, 1])
                    new = val + delta
                    new = np.clip(new, 0, 255)  # ← защита от uint8-переполнения
                    flat[pos] = new
            stego_array = flat.reshape(work.shape).astype(np.uint8)
            if img_array.shape[-1] == 4:
                stego_array = np.dstack([stego_array, img_array[:, :, 3]])
        if method == "aelsb":
            # -------- Adaptive-Edge-LSB --------
            if img_array.shape[-1] == 4:
                work = img_array[:, :, :3]
            else:
                work = img_array
            gray = cv2.cvtColor(work.astype(np.uint8), cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 100)  # пороги можно подстроить
            safe_mask = (edges == 0)  # только «гладкие» пиксели
            flat = work.reshape(-1)
            safe_idx = np.where(safe_mask.reshape(-1))[0]

            header = len(data).to_bytes(4, "big")
            payload = header + data
            bits_needed = len(payload) * 8
            if bits_needed > len(safe_idx):
                raise ValueError("Изображение слишком мало для AELSB")

            key = hashlib.sha256(password.encode()).digest()
            rng = np.random.default_rng(np.frombuffer(key, dtype=np.uint32))
            positions = rng.choice(safe_idx, size=bits_needed, replace=False)

            bitstream = ''.join(f"{b:08b}" for b in payload)
            for i, bit_chr in enumerate(bitstream):
                if i % 2000 == 0:
                    update(100 * i / len(bitstream), "Скрытие (AELSB)...")
                pos = positions[i]
                bit = int(bit_chr)
                val = flat[pos] & ~1 | bit
                flat[pos] = np.clip(val, 0, 255)

            stego_array = flat.reshape(img_array.shape)
        else:
            # --- Классический LSB (без изменений) ---
            if img_array.shape[-1] == 4:
                img_array = img_array[:, :, :3]
            flat = img_array.reshape(-1)
            header = len(data).to_bytes(4, "big")
            payload = header + data
            bits_needed = len(payload) * 8
            if bits_needed > len(flat):
                raise ValueError("Изображение слишком мало")
            key = hashlib.sha256(password.encode()).digest()
            rng = np.random.default_rng(np.frombuffer(key, dtype=np.uint32))
            positions = rng.permutation(len(flat))[:bits_needed]
            bitstream = ''.join(f"{b:08b}" for b in payload)
            for i, bit_chr in enumerate(bitstream):
                if i % 2000 == 0:
                    update(100 * i / len(bitstream), "Скрытие…")
                pos = positions[i]
                bit = int(bit_chr)
                val = flat[pos] & ~1 | bit
                flat[pos] = np.clip(val, 0, 255)  # ← защита
            stego_array = flat.reshape(img_array.shape)

        update(100, "Сохранение")
        Image.fromarray(stego_array.astype(np.uint8)).save(output_path, "PNG", compress_level=compression_level)

    # ── 2.  ИЗВЛЕЧЕНИЕ -------------------------------------------------------
    @staticmethod
    def extract_data(image_path: str,
                     password: str,
                     method: str = "lsb",  # ← новый параметр
                     progress_callback: Optional[Callable[[float], None]] = None,
                     cancel_event: Optional[threading.Event] = None) -> bytes:
        def update(pct, msg):
            if progress_callback:
                progress_callback(pct)
            if cancel_event and cancel_event.is_set():
                raise Exception("Операция отменена")

        update(0, "Загрузка изображения")
        with Image.open(image_path) as img:
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            img_array = np.array(img, dtype=np.int16)  # ← int16

        # ---------- 1.  выбор метода ----------
        if method == "noise":
            # --- 1.1  Adaptive-Noise---
            key = hashlib.sha512(password.encode()).digest()
            rng = np.random.default_rng(np.frombuffer(key, dtype=np.uint64))
            work = img_array[:, :, :3].astype(np.int16)
            flat = work.reshape(-1)
            gray = cv2.cvtColor(img_array[:, :, :3], cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 40, 80).reshape(-1)
            safe = np.where(edges == 0)[0]
            # читаем заголовок (4 байта = 32 бита)
            positions = rng.choice(safe, size=32, replace=False)
            header_bits = [str(flat[p] & 1) for p in sorted(positions)]
            data_len = int(''.join(header_bits), 2)
            if data_len <= 0 or data_len > 50 * 1024 * 1024:
                raise ValueError("Некорректная длина данных")
            total_bits = 32 + data_len * 8
            positions = rng.choice(safe, size=total_bits, replace=False)
            data_bits = [str(flat[p] & 1) for p in sorted(positions)][32:]
            data = bytes(int(''.join(data_bits[i:i + 8]), 2)
                         for i in range(0, len(data_bits), 8))
        elif method == "aelsb":
            # -------- Adaptive-Edge-LSB extraction --------
            if img_array.shape[-1] == 4:
                work = img_array[:, :, :3]
            else:
                work = img_array
            gray = cv2.cvtColor(work.astype(np.uint8), cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 100)
            safe_mask = (edges == 0)
            flat = work.reshape(-1)
            safe_idx = np.where(safe_mask.reshape(-1))[0]

            key = hashlib.sha256(password.encode()).digest()
            rng = np.random.default_rng(np.frombuffer(key, dtype=np.uint32))

            # читаем заголовок
            positions32 = rng.choice(safe_idx, size=32, replace=False)
            header_bits = [str(flat[p] & 1) for p in sorted(positions32)]
            data_len = int(''.join(header_bits), 2)
            if data_len <= 0 or data_len > 50 * 1024 * 1024:
                raise ValueError("Некорректная длина данных (AELSB)")

            total_bits = 32 + data_len * 8
            positions = rng.choice(safe_idx, size=total_bits, replace=False)
            data_bits = [str(flat[p] & 1) for p in sorted(positions)][32:]
            data = bytes(int(''.join(data_bits[i:i + 8]), 2)
                         for i in range(0, len(data_bits), 8))
        else:  # classic LSB
            # --- 1.2  классический LSB ---
            if img_array.shape[-1] == 4:
                img_array = img_array[:, :, :3]
            flat = img_array.reshape(-1)
            key = hashlib.sha256(password.encode()).digest()
            rng = np.random.default_rng(np.frombuffer(key, dtype=np.uint32))
            positions = rng.permutation(len(flat))
            # header
            header_bits = [str(flat[p] & 1) for p in positions[:32]]
            data_len = int(''.join(header_bits), 2)
            if data_len <= 0 or data_len > 50 * 1024 * 1024:
                raise ValueError("Некорректная длина данных")
            total_bits = 32 + data_len * 8
            data_bits = [str(flat[p] & 1) for p in positions[32:total_bits]]
            data = bytes(int(''.join(data_bits[i:i + 8]), 2)
                         for i in range(0, len(data_bits), 8))

        update(100, "Готово")
        return data


# ───────────────────────────────────────────────
# 🔐 КЛАСС ДЛЯ ПРОВЕРКИ ПАРОЛЯ
# ───────────────────────────────────────────────
class PasswordDialog:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.password_correct = False
        self.dialog = tk.Toplevel(root)
        self.dialog.title("Введите пароль")
        self.dialog.geometry("350x300")  # Уменьшена высота
        self.dialog.resizable(False, False)
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)

        # Центрирование окна
        self.dialog.withdraw()
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - self.dialog.winfo_reqwidth()) // 2
        y = (self.dialog.winfo_screenheight() - self.dialog.winfo_reqheight()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        self.dialog.deiconify()

        # Создаем менеджер тем для диалога
        self.theme_manager = ThemeManager(self.dialog)
        self.theme_manager.set_theme("Тёмная")  # Устанавливаем тему по умолчанию для диалога
        self.colors = self.theme_manager.colors

        # Элементы интерфейса
        # Заголовок
        title_label = ttk.Label(self.dialog, text="🔐 Доступ к ØccultoNG", font=("Segoe UI", 14, "bold"),
                                style="GroupHeader.TLabel")
        title_label.pack(pady=(20, 10))

        # Подзаголовок
        subtitle_label = ttk.Label(self.dialog, text="Введите пароль для продолжения", style="Secondary.TLabel")
        subtitle_label.pack(pady=(0, 15))

        # Поле ввода пароля
        self.password_var = tk.StringVar()
        self.entry = ttk.Entry(self.dialog, textvariable=self.password_var, show="*", width=30, font=("Segoe UI", 11))
        self.entry.pack(pady=5, padx=20, fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.check_password())

        # Удален чекбокс "Запомнить пароль"

        # Метка для ошибок
        self.error_label = ttk.Label(self.dialog, text="", style="Error.TLabel")
        self.error_label.pack()

        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Войти", command=self.check_password, style="Accent.TButton").pack(side=tk.LEFT,
                                                                                                      padx=5)
        ttk.Button(btn_frame, text="Выход", command=self._on_close, style="TButton").pack(side=tk.LEFT, padx=5)

        # Фокус на поле ввода
        self.entry.focus_set()

        # Ожидание закрытия диалога
        self.dialog.transient(root)
        self.dialog.grab_set()
        root.wait_window(self.dialog)

    def check_password(self) -> None:
        entered = self.password_var.get()
        if not entered:
            self.error_label.config(text="Пароль не может быть пустым")
            return
        # Проверяем хеш пароля
        hash_obj = hashlib.sha256(entered.encode('utf-8'))
        if hash_obj.hexdigest() == PASSWORD_HASH:
            self.password_correct = True
            self.dialog.destroy()
        else:
            self.error_label.config(text="Неверный пароль")

    def _on_close(self) -> None:
        self.password_correct = False
        self.dialog.destroy()


# ───────────────────────────────────────────────
# 🧠 ОСНОВНОЕ ПРИЛОЖЕНИЕ
# ───────────────────────────────────────────────
class SteganographyUltimate:
    def __init__(self):
        # Создаём DnD-окно
        self.root = TkinterDnD.Tk()
        self.root.title(f"ØccultoNG v{VERSION}")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)

        # Проверка пароля перед инициализацией интерфейса
        password_dialog = PasswordDialog(self.root)
        if not password_dialog.password_correct:
            self.root.destroy()
            return

        # Иконка приложения
        try:
            self.root.iconbitmap(default=self.resource_path("icon.ico"))
        except:
            pass

        # Менеджер тем
        self.theme_manager = ThemeManager(self.root)

        # Загружаем настройки
        self.settings = self.load_settings()
        self.history = self.load_history()

        # Устанавливаем тему из настроек
        self.theme_manager.set_theme(self.settings.get("theme", "Тёмная"))
        self.colors = self.theme_manager.colors

        # Переменные
        self.img_path = tk.StringVar()
        self.extract_img_path = tk.StringVar()
        self.data_type = tk.StringVar(value=self.settings.get("data_type", "text"))
        self.method_var = tk.StringVar(value=self.settings.get("method", "lsb"))
        self.compression_level = tk.IntVar(value=self.settings.get("compression_level", 9))
        self.current_extracted = None
        self.is_dragging = False
        self.last_update_time = 0
        self.file_path_var = tk.StringVar()

        # Элементы интерфейса
        self.preview_img = None
        self.extract_preview = None
        self.text_input = None
        self.result_text = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.history_labels = []
        self.size_info = None

        # Для отмены операций
        self.cancel_event = threading.Event()
        self.operation_thread = None

        # Для временного хранения больших данных
        self.temp_extracted_file = None

        # Блокировка кнопок во время операций
        self.buttons_disabled = False

        # Toast
        self.toast_label = None
        self.toast_timer = None
        self._preview_photo = None  # для вкладки "Скрыть"
        self._extract_photo = None  # для вкладки "Извлечь"
        # Запомнить пароль (теперь всегда False)
        self.remember_password = False  # password_dialog.remember_var.get()

        self.setup_ui()
        self.bind_drag_drop()
        self.refresh_history()

    def resource_path(self, relative_path: str) -> str:
        """ Получает абсолютный путь к ресурсу """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def load_settings(self) -> dict:
        try:
            if os.path.exists(CONFIG["SETTINGS_FILE"]):
                with open(CONFIG["SETTINGS_FILE"], 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
        return {
            "theme": "Тёмная",
            "method": "lsb",
            "data_type": "text",
            "compression_level": 9,
            "window_size": "1000x800"
        }

    def save_settings(self) -> None:
        settings = {
            "theme": self.theme_manager.current_theme,
            "method": self.method_var.get(),
            "data_type": self.data_type.get(),
            "compression_level": self.compression_level.get(),
            "window_size": self.root.geometry()
        }
        try:
            with open(CONFIG["SETTINGS_FILE"], 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def load_history(self) -> list:
        try:
            if os.path.exists(CONFIG["HISTORY_FILE"]):
                with open(CONFIG["HISTORY_FILE"], 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    # Фильтруем только существующие файлы
                    valid_history = [h for h in history if os.path.exists(h)]
                    # Сохраняем только валидные записи
                    if len(valid_history) != len(history):
                        self.save_history(valid_history)
                    return valid_history[:MAX_HISTORY]
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
        return []

    def save_history(self, history: list) -> None:
        """Сохраняет историю в файл"""
        try:
            with open(CONFIG["HISTORY_FILE"], 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def save_to_history(self, path: str) -> None:
        if not path:
            return
        # Удаляем дубликаты и ограничиваем размер истории
        hist = [path] + [h for h in self.history if h != path and os.path.exists(h)]
        self.history = hist[:MAX_HISTORY]
        self.save_history(self.history)

    def setup_ui(self) -> None:
        # Основной контейнер
        main_frame = ttk.Frame(self.root, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Заголовок и меню
        self.create_header(main_frame)

        # Вкладки
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.create_hide_tab()
        self.create_extract_tab()
        self.create_settings_tab()

        # Статус бар
        self.create_status_bar(main_frame)

        # Toast
        self.create_toast()

    def create_header(self, parent: ttk.Frame) -> None:
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # Логотип и название
        title_frame = ttk.Frame(header_frame, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Заголовок программы
        title = ttk.Label(
            title_frame,
            text="ØccultoNG",
            font=("Segoe UI Variable Display", 22, "bold"),
            foreground=self.colors["accent"]
        )
        title.pack(side=tk.LEFT)

        version_label = ttk.Label(
            title_frame,
            text=f"v{VERSION}",
            font=("Segoe UI", 11),
            foreground=self.colors["text_secondary"]
        )
        version_label.pack(side=tk.LEFT, padx=(8, 0), pady=(5, 0))

        # Меню
        menu_frame = ttk.Frame(header_frame, style="Card.TFrame")
        menu_frame.pack(side=tk.RIGHT)

        help_btn = ttk.Button(
            menu_frame,
            text="Помощь",
            command=self.show_help,
            style="IconButton.TButton"
        )
        help_btn.pack(side=tk.LEFT, padx=5)

    def create_hide_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(frame, text="Скрыть данные")

        # Контейнер для изображения
        container = ttk.LabelFrame(
            frame,
            text="Изображение-контейнер",
            padding=15,
            style="Card.TLabelframe"
        )
        container.pack(fill=tk.X, pady=(0, 15))

        # Путь к изображению
        path_frame = ttk.Frame(container, style="Card.TFrame")
        path_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(path_frame, text="Путь:", style="TLabel").pack(side=tk.LEFT)

        path_entry = ttk.Entry(
            path_frame,
            textvariable=self.img_path,
            state='readonly',
            width=50,
            style="TEntry"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        browse_btn = ttk.Button(
            path_frame,
            text="Обзор...",
            command=self.select_image,
            style="IconButton.TButton"
        )
        browse_btn.pack(side=tk.LEFT)

        # Зона для перетаскивания
        drop_frame = ttk.Frame(container, style="DropZone.TFrame")
        drop_frame.pack(fill=tk.X, pady=10)

        self.drop_label = ttk.Label(
            drop_frame,
            text="📁 Перетащите изображение сюда или нажмите для выбора",
            anchor="center",
            font=("Segoe UI", 11),
            cursor="hand2",
            style="Secondary.TLabel"
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.drop_label.bind("<Button-1>", lambda e: self.select_image())
        # ----- Предпросмотр изображения -----
        self.preview_img = ttk.Label(container)
        self.preview_img.pack(pady=5)

        # Группа для данных
        data_group = ttk.LabelFrame(
            frame,
            text="Скрываемые данные",
            padding=15,
            style="Card.TLabelframe"
        )
        data_group.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Выбор типа данных
        type_frame = ttk.Frame(data_group, style="Card.TFrame")
        type_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(type_frame, text="Тип данных:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))

        ttk.Radiobutton(
            type_frame,
            text="Текст",
            variable=self.data_type,
            value="text",
            command=self.toggle_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Radiobutton(
            type_frame,
            text="Файл",
            variable=self.data_type,
            value="file",
            command=self.toggle_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT)

        # Текстовый ввод
        self.text_frame = ttk.Frame(data_group, style="Card.TFrame")
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_input = scrolledtext.ScrolledText(
            self.text_frame,
            height=10,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=1
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)

        # Файловый ввод
        self.file_frame = ttk.Frame(data_group, style="Card.TFrame")

        file_input_frame = ttk.Frame(self.file_frame, style="Card.TFrame")
        file_input_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(file_input_frame, text="Файл:", style="TLabel").pack(side=tk.LEFT)

        file_entry = ttk.Entry(
            file_input_frame,
            textvariable=self.file_path_var,
            state='readonly',
            width=40,
            style="TEntry"
        )
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            file_input_frame,
            text="Выбрать...",
            command=self.select_file,
            style="IconButton.TButton"
        ).pack(side=tk.LEFT)

        options_frame = ttk.Frame(frame, style="Card.TFrame")
        options_frame.pack(fill=tk.X, pady=(0, 15))

        # Метод скрытия
        method_frame = ttk.Frame(options_frame, style="Card.TFrame")
        method_frame.pack(side=tk.LEFT)

        ttk.Label(method_frame, text="Метод:", style="TLabel").pack(side=tk.LEFT)

        method_combo = ttk.Combobox(
            method_frame,
            textvariable=self.method_var,
            values=list(STEGANO_METHODS.keys()),
            state="readonly",
            width=20,
            style="TCombobox"
        )
        method_combo.pack(side=tk.LEFT, padx=5)

        # Степень сжатия PNG
        compression_frame = ttk.Frame(options_frame, style="Card.TFrame")
        compression_frame.pack(side=tk.LEFT, padx=(20, 0))

        ttk.Label(compression_frame, text="Сжатие PNG:", style="TLabel").pack(side=tk.LEFT, padx=(10, 0))

        compression_combo = ttk.Combobox(
            compression_frame,
            textvariable=self.compression_level,
            values=list(range(0, 10)),
            state="readonly",
            width=5,
            style="TCombobox"
        )
        compression_combo.pack(side=tk.LEFT, padx=5)

        # 📌 Информация о размере — теперь над кнопкой
        self.size_info = ttk.Label(
            frame,
            text="",
            font=("Segoe UI", 10),
            foreground=self.colors["text_secondary"]
        )
        self.size_info.pack(pady=(15, 5))  # 👈 подняли выше

        # 📌 Кнопка скрытия — теперь под шкалой
        self.hide_button = ttk.Button(
            frame,
            text="🔐 Скрыть данные",
            style="Accent.TButton",
            command=self.start_hide
        )
        self.hide_button.pack(pady=(5, 15))

    def create_extract_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(frame, text="Извлечь данные")

        # Контейнер для изображения
        container = ttk.LabelFrame(
            frame,
            text="Изображение с данными",
            padding=15,
            style="Card.TLabelframe"
        )
        container.pack(fill=tk.X, pady=(0, 15))

        # Путь к изображению
        path_frame = ttk.Frame(container, style="Card.TFrame")
        path_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(path_frame, text="Путь:", style="TLabel").pack(side=tk.LEFT)

        path_entry = ttk.Entry(
            path_frame,
            textvariable=self.extract_img_path,
            state='readonly',
            width=50,
            style="TEntry"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        browse_btn = ttk.Button(
            path_frame,
            text="Обзор...",
            command=self.select_extract_image,
            style="IconButton.TButton"
        )
        browse_btn.pack(side=tk.LEFT)

        # ----- Предпросмотр изображения -----
        self.extract_preview = ttk.Label(container)
        self.extract_preview.pack(pady=5)

        # Результат извлечения
        result_group = ttk.LabelFrame(
            frame,
            text="Извлечённые данные",
            padding=15,
            style="Card.TLabelframe"
        )
        result_group.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.result_text = scrolledtext.ScrolledText(
            result_group,
            height=12,
            font=("Consolas", 10),
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=1
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        btn_frame = ttk.Frame(frame, style="Card.TFrame")
        btn_frame.pack(pady=(10, 0))

        self.extract_button = ttk.Button(
            btn_frame,
            text="🔍 Извлечь",
            style="Action.TButton",
            command=self.start_extract
        )
        self.extract_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(
            btn_frame,
            text="💾 Сохранить",
            style="Action.TButton",
            command=self.save_extracted
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = ttk.Button(
            btn_frame,
            text="📋 Копировать",
            style="Action.TButton",
            command=self.copy_extracted
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)

        # История
        hist_frame = ttk.LabelFrame(
            frame,
            text="Последние файлы",
            padding=10,
            style="Card.TLabelframe"
        )
        hist_frame.pack(fill=tk.X, pady=(15, 0))

        # Создаем метки для истории
        self.history_labels = []
        for i in range(MAX_HISTORY):
            lbl = ttk.Label(
                hist_frame,
                text="",
                style="History.TLabel",
                cursor="hand2"
            )
            lbl.pack(anchor="w", pady=2)
            self.history_labels.append(lbl)

    def create_settings_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(frame, text="Настройки")

        # Группа внешнего вида
        appearance_group = ttk.LabelFrame(
            frame,
            text="Внешний вид",
            padding=15,
            style="Card.TLabelframe"
        )
        appearance_group.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            appearance_group,
            text="Тема интерфейса:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        theme_var = tk.StringVar(value=self.theme_manager.current_theme)
        theme_combo = ttk.Combobox(
            appearance_group,
            textvariable=theme_var,
            values=list(THEMES.keys()),
            state="readonly",
            style="TCombobox"
        )
        theme_combo.pack(fill=tk.X, pady=(0, 10))
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.change_theme(theme_var.get()))

        # Группа параметров
        params_group = ttk.LabelFrame(
            frame,
            text="Параметры",
            padding=15,
            style="Card.TLabelframe"
        )
        params_group.pack(fill=tk.X, pady=(0, 15))

        # Метод по умолчанию
        ttk.Label(
            params_group,
            text="Метод по умолчанию:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        method_combo = ttk.Combobox(
            params_group,
            textvariable=self.method_var,
            values=list(STEGANO_METHODS.keys()),
            state="readonly",
            style="TCombobox"
        )
        method_combo.pack(fill=tk.X, pady=(0, 10))

        # Тип данных по умолчанию
        ttk.Label(
            params_group,
            text="Тип данных по умолчанию:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        data_type_combo = ttk.Combobox(
            params_group,
            textvariable=self.data_type,
            values=["text", "file"],
            state="readonly",
            style="TCombobox"
        )
        data_type_combo.pack(fill=tk.X, pady=(0, 10))

        # Степень сжатия PNG по умолчанию
        ttk.Label(
            params_group,
            text="Степень сжатия PNG по умолчанию:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        compression_combo = ttk.Combobox(
            params_group,
            textvariable=self.compression_level,
            values=list(range(0, 10)),
            state="readonly",
            style="TCombobox"
        )
        compression_combo.pack(fill=tk.X, pady=(0, 10))

        # Кнопки
        btn_frame = ttk.Frame(frame, style="Card.TFrame")
        btn_frame.pack(pady=20)

        self.save_settings_button = ttk.Button(
            btn_frame,
            text="Сохранить настройки",
            style="Accent.TButton",
            command=self.save_settings_ui
        )
        self.save_settings_button.pack(side=tk.LEFT, padx=10)

        self.reset_settings_button = ttk.Button(
            btn_frame,
            text="Сбросить настройки",
            style="TButton",
            command=self.reset_settings
        )
        self.reset_settings_button.pack(side=tk.LEFT, padx=10)

        # Информация о программе
        info_group = ttk.LabelFrame(
            frame,
            text="О программе",
            padding=15,
            style="Card.TLabelframe"
        )
        info_group.pack(fill=tk.X, pady=(15, 0))

        info_text = f"""\
        ØccultoNG v{VERSION}  •  Made with 🖤 by {AUTHOR}

        Состав «магического зелья»:
        • Python 3.10+ – мозг и нервная система  
        • Pillow – глаза для работы с изображениями  
        • OpenCV – аналитик, ищущий «тихие» пиксели  
        • NumPy – скорость, миллионы операций за мгновение  
        • Tkinter + tkdnd2 – лицо и руки, удобный drag-and-drop  

        Лицензия: MIT – используй, модифицируй, делись свободно.
        """
        info_label = ttk.Label(
            info_group,
            text=info_text,
            justify=tk.LEFT,
            font=("Segoe UI", 9),
            style="Secondary.TLabel"
        )
        info_label.pack(anchor="w")

    def create_status_bar(self, parent: ttk.Frame) -> None:
        status_frame = ttk.Frame(parent, style="StatusBar.TFrame")
        status_frame.pack(fill=tk.X, pady=(10, 0))

        # Прогресс-бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # Кнопка отмены
        self.cancel_button = ttk.Button(
            status_frame,
            text="Отмена",
            command=self.cancel_operation,
            style="TButton"
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Статус
        self.status_label = ttk.Label(
            status_frame,
            text="Готов",
            font=("Segoe UI", 9),
            foreground=self.colors["text_secondary"],
            style="Secondary.TLabel"
        )
        self.status_label.pack(side=tk.RIGHT, padx=(10, 0))

        # Изначально скрываем прогресс-бар и кнопку отмены
        self.progress_bar.pack_forget()
        self.cancel_button.pack_forget()

    def create_toast(self) -> None:
        """Создает всплывающее уведомление"""
        self.toast_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="solid",
            bd=0,
            bg=self.colors.get("shadow", "#333333"),
            fg=self.colors.get("text", "#ffffff"),
            highlightthickness=1,
            highlightcolor=self.colors.get("accent", "#58A6FF")
        )
        self.toast_label.place_forget()

    def show_toast(self, message: str, duration: int = 2000) -> None:
        """Показывает всплывающее уведомление"""
        # Отменяем предыдущий таймер
        if self.toast_timer:
            self.root.after_cancel(self.toast_timer)

        # Позиционируем уведомление
        self.toast_label.config(text=message)
        self.toast_label.place(relx=0.5, rely=0.9, anchor="center")

        # Автоматически скрываем через duration миллисекунд
        self.toast_timer = self.root.after(duration, self.hide_toast)

    def hide_toast(self) -> None:
        """Скрывает всплывающее уведомление"""
        self.toast_label.place_forget()
        self.toast_timer = None

    def animate_drop(self) -> None:
        """Анимация при перетаскивании"""
        original_text = self.drop_label.cget("text")
        self.drop_label.config(text="✅ Файл загружен!", foreground=self.colors["success"])
        self.root.after(1500,
                        lambda: self.drop_label.config(text=original_text, foreground=self.colors["text_secondary"]))

    def bind_drag_drop(self) -> None:
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_image)

    def on_drop_image(self, event: tk.Event) -> None:
        path = event.data.strip('{}')
        if os.path.isfile(path) and Utils.is_image_file(path):
            self.img_path.set(path)
            self.update_size_info()
            self.animate_drop()
            self.show_toast("Файл загружен")
            self.update_thumbnail(path, self.preview_img)

        else:
            messagebox.showwarning(
                "Неверный формат",
                "Поддерживаются только изображения в форматах: PNG, BMP, TIFF, TGA, JPG, JPEG"
            )

    def show_image_preview(self, image_path: str) -> None:
        """Модальное окно предпросмотра изображения при загрузке."""
        if not os.path.exists(image_path):
            return

        preview_win = tk.Toplevel(self.root)
        preview_win.title(f"Предпросмотр – {os.path.basename(image_path)}")
        preview_win.geometry("600x600")
        preview_win.resizable(True, True)
        preview_win.transient(self.root)
        preview_win.grab_set()
        preview_win.focus_set()
        preview_win.bind("<Escape>", lambda e: preview_win.destroy())

        # Загружаем картинку и масштабируем
        with Image.open(image_path) as img:
            img.thumbnail((550, 550), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

        # Контейнер
        frame = ttk.Frame(preview_win, style="Card.TFrame")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Метка с изображением
        lbl = ttk.Label(frame, image=photo, style="Card.TFrame")
        lbl.image = photo  # защита от сборщика мусора
        lbl.pack(fill=tk.BOTH, expand=True)

        # Кнопка закрытия
        close_btn = ttk.Button(frame, text="Закрыть", command=preview_win.destroy)
        close_btn.pack(pady=10)

        # Центрируем окно
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - preview_win.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - preview_win.winfo_reqheight()) // 2
        preview_win.geometry(f"+{x}+{y}")

    def select_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Выберите изображение-контейнер",
            filetypes=SUPPORTED_FORMATS
        )
        if path:
            self.img_path.set(path)
            self.update_size_info()
            self.update_thumbnail(path, self.preview_img)

    def select_extract_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Выберите изображение с данными",
            filetypes=SUPPORTED_FORMATS
        )
        if path:
            self.extract_img_path.set(path)
            self.update_thumbnail(path, self.extract_preview)

    def select_file(self) -> None:
        path = filedialog.askopenfilename(title="Выберите файл для скрытия")
        if path:
            file_size = os.path.getsize(path) / (1024 * 1024)  # MB
            if file_size > CONFIG["MAX_FILE_SIZE_MB"]:
                messagebox.showwarning(
                    "Слишком большой файл",
                    f"Максимальный размер файла: {CONFIG['MAX_FILE_SIZE_MB']} МБ"
                )
                return
            self.file_path_var.set(path)
            self.update_size_info()

    def toggle_data_input(self) -> None:
        if self.data_type.get() == "text":
            self.file_frame.pack_forget()
            self.text_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.text_frame.pack_forget()
            self.file_frame.pack(fill=tk.X, pady=(10, 0))
        self.update_size_info()

    def update_size_info(self) -> None:
        current_time = time.time()
        if current_time - self.last_update_time < 0.5:  # Ограничение частоты обновлений
            return
        self.last_update_time = current_time

        try:
            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                self.size_info.config(text="Изображение не выбрано", style="Error.TLabel")
                return

            w, h, total_bits = ImageProcessor.get_image_info(img_path)
            used_bits = HEADER_SIZE_BITS  # Заголовок

            if self.data_type.get() == "text":
                text = self.text_input.get("1.0", tk.END).strip()
                if not text:
                    self.size_info.config(text="Текст не введён", style="Error.TLabel")
                    return
                raw_data = text.encode('utf-8')
            else:
                file_path = self.file_path_var.get()
                if not os.path.exists(file_path):
                    self.size_info.config(text="Файл не выбран", style="Error.TLabel")
                    return
                with open(file_path, 'rb') as f:
                    raw_data = f.read()

            # Учёт шифрования (теперь просто используем данные как есть)
            encrypted = raw_data
            used_bits += len(encrypted) * 8

            usage = (used_bits / total_bits) * 100

            if usage < 70:
                style = "Success.TLabel"
            elif usage < 90:
                style = "Warning.TLabel"
            else:
                style = "Error.TLabel"

            self.size_info.config(
                text=f"Размер изображения: {w}x{h} | Доступно: {Utils.format_size(total_bits / 8)} | " +
                     f"Требуется: {Utils.format_size(used_bits / 8)} ({usage:.1f}%)",
                style=style
            )

        except Exception as e:
            self.size_info.config(text=f"Ошибка: {str(e)}", style="Error.TLabel")

    def update_thumbnail(self, path: str, target_label: tk.Widget) -> None:
        """Создаёт и показывает миниатюру 200×200 в указанной метке."""
        try:
            with Image.open(path) as img:
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                tk_img = ImageTk.PhotoImage(img)
                target_label.configure(image=tk_img)
                target_label.image = tk_img  # защита от сборщика мусора
        except Exception as e:
            target_label.configure(image='', text=f'Ошибка: {e}')

    def validate_before_hide(self) -> bool:
        """Валидация перед скрытием данных"""
        img_path = self.img_path.get()
        if not img_path or not os.path.exists(img_path):
            messagebox.showerror("Ошибка", "Изображение не выбрано или не существует")
            return False

        # Проверка размера изображения
        try:
            w, h, total_bits = ImageProcessor.get_image_info(img_path)
            if w < 100 or h < 100:
                messagebox.showwarning("Предупреждение",
                                       "Изображение слишком маленькое. Рекомендуется использовать изображения размером не менее 100x100 пикселей.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка проверки изображения: {str(e)}")
            return False

        # Проверка данных
        if self.data_type.get() == "text":
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Ошибка", "Текст для скрытия не введён")
                return False
        else:
            file_path = self.file_path_var.get()
            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("Ошибка", "Файл для скрытия не выбран или не существует")
                return False

        return True

    def start_hide(self) -> None:
        if self.buttons_disabled:
            return
        if not self.validate_before_hide():
            return
        self.operation_thread = threading.Thread(target=self.hide_data, daemon=True)
        self.operation_thread.start()

    def hide_data(self) -> None:
        try:
            self.set_progress_mode(True, "Подготовка данных...")
            self.toggle_buttons(False)
            self.cancel_event.clear()

            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                raise ValueError("Изображение не выбрано или не существует")

            # Подготовка данных
            if self.data_type.get() == "text":
                text = self.text_input.get("1.0", tk.END).strip()
                if not text:
                    raise ValueError("Текст для скрытия не введён")
                data = text.encode('utf-8')
            else:
                file_path = self.file_path_var.get()
                if not file_path or not os.path.exists(file_path):
                    raise ValueError("Файл для скрытия не выбран или не существует")
                with open(file_path, 'rb') as f:
                    data = f.read()

            # Запрос места сохранения
            output = filedialog.asksaveasfilename(
                title="Сохранить изображение с данными",
                defaultextension=".png",
                filetypes=[("PNG изображения", "*.png")]
            )
            if not output:
                self.set_progress_mode(False)
                self.toggle_buttons(True)
                return

            # Проверка свободного места
            required_space_mb = os.path.getsize(img_path) / (1024 * 1024) * 1.1
            free_space_mb = Utils.get_free_space_mb(os.path.dirname(output) or '.')

            if free_space_mb < required_space_mb:
                raise ValueError(
                    f"Недостаточно свободного места на диске. Требуется: {Utils.format_size(required_space_mb * 1024 * 1024)}, Доступно: {Utils.format_size(free_space_mb * 1024 * 1024)}")

            # Скрытие данных
            start_time = time.time()

            def progress_callback(progress: float) -> None:
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")
                elapsed_time = time.time() - start_time
                speed = progress / 100 * len(data) / elapsed_time if elapsed_time > 0 else 0
                self.root.after(0, lambda: self.progress_var.set(progress))
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Скрытие данных... {progress:.1f}% | {Utils.format_size(speed)}/s"
                ))

            ImageProcessor.hide_data(
                img_path,
                data,
                "",  # Пустой пароль, так как шифрование отключено
                output,
                compression_level=self.compression_level.get(),
                progress_callback=progress_callback,
                cancel_event=self.cancel_event
            )

            # Сохранение в историю
            self.save_to_history(output)

            # Уведомление об успехе
            self.root.after(0, lambda: messagebox.showinfo(
                "Успех",
                f"Данные успешно скрыты в изображении!\nФайл сохранён: {output}"
            ))

        except Exception as e:
            if str(e) == "Операция отменена пользователем":
                self.root.after(0, lambda: messagebox.showinfo("Отмена", "Операция скрытия данных была отменена."))
            else:
                error_msg = f"Произошла ошибка при скрытии данных:\n{str(e)}"
                # Добавляем возможные причины и решения
                if "too small" in str(e).lower() or "слишком мало" in str(e).lower():
                    error_msg += "\nВозможные причины:\n- Изображение слишком маленькое для объема данных.\n- Выбран неверный метод скрытия."
                    error_msg += "\nРешения:\n- Используйте изображение большего размера.\n- Попробуйте другой метод скрытия данных."
                elif "not enough space" in str(e).lower() or "недостаточно" in str(e).lower():
                    error_msg += "\nВозможные причины:\n- Недостаточно свободного места на диске."
                    error_msg += "\nРешения:\n- Освободите место на диске и повторите попытку."
                elif "file not found" in str(e).lower() or "не найден" in str(e).lower():
                    error_msg += "\nВозможные причины:\n- Указанный файл не существует или был перемещен."
                    error_msg += "\nРешения:\n- Проверьте путь к файлу и повторите попытку."

                self.root.after(0, lambda: messagebox.showerror("Ошибка", error_msg))
        finally:
            self.set_progress_mode(False)
            self.toggle_buttons(True)

    def start_extract(self) -> None:
        if self.buttons_disabled:
            return
        self.operation_thread = threading.Thread(target=self.extract_data, daemon=True)
        self.operation_thread.start()

    def extract_data(self) -> None:
        try:
            self.set_progress_mode(True, "Подготовка к извлечению...")
            self.toggle_buttons(False)
            self.cancel_event.clear()
            path = self.extract_img_path.get()
            if not path or not os.path.exists(path):
                raise ValueError("Файл не выбран или не существует")
            # Извлечение данных
            start_time = time.time()

            def progress_callback(progress: float) -> None:
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")
                elapsed_time = time.time() - start_time
                # Для извлечения сложно рассчитать скорость, так как мы не знаем размер данных заранее
                self.root.after(0, lambda: self.progress_var.set(progress))
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Извлечение данных... {progress:.1f}% | {elapsed_time:.1f}s"
                ))

            extracted = ImageProcessor.extract_data(
                path,
                "",  # Пустой пароль, так как шифрование отключено
                progress_callback,
                cancel_event=self.cancel_event
            )
            # Определение типа данных и сохранение во временный файл при необходимости
            try:
                text = extracted.decode('utf-8')
                self.current_extracted = ('text', text)
                self.root.after(0, lambda: self.result_text.config(state='normal'))
                self.root.after(0, lambda: self.result_text.delete("1.0", tk.END))
                self.root.after(0, lambda: self.result_text.insert("1.0", text))
                self.root.after(0, lambda: self.result_text.config(state='disabled'))
            except UnicodeDecodeError:
                # Для бинарных данных создаем временный файл
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(extracted)
                    tmp_file_path = tmp_file.name
                # Определяем MIME-тип и расширение
                mime_type, encoding = mimetypes.guess_type(tmp_file_path)
                if mime_type:
                    ext = mimetypes.guess_extension(mime_type)
                    if ext:
                        # Переименовываем временный файл с правильным расширением
                        new_name = tmp_file_path + ext
                        os.rename(tmp_file_path, new_name)
                        tmp_file_path = new_name
                self.current_extracted = ('binary', tmp_file_path)
                self.root.after(0, lambda: self.result_text.config(state='normal'))
                self.root.after(0, lambda: self.result_text.delete("1.0", tk.END))
                self.root.after(0, lambda: self.result_text.insert(
                    "1.0",
                    f"Бинарные данные: {len(extracted)} байт\n" +
                    f"Хеш SHA-256: {hashlib.sha256(extracted).hexdigest()}\n" +
                    f"Временный файл: {tmp_file_path}"
                ))
                self.root.after(0, lambda: self.result_text.config(state='disabled'))
            # Добавление в историю
            self.save_to_history(path)
        except Exception as e:
            if str(e) == "Операция отменена пользователем":
                self.root.after(0, lambda: messagebox.showinfo("Отмена", "Операция извлечения данных была отменена."))
            else:
                error_msg = f"Произошла ошибка при извлечении данных:\n{str(e)}"
                # Добавляем возможные причины и решения
                if "incorrect data length" in str(e).lower() or "некорректная длина данных" in str(e).lower():
                    error_msg += "\nВозможные причины:\n- В изображении нет скрытых данных.\n- Использован неверный пароль (если применяется).\n- Изображение повреждено или изменено после скрытия данных."
                    error_msg += "\nРешения:\n- Убедитесь, что вы используете правильное изображение.\n- Проверьте правильность введенного пароля.\n- Попробуйте извлечь данные другим методом."
                elif "file not found" in str(e).lower() or "не найден" in str(e).lower():
                    error_msg += "\nВозможные причины:\n- Указанный файл не существует или был перемещен."
                    error_msg += "\nРешения:\n- Проверьте путь к файлу и повторите попытку."

                self.root.after(0, lambda: messagebox.showerror("Ошибка", error_msg))
        finally:
            self.set_progress_mode(False)
            self.toggle_buttons(True)

    def save_extracted(self) -> None:
        if not self.current_extracted:
            messagebox.showerror("Ошибка", "Сначала извлеките данные")
            return
        data_type, content = self.current_extracted
        if data_type == 'text':
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Сохранено", f"Текст сохранён в файл: {path}")
        else:
            # Для бинарных данных используем автоматическое определение MIME-типа
            mime_type, encoding = mimetypes.guess_type(content)
            default_ext = ".bin"
            filetypes = [("Бинарные файлы", "*.bin"), ("Все файлы", "*.*")]
            if mime_type:
                ext = mimetypes.guess_extension(mime_type)
                if ext:
                    default_ext = ext
                    # Добавляем тип файла в список
                    desc = mime_type.split('/')[0].capitalize() + " файлы"
                    filetypes.insert(0, (desc, f"*{ext}"))

            path = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                filetypes=filetypes
            )
            if path:
                shutil.copy(content, path)
                messagebox.showinfo("Сохранено", f"Данные сохранены в файл: {path}")

    def copy_extracted(self) -> None:
        if not self.current_extracted:
            messagebox.showerror("Ошибка", "Нет данных для копирования")
            return
        data_type, content = self.current_extracted
        if data_type == 'text':
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="Текст скопирован в буфер обмена")
        else:
            messagebox.showwarning("Внимание", "Бинарные данные нельзя скопировать в буфер")

    def set_progress_mode(self, active: bool, message: str = None) -> None:
        if active:
            self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)
            self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
            self.progress_var.set(0)
            if message:
                self.status_label.config(text=message)
        else:
            self.progress_bar.pack_forget()
            self.cancel_button.pack_forget()
            self.progress_var.set(0)
            self.status_label.config(text="Готов")

    def toggle_buttons(self, enable: bool) -> None:
        """Блокирует или разблокирует кнопки интерфейса"""
        self.buttons_disabled = not enable
        state = "normal" if enable else "disabled"
        # Кнопки на вкладке скрытия
        self.hide_button.config(state=state)
        # Кнопки на вкладке извлечения
        self.extract_button.config(state=state)
        self.save_button.config(state=state)
        self.copy_button.config(state=state)
        # Кнопки на вкладке настроек
        self.save_settings_button.config(state=state)
        self.reset_settings_button.config(state=state)

    def cancel_operation(self) -> None:
        """Отменяет текущую операцию"""
        self.cancel_event.set()
        self.status_label.config(text="Отмена операции...")

    def refresh_history(self) -> None:
        for i, lbl in enumerate(self.history_labels):
            if i < len(self.history):
                lbl.config(
                    text=f"{i + 1}. {Utils.truncate_path(self.history[i])}",
                    style="History.TLabel"
                )
                lbl.bind("<Button-1>", lambda e, idx=i: self.load_from_history(idx))
            else:
                lbl.config(text="", cursor="")

    def load_from_history(self, idx: int) -> None:
        if idx < len(self.history):
            path = self.history[idx]
            if os.path.exists(path):
                self.extract_img_path.set(path)
            else:
                messagebox.showwarning("Файл не найден", "Файл был перемещён или удалён.")
                del self.history[idx]
                self.refresh_history()

    def change_theme(self, theme_name: str) -> None:
        self.theme_manager.set_theme(theme_name)
        self.colors = self.theme_manager.colors
        self.refresh_history()
        # Обновляем цвет текста в информационных метках
        if hasattr(self, 'size_info'):
            self.size_info.config(foreground=self.colors["text_secondary"])
        if hasattr(self, 'status_label'):
            self.status_label.config(foreground=self.colors["text_secondary"])
        # Проверяем контрастность
        self.check_theme_contrast()
        # Обновляем цвета для текстовых областей, которые не управляются стилями ttk
        if self.text_input:
            self.text_input.config(
                bg=self.colors["card"],
                fg=self.colors["text"],
                insertbackground=self.colors["fg"],
                selectbackground=self.colors["accent"],
                selectforeground="#ffffff"
            )
        if self.result_text:
            self.result_text.config(
                bg=self.colors["card"],
                fg=self.colors["text"],
                insertbackground=self.colors["fg"],
                selectbackground=self.colors["accent"],
                selectforeground="#ffffff"
            )

        # Обновляем цвета всплывающего уведомления
        if self.toast_label:
            self.toast_label.config(
                bg=self.colors.get("shadow", "#333333"),
                fg=self.colors.get("text", "#ffffff"),
                highlightcolor=self.colors.get("accent", "#58A6FF")
            )

    def check_theme_contrast(self) -> None:
        """Проверяет контрастность темы по WCAG"""
        c = self.colors
        # Проверяем контраст между текстом и фоном
        contrast_ratio = Utils.get_contrast_ratio(c["fg"], c["bg"])
        if contrast_ratio < 4.5:  # WCAG AA standard
            print(
                f"Предупреждение: Низкая контрастность текста и фона в теме '{self.theme_manager.current_theme}'. Рекомендуется контраст не менее 4.5:1 для обычного текста.")

    def save_settings_ui(self) -> None:
        self.save_settings()
        messagebox.showinfo(
            "Настройки",
            "Настройки сохранены.\n" +
            "Некоторые изменения вступят в силу после перезапуска программы."
        )

    def reset_settings(self) -> None:
        if messagebox.askyesno(
                "Подтверждение",
                "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?"
        ):
            try:
                if os.path.exists(CONFIG["SETTINGS_FILE"]):
                    os.remove(CONFIG["SETTINGS_FILE"])
                if os.path.exists(CONFIG["HISTORY_FILE"]):
                    os.remove(CONFIG["HISTORY_FILE"])
                # Удаляем временные файлы
                if hasattr(self, 'temp_extracted_file') and self.temp_extracted_file and os.path.exists(
                        self.temp_extracted_file.name):
                    os.unlink(self.temp_extracted_file.name)

                messagebox.showinfo(
                    "Сброс настроек",
                    "Настройки сброшены. Программа будет закрыта."
                )
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сбросить настройки: {e}")

    def show_help(self) -> None:
        # ───────────────────────────────────────────────
        # 🆕 ОБНОВЛЁННОЕ ПОЛЬЗОВАТЕЛЬСКОЕ РУКОВОДСТВО
        # ───────────────────────────────────────────────
        # 1. Скопируйте этот блок в метод show_help() класса SteganographyUltimate
        # 2. Замените переменную help_text = f""" … """ на содержимое ниже
        # 3. Сохраните и перезапустите приложение – вкладка «Помощь» станет живой и понятной.
        # ───────────────────────────────────────────────

        help_text = f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║                 ØccultoNG v{VERSION} – Полное руководство               ║
        ║        «Скрывай данные как профи, извлекай как детектив»      ║
        ╚══════════════════════════════════════════════════════════════╝

        📌 Что это такое?
        ØccultoNG – это стеганографический «швейцарский нож» для изображений.  
        Он позволяет НЕЗАМЕТНО прятать внутри любой картинки:
        • текстовые сообщения, пароли, коды;  
        • любые файлы (PDF, ZIP, EXE, видео) до 50 МБ.  

        🔐 Всё, что вы спрячете, останется невидимым для глаза и большинства
        анализаторов. Главное – не теряйте исходное изображение и помните пароль!

        ──────────────────────────────────────────────────────────────
        🧩 Три метода скрытия: когда какой выбирать
        ──────────────────────────────────────────────────────────────
        1️⃣ LSB (Least Significant Bits) – «Классика»  
           • Просто подменяет последний бит каждого цветового канала.  
           • Плюсы: максимальная вместимость (≈ 12,5 % от размера картинки).  
           • Минусы: легко обнаружить специальными сканерами.  
           • Когда использовать: для быстрой передачи, когда важен объём, а не скрытность.

        2️⃣ Adaptive-Noise – «Невидимка»  
           • Добавляет/убирает ±1 к пикселю ТОЛЬКО в «гладких» областях (без рёбер).  
           • Плюсы: практически невозможно заметить визуально и статистически.  
           • Минусы: вместимость меньше (~30-50 % от LSB).  
           • Когда использовать: когда нужна максимальная незаметность.

        3️⃣ Adaptive-Edge-LSB (AELSB) – «Компромисс»  
           • Использует LSB, но только в пикселях, где нет резких перепадов цвета.  
           • Плюсы: баланс между вместимостью и скрытностью.  
           • Минусы: немного сложнее в реализации, требует CPU.  
           • Когда использовать: когда нужно «и много, и тихо».

        💡 Правило большого пальца  
        • Маленькая картинка + много данных → LSB.  
        • Соцсети/публикация → Adaptive-Noise.  
        • Всё остальное → AELSB.

        ──────────────────────────────────────────────────────────────
        🎮 Быстрый старт. 4 шага за 30 секунд
        ──────────────────────────────────────────────────────────────
        1. Откройте вкладку «Скрыть данные».  
        2. Перетащите или выберите картинку-контейнер.  
        3. Вставьте текст или выберите файл.  
        4. Выберите метод (см. выше), нажмите «🔐 Скрыть» → сохраните PNG.

        Готово! Ваша картинка выглядит так же, но внутри – ваш секрет.

        ──────────────────────────────────────────────────────────────
        🔍 Извлечение данных
        ───────────────────────────────────────────────────────────
        1. Перейдите во вкладку «Извлечь данные».  
        2. Укажите ту же картинку, которую получили на шаге 4.  
        3. Нажмите «🔍 Извлечь».  
        4. Сохраните или скопируйте результат.

        ──────────────────────────────────────────────────────────────
        🎨 Темы и внешний вид
        ──────────────────────────────────────────────────────────────
        • Тёмная – официальный стиль GitHub Dark.  
        • Светлая – глаз не устаёт при дневном свете.  
        • Космос / Океан / Лес / Неонка / Закат – для настроения.  
        Переключайтесь во вкладке «Настройки». Все изменения сохраняются автоматически.

        ──────────────────────────────────────────────────────────────
        📊 Как читать строку «Размер/Доступно/Требуется»
        ──────────────────────────────────────────────────────────────
        • Размер изображения – фактические пиксели.  
        • Доступно – сколько байт можно спрятать (зависит от метода).  
        • Требуется – сколько занимут ваши данные + заголовок.  
        Цвет подскажет:  
        🟢 <70 % – всё ок.  
        🟡 70-90 % – риск заметности.  
        🔴 >90 % – выберите больше картинку или другой метод.

        ──────────────────────────────────────────────────────────────
        🛠️ Подсказки продвинутого пользователя
        ──────────────────────────────────────────────────────────────
        • PNG → PNG – идеальный путь без потерь.  
        • JPG → PNG – можно, но избегайте повторного JPG-сжатия (данные удалятся).  
        • Масштабируйте картинку «вниз» после скрытия – данные останутся.  
        • История последних файлов – кликайте по строке, чтобы быстро загрузить.  
        • Кнопка «Отмена» прервёт длинную операцию без потерь.

        Автор: {AUTHOR}  

        Удачных тайных дел! 🕵️‍♂️
        """
        # Создаем отдельное окно для помощи
        help_window = tk.Toplevel(self.root)
        help_window.title("Помощь")
        help_window.geometry("600x500")
        help_window.resizable(True, True)
        # Центрируем окно
        help_window.transient(self.root)
        help_window.grab_set()
        # Текстовая область с прокруткой
        text_area = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=1
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, help_text)
        text_area.config(state=tk.DISABLED)
        # Кнопка закрытия
        close_btn = ttk.Button(help_window, text="Закрыть", command=help_window.destroy, style="TButton")
        close_btn.pack(pady=10)

    def run(self) -> None:
        # Восстановление размера окна
        if "window_size" in self.settings:
            self.root.geometry(self.settings["window_size"])
        # Установка типа данных
        if self.data_type.get() == "text":
            self.text_frame.pack(fill=tk.BOTH, expand=True)
            self.file_frame.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.file_frame.pack(fill=tk.X, pady=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self) -> None:
        self.save_settings()
        # Удаляем временный файл при закрытии
        if hasattr(self, 'temp_extracted_file') and self.temp_extracted_file and os.path.exists(
                self.temp_extracted_file.name):
            try:
                os.unlink(self.temp_extracted_file.name)
            except:
                pass
        self.root.destroy()


if __name__ == "__main__":
    app = SteganographyUltimate()
    if hasattr(app, 'root') and app.root.winfo_exists():
        app.run()
