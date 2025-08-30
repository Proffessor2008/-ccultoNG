import hashlib
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import zlib
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import List
from typing import Tuple

import numba
import numpy as np
from PIL import Image
from PIL import ImageTk
from scipy import ndimage
from tkinterdnd2 import DND_FILES, TkinterDnD

# ───────────────────────────────────────────────
# 🎨 ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ───────────────────────────────────────────────
VERSION = "0.4.2"
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
        "bg": "#0B1220",
        "fg": "#E6EDF6",
        "accent": "#4C8DFF",
        "accent_hover": "#6AA8FF",
        "accent_pressed": "#3B7CF2",
        "secondary": "#111827",
        "success": "#3FDA87",
        "error": "#FF6B6B",
        "warning": "#F0B23E",
        "card": "#0E1726",
        "border": "#253044",
        "text": "#E6EDF6",
        "text_secondary": "#94A3B8",
        "disabled": "#55637A",
        "scrollbar": "#243244",
        "highlight": "#1C273A",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1
    },
    "Светлая": {
        "name": "Светлая",
        "bg": "#F7F9FC",
        "fg": "#0F172A",
        "accent": "#2563EB",
        "accent_hover": "#3B82F6",
        "accent_pressed": "#1D4ED8",
        "secondary": "#FFFFFF",
        "success": "#16A34A",
        "error": "#DC2626",
        "warning": "#D97706",
        "card": "#FFFFFF",
        "border": "#E2E8F0",
        "text": "#0F172A",
        "text_secondary": "#64748B",
        "disabled": "#A3AEC2",
        "scrollbar": "#CBD5E1",
        "highlight": "#E8F1FF",
        "shadow": "#DDE3EC",
        "radius": 12,
        "padding": 12,
        "border_width": 1
    },
    "Космос": {
        "name": "Космос",
        "bg": "#0B1020",
        "fg": "#CDE7FF",
        "accent": "#7C3AED",
        "accent_hover": "#9D5CFF",
        "accent_pressed": "#6D28D9",
        "secondary": "#11162A",
        "success": "#22D3EE",
        "error": "#FB7185",
        "warning": "#FBBF24",
        "card": "#0F1530",
        "border": "#232B47",
        "text": "#D7EEFF",
        "text_secondary": "#8393B2",
        "disabled": "#3B4470",
        "scrollbar": "#1C2446",
        "highlight": "#1A2142",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1
    },
    "Океан": {
        "name": "Океан",
        "bg": "#021A2E",
        "fg": "#CDEBFF",
        "accent": "#0EA5E9",
        "accent_hover": "#38BDF8",
        "accent_pressed": "#0284C7",
        "secondary": "#03243F",
        "success": "#34D399",
        "error": "#F87171",
        "warning": "#F59E0B",
        "card": "#062B4A",
        "border": "#0B3B63",
        "text": "#CDEBFF",
        "text_secondary": "#8DB8D6",
        "disabled": "#2A5877",
        "scrollbar": "#0D3355",
        "highlight": "#0A2F54",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1
    },
    "Лес": {
        "name": "Лес",
        "bg": "#0D1A11",
        "fg": "#D6F5DE",
        "accent": "#22C55E",
        "accent_hover": "#4ADE80",
        "accent_pressed": "#16A34A",
        "secondary": "#102418",
        "success": "#84CC16",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "card": "#0F2616",
        "border": "#224A2F",
        "text": "#D8F7E0",
        "text_secondary": "#91C3A2",
        "disabled": "#416D54",
        "scrollbar": "#1B3A2A",
        "highlight": "#12301E",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1
    },
    "Ночная Неонка": {
        "name": "Ночная Неонка",
        "bg": "#0D0B21",
        "fg": "#F7F7FF",
        "accent": "#FF2EA8",
        "accent_hover": "#FF64C3",
        "accent_pressed": "#DB158E",
        "secondary": "#1B1841",
        "success": "#00E6A8",
        "error": "#FF5A7A",
        "warning": "#FFD166",
        "card": "#221E56",
        "border": "#3B3784",
        "text": "#F7F7FF",
        "text_secondary": "#C8C8F0",
        "disabled": "#6A67B2",
        "scrollbar": "#2B2770",
        "highlight": "#2A2671",
        "shadow": "#000000",
        "radius": 14,
        "padding": 14,
        "border_width": 1
    },
    "Солнечный Закат": {
        "name": "Солнечный Закат",
        "bg": "#FFF9F4",
        "fg": "#1F2937",
        "accent": "#FB6A63",
        "accent_hover": "#FF8B85",
        "accent_pressed": "#E1544E",
        "secondary": "#FFFFFF",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "card": "#FFFFFF",
        "border": "#EAD7CC",
        "text": "#1F2937",
        "text_secondary": "#6B7280",
        "disabled": "#B8BDC7",
        "scrollbar": "#E5D7CD",
        "highlight": "#FFEDE6",
        "shadow": "#EAD7CC",
        "radius": 12,
        "padding": 12,
        "border_width": 1
    }
}

SUPPORTED_FORMATS = [("Изображения", "*.png *.bmp *.tiff *.tga *.jpg *.jpeg")]
STEGANO_METHODS = {
    "lsb": "Классический LSB",
    "noise": "Adaptive-Noise",
    "aelsb": "Adaptive-Edge-LSB",
    "hill": "HILL-CA LSB Matching"}
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
        if size_bytes < 0:
            return "0 B"
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

    @staticmethod
    def open_in_file_manager(path: str) -> None:
        """Открывает файл или папку в системном проводнике."""
        try:
            if os.path.isfile(path):
                directory = os.path.dirname(path) or "."
            else:
                directory = path or "."
            if sys.platform.startswith('darwin'):
                subprocess.call(['open', directory])
            elif os.name == 'nt':
                os.startfile(directory)
            else:
                subprocess.call(['xdg-open', directory])
        except Exception as e:
            print(f"Не удалось открыть проводник: {e}")

    @staticmethod
    def open_in_default_app(path: str) -> None:
        """Открывает файл в приложении по умолчанию."""
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(['open', path])
            elif os.name == 'nt':
                os.startfile(path)
            else:
                subprocess.call(['xdg-open', path])
        except Exception as e:
            print(f"Не удалось открыть файл: {e}")


# ───────────────────────────────────────────────
# 🛈 КЛАСС ПОДСКАЗОК (TOOLTIP)
# ───────────────────────────────────────────────
class ToolTip:
    def __init__(self, widget, text, bg="#333333", fg="#ffffff", delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.bg = bg
        self.fg = fg
        self.tipwindow = None
        self._after_id = None
        self.widget.bind("<Enter>", self._schedule, add="+")
        self.widget.bind("<Leave>", self._unschedule, add="+")
        self.widget.bind("<Button-1>", self._unschedule, add="+")

    def _schedule(self, _event=None):
        self._after_id = self.widget.after(self.delay, self._show)

    def _unschedule(self, _event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        self._hide()

    def _show(self):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background=self.bg, foreground=self.fg,
                         relief=tk.SOLID, borderwidth=1, font=("Segoe UI", 9))
        label.pack(ipadx=8, ipy=4)
        tw.wm_geometry(f"+{x}+{y}")

    def _hide(self):
        tw = self.tipwindow
        if tw:
            tw.destroy()
            self.tipwindow = None


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
        radius = c.get("radius", 10)
        padding = c.get("padding", 10)
        border_width = c.get("border_width", 1)

        self.root.configure(bg=c["bg"])
        self.style.theme_use("clam")

        # Базовые установки
        self.style.configure(".", background=c["bg"], foreground=c["text"], font=("Segoe UI", 10))

        # Notebook (вкладки)
        self.style.configure("TNotebook", background=c["bg"], borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background=c["secondary"],
            foreground=c["text_secondary"],
            padding=(padding, padding - 2),
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", c["card"]), ("active", c["highlight"])],
            foreground=[("selected", c["text"]), ("active", c["text"])]
        )

        # Кнопки (обычные)
        self.style.configure(
            "TButton",
            background=c["secondary"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding, padding - 2),
            borderwidth=border_width,
            bordercolor=c["border"],
            focusthickness=2,
            focuscolor=c["accent"]
        )
        self.style.map(
            "TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent_pressed"])],
            foreground=[("disabled", c["disabled"]), ("pressed", "#ffffff")],
            bordercolor=[("focus", c["accent"])]
        )

        # Кнопки (акцентные)
        self.style.configure(
            "Accent.TButton",
            background=c["accent"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(padding + 2, padding - 1),
            borderwidth=0,
            relief="flat",
            focusthickness=3,
            focuscolor=c["accent_hover"]
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", c["accent_hover"]), ("pressed", c["accent_pressed"])],
            foreground=[("disabled", c["disabled"])]
        )

        # Кнопки-иконки (в шапке и рядом), чуть более «плоские»
        self.style.configure(
            "IconButton.TButton",
            background=c["secondary"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding - 3, padding - 5),
            borderwidth=border_width,
            bordercolor=c["border"]
        )
        self.style.map(
            "IconButton.TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent"])],
            foreground=[("pressed", "#ffffff")]
        )

        # Кнопки действий (извлечь/сохранить/копировать)
        self.style.configure(
            "Action.TButton",
            background=c["secondary"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding, padding - 2),
            borderwidth=border_width,
            bordercolor=c["border"],
            focusthickness=2,
            focuscolor=c["accent"]
        )
        self.style.map(
            "Action.TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent_pressed"])],
            foreground=[("pressed", "#ffffff")]
        )

        # Карточки
        self.style.configure("Card.TFrame", background=c["card"])
        self.style.configure(
            "Card.TLabelframe",
            background=c["card"],
            borderwidth=border_width,
            relief="solid",
            bordercolor=c["border"],
            lightcolor=c["card"],
            darkcolor=c["card"]
        )
        self.style.configure(
            "Card.TLabelframe.Label",
            background=c["card"],
            foreground=c["text"],
            font=("Segoe UI", 10, "bold"),
            padding=(4, 0)
        )

        # Метки
        self.style.configure("TLabel", background=c["bg"], foreground=c["text"], font=("Segoe UI", 10))
        self.style.configure("Secondary.TLabel", background=c["bg"], foreground=c["text_secondary"],
                             font=("Segoe UI", 9))

        # Заголовки блоков
        self.style.configure("GroupHeader.TLabel",
                             background=c["bg"], foreground=c["accent"], font=("Segoe UI", 12, "bold"))

        # Поля ввода
        self.style.configure(
            "TEntry",
            fieldbackground=c["card"],
            foreground=c["text"],
            insertcolor=c["text"],
            bordercolor=c["border"],
            lightcolor=c["card"],
            darkcolor=c["card"],
            relief="flat",
            borderwidth=border_width,
            padding=(padding - 4, padding - 6)
        )
        self.style.map(
            "TEntry",
            bordercolor=[("focus", c["accent"])],
            lightcolor=[("focus", c["card"])],
            darkcolor=[("focus", c["card"])]
        )

        # Выпадающие списки
        self.style.configure(
            "TCombobox",
            fieldbackground=c["card"],
            foreground=c["text"],
            selectbackground=c["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=border_width,
            padding=(padding - 6, padding - 6),
            arrowsize=13,
            bordercolor=c["border"]
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", c["card"])],
            bordercolor=[("focus", c["accent"])]
        )

        # Текстовые поля (ScrolledText)
        self.style.configure("TText",
                             background=c["card"],
                             foreground=c["text"],
                             insertbackground=c["text"],
                             selectbackground=c["accent"],
                             selectforeground="#ffffff",
                             relief="flat",
                             borderwidth=border_width)

        # Прогресс-бар
        self.style.configure(
            "TProgressbar",
            background=c["accent"],
            troughcolor=c["secondary"],
            bordercolor=c["border"],
            lightcolor=c["accent"],
            darkcolor=c["accent"],
            thickness=14
        )

        # Доп. стили прогресс-бара для индикатора заполнения
        self.style.configure(
            "UsageGreen.Horizontal.TProgressbar",
            background=c["success"],
            troughcolor=c["secondary"],
            thickness=12
        )
        self.style.configure(
            "UsageYellow.Horizontal.TProgressbar",
            background=c["warning"],
            troughcolor=c["secondary"],
            thickness=12
        )
        self.style.configure(
            "UsageRed.Horizontal.TProgressbar",
            background=c["error"],
            troughcolor=c["secondary"],
            thickness=12
        )

        # Скроллбар
        self.style.configure(
            "TScrollbar",
            background=c["scrollbar"],
            troughcolor=c["secondary"],
            bordercolor=c["border"],
            arrowcolor=c["text_secondary"]
        )
        self.style.map(
            "TScrollbar",
            background=[("active", c["highlight"])]
        )

        # История
        self.style.configure(
            "History.TLabel",
            background=c["card"],
            foreground=c["text_secondary"],
            font=("Segoe UI", 9),
            padding=(padding, padding // 2)
        )
        self.style.map(
            "History.TLabel",
            background=[("active", c["highlight"])],
            foreground=[("active", c["accent"])]
        )

        # Предпросмотр
        self.style.configure(
            "Preview.TFrame",
            background=c["card"],
            relief="solid",
            borderwidth=border_width,
            bordercolor=c["border"]
        )

        # Тексты статуса/ошибок/успеха/варнингов
        self.style.configure("Error.TLabel", background=c["bg"], foreground=c["error"], font=("Segoe UI", 10))
        self.style.configure("Success.TLabel", background=c["bg"], foreground=c["success"], font=("Segoe UI", 10))
        self.style.configure("Warning.TLabel", background=c["bg"], foreground=c["warning"], font=("Segoe UI", 10))

        # Дроп-зона — теперь отдельным стилем метки
        self.style.configure(
            "DropLabel.TLabel",
            background=c["card"],
            foreground=c["text_secondary"],
            font=("Segoe UI", 11, "bold"),
            padding=(padding * 2, padding * 2),
            borderwidth=0
        )
        self.style.configure(
            "DropLabelActive.TLabel",
            background=c["highlight"],
            foreground=c["text"],
            font=("Segoe UI", 11, "bold"),
            padding=(padding * 2, padding * 2),
            borderwidth=0
        )

        # Статусная панель
        self.style.configure("StatusBar.TFrame", background=c["secondary"])

        # Тосты
        self.style.configure("Toast.TLabel",
                             background="#333333", foreground="#ffffff", font=("Segoe UI", 10), relief="solid",
                             borderwidth=1)

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


MAGIC_BYTES = b'ONG'  # OccultoNG
HEADER_MAGIC_LEN = len(MAGIC_BYTES)
HEADER_CHECKSUM_LEN = 4  # CRC32
HEADER_DATALEN_LEN = 4  # Длина данных
HEADER_FULL_LEN = HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN + HEADER_DATALEN_LEN


# Функция-помощник для генерации RNG
def _generate_rng(password: str, method: str) -> np.random.Generator:
    """Генерирует отдельный rng для каждого метода."""
    seed_str = f"{password}{method}".encode()
    key = hashlib.sha256(seed_str).digest()
    return np.random.default_rng(np.frombuffer(key, dtype=np.uint64))


# ───────────────────────────────────────────────
# 🧠 КЛАСС ПРОДВИНУТЫХ СТЕГО-МЕТОДОВ
# ───────────────────────────────────────────────
class AdvancedStego:

    # ---------- Вспомогательные методы для работы с данными и заголовками ----------
    @staticmethod
    def _pack_data_with_header(data: bytes) -> bytes:
        checksum = zlib.crc32(data).to_bytes(HEADER_CHECKSUM_LEN, 'big')
        data_len = len(data).to_bytes(HEADER_DATALEN_LEN, 'big')
        return MAGIC_BYTES + checksum + data_len + data

    @staticmethod
    def _unpack_data_with_header(full_bytes: bytes) -> bytes:
        if len(full_bytes) < HEADER_FULL_LEN:
            raise ValueError("Недостаточно данных для заголовка.")
        magic = full_bytes[:HEADER_MAGIC_LEN]
        if magic != MAGIC_BYTES:
            raise ValueError("Неверные магические байты. Данные не найдены или повреждены.")
        header_end = HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN + HEADER_DATALEN_LEN
        stored_checksum = int.from_bytes(full_bytes[HEADER_MAGIC_LEN:HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN], 'big')
        data_len = int.from_bytes(full_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:header_end], 'big')
        data_start, data_end = header_end, header_end + data_len
        if len(full_bytes) < data_end:
            raise ValueError("Данные обрезаны, фактическая длина меньше заявленной в заголовке.")
        data = full_bytes[data_start:data_end]
        calculated_checksum = zlib.crc32(data)
        if calculated_checksum != stored_checksum:
            raise ValueError("Ошибка контрольной суммы. Данные повреждены.")
        return data

    @staticmethod
    def _embed_with_parity(pixel_value: int, bit_to_embed: int) -> int:
        if (pixel_value % 2) != bit_to_embed:
            return pixel_value - 1 if pixel_value % 2 != 0 and pixel_value > 0 else pixel_value + 1
        return pixel_value

    @staticmethod
    @numba.jit(nopython=True)
    def _embed_bits_numba(pixels_flat, indices, bits):
        """
        Компилируемая Numba-функция для быстрой вставки битов.
        Заменяет медленный Python-цикл.
        """
        for i in range(len(indices)):
            idx = indices[i]
            bit_to_embed = bits[i]
            pixel_val = pixels_flat[idx]

            # Логика _embed_with_parity
            if (pixel_val % 2) != bit_to_embed:
                if pixel_val > 0 and (pixel_val % 2) != 0:
                    pixels_flat[idx] -= 1
                elif pixel_val < 255:
                    pixels_flat[idx] += 1
                else:  # Если pixel_val == 255
                    pixels_flat[idx] -= 1
        return pixels_flat

    # Numba-функция для AELSB
    @staticmethod
    @numba.jit(nopython=True)
    def _embed_bits_aelsb_numba(pixels_flat_rgb, pixel_indices, channel_indices, data_bits):
        """
        Компилируемая Numba-функция для быстрой вставки битов в AELSB.
        """
        for i in range(len(pixel_indices)):
            pixel_idx = pixel_indices[i]
            channel = channel_indices[i]
            bit = data_bits[i]

            pixel_val = pixels_flat_rgb[pixel_idx, channel]

            if (pixel_val % 2) != bit:
                if pixel_val > 0 and (pixel_val % 2) != 0:
                    pixels_flat_rgb[pixel_idx, channel] -= 1
                elif pixel_val < 255:
                    pixels_flat_rgb[pixel_idx, channel] += 1
                else:
                    pixels_flat_rgb[pixel_idx, channel] -= 1

    # ---------- LSB (Максимальная вместимость) ----------
    @staticmethod
    def hide_lsb(container_path: str, data: bytes, password: str, output_path: str,
                 progress_callback=None, cancel_event=None):
        try:
            with Image.open(container_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                height, width, _ = pixels.shape
                full_data = AdvancedStego._pack_data_with_header(data)
                total_bits_needed = len(full_data) * 8
                available_bits = height * width * 3
                if total_bits_needed > available_bits:
                    raise ValueError(f"Данные слишком велики для изображения. Максимум: {available_bits // 8} байт")
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8))
                pixels_flat = pixels.reshape(-1)
                pixels_flat[:total_bits_needed] = (pixels_flat[:total_bits_needed] & 0xFE) | data_bits

                for i in range(0, total_bits_needed, 1000):
                    if progress_callback:
                        progress_callback((i / total_bits_needed) * 100)
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Операция отменена пользователем")

                result_img = Image.fromarray(pixels)
                result_img.save(output_path, format='PNG', optimize=True)
                if progress_callback: progress_callback(100.0)
        except Exception as e:
            raise e

    @staticmethod
    def extract_lsb(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img)
                pixels_flat = pixels.reshape(-1)
                header_bits_needed = HEADER_FULL_LEN * 8
                if pixels_flat.size < header_bits_needed:
                    raise ValueError("Недостаточно данных для заголовка.")

                header_bits = (pixels_flat[:header_bits_needed] & 1)
                header_bytes = np.packbits(header_bits).tobytes()

                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big')
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных в заголовке.")

                total_bits_to_extract = (HEADER_FULL_LEN + data_len) * 8
                if pixels_flat.size < total_bits_to_extract:
                    raise ValueError("Недостаточно данных для извлечения полного сообщения.")

                all_bits = (pixels_flat[:total_bits_to_extract] & 1)
                full_bytes = np.packbits(all_bits).tobytes()

                if progress_callback: progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e

    # ---------- Adaptive-Noise ----------
    @staticmethod
    def hide_noise(container_path: str, data: bytes, password: str, output_path: str,
                   progress_callback=None, cancel_event=None):
        try:
            rng = _generate_rng(password, "noise")
            with Image.open(container_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                full_data = AdvancedStego._pack_data_with_header(data)
                total_bits_needed = len(full_data) * 8
                if total_bits_needed > pixels.size:
                    raise ValueError("Данные слишком велики для этого изображения.")
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8))

                indices = np.arange(pixels.size)
                rng.shuffle(indices)
                selected_indices = indices[:total_bits_needed]

                pixels_flat = pixels.reshape(-1)

                # *** ОПТИМИЗАЦИЯ: Вызов Numba-функции вместо цикла ***
                AdvancedStego._embed_bits_numba(pixels_flat, selected_indices, data_bits)

                # Обновление прогресса можно оставить, т.к. основная работа сделана
                if progress_callback: progress_callback(100.0)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                result_img = Image.fromarray(pixels)
                # Для скорости можно использовать compress_level=1
                result_img.save(output_path, format='PNG', compress_level=1)
        except Exception as e:
            raise e

    @staticmethod
    def extract_noise(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            rng = _generate_rng(password, "noise")
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img)
                indices = np.arange(pixels.size)
                rng.shuffle(indices)
                pixels_flat = pixels.reshape(-1)

                header_bits_needed = HEADER_FULL_LEN * 8
                header_indices = indices[:header_bits_needed]

                # *** ОПТИМИЗАЦИЯ: Векторизованное извлечение ***
                header_bits = (pixels_flat[header_indices] & 1)
                header_bytes = np.packbits(header_bits).tobytes()

                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big')
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных.")

                total_bits_needed = (HEADER_FULL_LEN + data_len) * 8
                all_indices = indices[:total_bits_needed]

                # *** ОПТИМИЗАЦИЯ: Векторизованное извлечение ***
                extracted_bits = (pixels_flat[all_indices] & 1)

                full_bytes = np.packbits(extracted_bits).tobytes()
                if progress_callback: progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e

    # ---------- AELSB++ (Content-Adaptive + Hamming(7,3) + LSB matching) ----------
    @staticmethod
    def _hill_cost_map(img: Image.Image) -> np.ndarray:
        """
        HILL-подобная карта 'стоимости' изменений.
        Чем меньше cost, тем лучше место для скрытия.
        Строим на 'санированном' изображении (LSB обнулены) для детерминизма.
        """
        # Санируем LSB, чтобы и при скрытии, и при извлечении
        # карта стоимости была абсолютно одинаковой.
        rgb = np.array(img, dtype=np.uint8)
        # Отбрасываем LSB с помощью побитового AND с 0xFE (...11111110)
        sanitized = (rgb & 0xFE).astype(np.uint8)
        gray = Image.fromarray(sanitized).convert('L')
        g = np.array(gray, dtype=np.float32)

        # Высокочастотный фильтр (по мотивам HILL)
        hp = np.array([[-1, 2, -1],
                       [2, -4, 2],
                       [-1, 2, -1]], dtype=np.float32)

        res = ndimage.convolve(g, hp, mode='reflect')
        mag = np.abs(res)

        # Небольшое сглаживание, чтобы получить устойчивую карту
        smooth = ndimage.uniform_filter(mag, size=5, mode='reflect')
        # Чем выше текстурность, тем меньше стоимость (и наоборот)
        cost = 1.0 / (smooth + 1.0)
        return cost  # нормализация не обязательна, важен относительный порядок

    @staticmethod
    def _prepare_calsb_indices(pixels: np.ndarray, base_cost: np.ndarray,
                               rng: np.random.Generator, needed_elements: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Новая версия: порядок зависит только от RNG.
        Это гарантирует идентичный порядок на скрытии и извлечении.
        """
        # Берём только первые 3 канала на всякий случай
        if pixels.ndim != 3 or pixels.shape[2] < 3:
            raise ValueError("Ожидается изображение RGB.")
        h, w, _ = pixels.shape
        total = h * w * 3
        if needed_elements > total:
            raise ValueError("Недостаточно позиций для встраивания.")

        indices = np.arange(total, dtype=np.int64)
        rng.shuffle(indices)
        chosen = indices[:needed_elements]
        pixel_idx = (chosen // 3).astype(np.int64)
        channel_idx = (chosen % 3).astype(np.int64)
        return pixel_idx, channel_idx

    @staticmethod
    @numba.jit(nopython=True)
    def _embed_hamming73_numba(pixels_flat_rgb, pixel_indices, channel_indices, bits, groups):
        bits_len = bits.shape[0]
        for g in range(groups):
            base = g * 7

            v0 = pixels_flat_rgb[pixel_indices[base + 0], channel_indices[base + 0]] & 1
            v1 = pixels_flat_rgb[pixel_indices[base + 1], channel_indices[base + 1]] & 1
            v2 = pixels_flat_rgb[pixel_indices[base + 2], channel_indices[base + 2]] & 1
            v3 = pixels_flat_rgb[pixel_indices[base + 3], channel_indices[base + 3]] & 1
            v4 = pixels_flat_rgb[pixel_indices[base + 4], channel_indices[base + 4]] & 1
            v5 = pixels_flat_rgb[pixel_indices[base + 5], channel_indices[base + 5]] & 1
            v6 = pixels_flat_rgb[pixel_indices[base + 6], channel_indices[base + 6]] & 1

            s0 = (v0 + v2 + v4 + v6) & 1
            s1 = (v1 + v2 + v5 + v6) & 1
            s2 = (v3 + v4 + v5 + v6) & 1

            b0_idx = g * 3
            m0 = bits[b0_idx] if b0_idx < bits_len else 0
            b1_idx = b0_idx + 1
            m1 = bits[b1_idx] if b1_idx < bits_len else 0
            b2_idx = b1_idx + 1
            m2 = bits[b2_idx] if b2_idx < bits_len else 0

            ds0 = s0 ^ m0
            ds1 = s1 ^ m1
            ds2 = s2 ^ m2
            syn = ds0 + (ds1 << 1) + (ds2 << 2)  # 0..7

            if syn != 0:
                j = syn - 1
                idx_p = pixel_indices[base + j]
                idx_c = channel_indices[base + j]

                val = pixels_flat_rgb[idx_p, idx_c]

                if val == 0:
                    pixels_flat_rgb[idx_p, idx_c] = 1
                elif val == 255:
                    pixels_flat_rgb[idx_p, idx_c] = 254
                else:
                    if val % 2 == 1:
                        pixels_flat_rgb[idx_p, idx_c] = val - 1
                    else:
                        pixels_flat_rgb[idx_p, idx_c] = val + 1

    @staticmethod
    @numba.jit(nopython=True)
    def _extract_hamming73_numba(pixels_flat_rgb, pixel_indices, channel_indices, groups, bits_len):
        """
        Декодирование Hamming(7,3): возвращает массив битов длиной bits_len.
        """
        out = np.zeros(bits_len, dtype=np.uint8)
        for g in range(groups):
            base = g * 7
            v0 = pixels_flat_rgb[pixel_indices[base + 0], channel_indices[base + 0]] & 1
            v1 = pixels_flat_rgb[pixel_indices[base + 1], channel_indices[base + 1]] & 1
            v2 = pixels_flat_rgb[pixel_indices[base + 2], channel_indices[base + 2]] & 1
            v3 = pixels_flat_rgb[pixel_indices[base + 3], channel_indices[base + 3]] & 1
            v4 = pixels_flat_rgb[pixel_indices[base + 4], channel_indices[base + 4]] & 1
            v5 = pixels_flat_rgb[pixel_indices[base + 5], channel_indices[base + 5]] & 1
            v6 = pixels_flat_rgb[pixel_indices[base + 6], channel_indices[base + 6]] & 1

            s0 = (v0 + v2 + v4 + v6) & 1
            s1 = (v1 + v2 + v5 + v6) & 1
            s2 = (v3 + v4 + v5 + v6) & 1

            pos = g * 3
            if pos < bits_len:
                out[pos] = s0
            if pos + 1 < bits_len:
                out[pos + 1] = s1
            if pos + 2 < bits_len:
                out[pos + 2] = s2
        return out

    @staticmethod
    def hide_aelsb(container_path: str, data: bytes, password: str, output_path: str,
                   progress_callback=None, cancel_event=None):
        try:
            rng_order = _generate_rng(password or "", "aelsbpp_order")

            with Image.open(container_path) as img:
                # Всегда RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)

                full_data = AdvancedStego._pack_data_with_header(data)
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8)).astype(np.uint8)

                r, n = 3, 7
                groups = (len(data_bits) + r - 1) // r
                needed_elements = groups * n

                # Новый детерминированный порядок
                pix_idx, ch_idx = AdvancedStego._prepare_calsb_indices(pixels, None, rng_order, needed_elements)

                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                # Явно работаем с RGB
                flat_rgb = pixels.reshape(-1, 3)
                AdvancedStego._embed_hamming73_numba(flat_rgb, pix_idx, ch_idx, data_bits, groups)

                if progress_callback:
                    progress_callback(100.0)

                result_img = Image.fromarray(pixels)
                result_img.save(output_path, format='PNG', optimize=True)

        except Exception as e:
            raise e

    @staticmethod
    def extract_aelsb(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            rng_order = _generate_rng(password or "", "aelsbpp_order")
            with Image.open(image_path) as img:
                # Всегда RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                flat_rgb = pixels.reshape(-1, 3)

                header_bits_needed = HEADER_FULL_LEN * 8
                r, n = 3, 7
                header_groups = (header_bits_needed + r - 1) // r
                header_elements = header_groups * n

                # Индексы для заголовка
                pix_idx_hdr, ch_idx_hdr = AdvancedStego._prepare_calsb_indices(pixels, None, rng_order, header_elements)

                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                header_bits = AdvancedStego._extract_hamming73_numba(flat_rgb, pix_idx_hdr, ch_idx_hdr,
                                                                     header_groups, header_bits_needed)
                header_bytes = np.packbits(header_bits).tobytes()

                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big')
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных.")

                total_bits_needed = (HEADER_FULL_LEN + data_len) * 8
                total_groups = (total_bits_needed + r - 1) // r
                total_elements = total_groups * n

                # Для полного сообщения заново пересоздаём RNG,
                # чтобы порядок был тем же (префикс совпадёт с заголовком)
                rng_order = _generate_rng(password or "", "aelsbpp_order")
                pix_idx_all, ch_idx_all = AdvancedStego._prepare_calsb_indices(pixels, None, rng_order, total_elements)

                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                bits = AdvancedStego._extract_hamming73_numba(flat_rgb, pix_idx_all, ch_idx_all,
                                                              total_groups, total_bits_needed)
                full_bytes = np.packbits(bits).tobytes()

                if progress_callback:
                    progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e

    @staticmethod
    def _rank_indices_by_hill(img: Image.Image,
                              rng: np.random.Generator,
                              needed_elements: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Дает. порядок позиций по HILL: квантуем cost в int и используем целочисленный tie-break.
        Гарантирует идентичный порядок на скрытии/извлечении.
        """
        img_rgb = img.convert('RGB')  # строго RGB
        pixels = np.array(img_rgb, dtype=np.uint8)
        h, w, _ = pixels.shape
        total = h * w * 3
        if needed_elements > total:
            raise ValueError("Недостаточно места для встраивания (HILL).")

        # HILL-карта на санированной картинке (LSB=0)
        cost_map = AdvancedStego._hill_cost_map(img_rgb)  # (h, w) float32
        # Квантуем, чтобы исключить микроскопические float-расхождения
        cost_q = np.round(cost_map * 1e7).astype(np.int64)  # (h, w) int64

        # Повтор на каналы
        cost_flat = np.repeat(cost_q.reshape(-1), 3)  # (h*w*3,) int64

        # Целочисленный тай-брейк от RNG — строго детерминирован
        tie = rng.integers(0, np.iinfo(np.int64).max, size=cost_flat.size, dtype=np.int64)

        # np.lexsort: последний ключ — первичный
        order = np.lexsort((tie, cost_flat))  # сначала cost, потом tie

        chosen = order[:needed_elements]
        pixel_idx = (chosen // 3).astype(np.int64)
        channel_idx = (chosen % 3).astype(np.int64)
        return pixel_idx, channel_idx

    @staticmethod
    def hide_hill(container_path: str, data: bytes, password: str, output_path: str,
                  progress_callback=None, cancel_event=None):
        """
        HILL-CA LSB Matching + Hamming(7,3)
        """
        try:
            rng_order = _generate_rng(password or "", "hill_order")

            with Image.open(container_path) as img:
                img_rgb = img.convert('RGB')
                pixels = np.array(img_rgb, dtype=np.uint8)

                full_data = AdvancedStego._pack_data_with_header(data)
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8)).astype(np.uint8)

                r, n = 3, 7
                groups = (len(data_bits) + r - 1) // r
                needed_elements = groups * n

                # Индексы по HILL
                pix_idx, ch_idx = AdvancedStego._rank_indices_by_hill(img_rgb, rng_order, needed_elements)

                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                flat_rgb = pixels.reshape(-1, 3)
                AdvancedStego._embed_hamming73_numba(flat_rgb, pix_idx, ch_idx, data_bits, groups)

                if progress_callback:
                    progress_callback(100.0)

                result_img = Image.fromarray(pixels)
                result_img.save(output_path, format='PNG', optimize=True)
        except Exception as e:
            raise e

    @staticmethod
    def extract_hill(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        """
        Извлечение: тот же порядок по HILL.
        """
        try:
            rng_order = _generate_rng(password or "", "hill_order")

            with Image.open(image_path) as img:
                img_rgb = img.convert('RGB')
                pixels = np.array(img_rgb, dtype=np.uint8)
                flat_rgb = pixels.reshape(-1, 3)

                header_bits_needed = HEADER_FULL_LEN * 8
                r, n = 3, 7
                header_groups = (header_bits_needed + r - 1) // r
                header_elements = header_groups * n

                # Индексы для заголовка
                pix_idx_hdr, ch_idx_hdr = AdvancedStego._rank_indices_by_hill(img_rgb, rng_order, header_elements)

                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                header_bits = AdvancedStego._extract_hamming73_numba(
                    flat_rgb, pix_idx_hdr, ch_idx_hdr, header_groups, header_bits_needed
                )
                header_bytes = np.packbits(header_bits).tobytes()

                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")

                data_len = int.from_bytes(
                    header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big'
                )
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных.")

                total_bits_needed = (HEADER_FULL_LEN + data_len) * 8
                total_groups = (total_bits_needed + r - 1) // r
                total_elements = total_groups * n

                # Переинициализируем RNG — порядок должен совпасть полностью
                rng_order = _generate_rng(password or "", "hill_order")
                pix_idx_all, ch_idx_all = AdvancedStego._rank_indices_by_hill(img_rgb, rng_order, total_elements)

                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                bits = AdvancedStego._extract_hamming73_numba(
                    flat_rgb, pix_idx_all, ch_idx_all, total_groups, total_bits_needed
                )
                full_bytes = np.packbits(bits).tobytes()

                if progress_callback:
                    progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e


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
                return w, h, w * h * 3  # 3 канала RGB
        except Exception as e:
            raise ValueError(f"Ошибка загрузки изображения: {str(e)}")

    @staticmethod
    def create_thumbnail(path: str, max_size: Tuple[int, int] = (200, 200)) -> ImageTk.PhotoImage:
        """Создает миниатюру изображения для предпросмотра"""
        try:
            with Image.open(path) as img:
                img.thumbnail(max_size, Image.Resampling.BOX)
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                return ImageTk.PhotoImage(img)
        except Exception as e:
            raise ValueError(f"Ошибка создания миниатюры: {str(e)}")

    @staticmethod
    def get_capacity_by_method(total_pixels: int, method: str) -> int:
        """
        Рассчитывает теоретическую вместимость ПОЛЕЗНЫХ ДАННЫХ в битах для заданного метода.
        Уже учитывает и вычитает размер заголовка.
        """
        total_lsb_bits = total_pixels * 3  # RGB

        if method in ("lsb", "noise"):
            capacity_bits = total_lsb_bits
        elif method in ("aelsb", "hill"):
            capacity_bits = int(total_lsb_bits * (3 / 7))
        else:
            return 0

        data_capacity_bits = max(0, capacity_bits - (HEADER_FULL_LEN * 8))
        return data_capacity_bits

    # ── 1. НЕВИДИМОЕ СКРЫТИЕ ──
    @staticmethod
    def hide_data(container_path: str, data: bytes, password: str, output_path: str,
                  method: str = "aelsb", compression_level: int = 9,
                  progress_callback=None, cancel_event=None) -> None:
        """Универсальный метод скрытия данных"""
        try:
            if method == "lsb":
                AdvancedStego.hide_lsb(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            elif method == "noise":
                AdvancedStego.hide_noise(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            elif method == "aelsb":
                AdvancedStego.hide_aelsb(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            elif method == "hill":
                AdvancedStego.hide_hill(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            else:
                raise ValueError(f"Неизвестный метод скрытия: {method}")
        except Exception as e:
            raise e

    @staticmethod
    def extract_data(image_path: str, password: str, method: str = None,
                     progress_callback=None, cancel_event=None) -> bytes:
        """Универсальный метод извлечения данных с автоматическим определением метода."""

        if method:
            methods_to_try = [method]
        else:
            methods_to_try = ["lsb", "noise", "aelsb", "hill"]

        last_error = None

        for method_name in methods_to_try:
            try:
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                if progress_callback:
                    progress_callback(0, f"Проверка метода: {STEGANO_METHODS.get(method_name, method_name)}...")

                if method_name == "lsb":
                    extractor = AdvancedStego.extract_lsb
                elif method_name == "noise":
                    extractor = AdvancedStego.extract_noise
                elif method_name == "aelsb":
                    extractor = AdvancedStego.extract_aelsb
                elif method_name == "hill":
                    extractor = AdvancedStego.extract_hill
                else:
                    continue

                def internal_progress(p):
                    if progress_callback:
                        base_progress = methods_to_try.index(method_name) * (100 / len(methods_to_try))
                        scaled_progress = p / len(methods_to_try)
                        progress_callback(base_progress + scaled_progress)

                data = extractor(image_path, password, internal_progress, cancel_event)

                if progress_callback:
                    progress_callback(100.0,
                                      f"✅ Данные успешно найдены методом: {STEGANO_METHODS.get(method_name, method_name)}!")
                return data

            except (ValueError, IndexError, InterruptedError) as e:
                last_error = e
                continue

        if isinstance(last_error, InterruptedError):
            raise last_error
        if last_error:
            raise ValueError(
                f"❌ Не удалось извлечь данные. Возможно, изображение не содержит скрытой информации или данные повреждены.\n\nПоследняя ошибка: {last_error}")
        else:
            raise ValueError("❌ Не удалось извлечь данные. Ни один из поддерживаемых методов не подошел.")


# ───────────────────────────────────────────────
# 🔐 КЛАСС ДЛЯ ПРОВЕРКИ ПАРОЛЯ
# ───────────────────────────────────────────────
class PasswordDialog:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.password_correct = False
        self.dialog = tk.Toplevel(root)
        self.dialog.title("Введите пароль")
        self.dialog.geometry("350x300")
        self.dialog.resizable(False, False)
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)

        self.dialog.withdraw()
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - self.dialog.winfo_reqwidth()) // 2
        y = (self.dialog.winfo_screenheight() - self.dialog.winfo_reqheight()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        self.dialog.deiconify()

        self.theme_manager = ThemeManager(self.dialog)
        self.theme_manager.set_theme("Тёмная")
        self.colors = self.theme_manager.colors

        title_label = ttk.Label(self.dialog, text="🔐 Доступ к ØccultoNG", font=("Segoe UI", 14, "bold"),
                                style="GroupHeader.TLabel")
        title_label.pack(pady=(20, 10))

        subtitle_label = ttk.Label(self.dialog, text="🔒 Введите пароль для продолжения работы",
                                   style="Secondary.TLabel")
        subtitle_label.pack(pady=(0, 15))

        self.password_var = tk.StringVar()
        self.entry = ttk.Entry(self.dialog, textvariable=self.password_var, show="*", width=30, font=("Segoe UI", 11))
        self.entry.pack(pady=5, padx=20, fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.check_password())

        self.error_label = ttk.Label(self.dialog, text="", style="Error.TLabel")
        self.error_label.pack()

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="🔓 Войти", command=self.check_password, style="Accent.TButton").pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(btn_frame, text="🚪 Выход", command=self._on_close, style="TButton").pack(side=tk.LEFT, padx=5)

        self.entry.focus_set()

        self.dialog.transient(root)
        self.dialog.grab_set()
        root.wait_window(self.dialog)

    def check_password(self) -> None:
        entered = self.password_var.get()
        if not entered:
            self.error_label.config(text="⚠️ Пароль не может быть пустым")
            return
        hash_obj = hashlib.sha256(entered.encode('utf-8'))
        if hash_obj.hexdigest() == PASSWORD_HASH:
            self.password_correct = True
            self.dialog.destroy()
        else:
            self.error_label.config(text="❌ Неверный пароль. Попробуйте снова.")

    def _on_close(self) -> None:
        self.password_correct = False
        self.dialog.destroy()


# ───────────────────────────────────────────────
# 🧠 ОСНОВНОЕ ПРИЛОЖЕНИЕ
# ───────────────────────────────────────────────
class SteganographyUltimate:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title(f"ØccultoNG v{VERSION}")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)

        password_dialog = PasswordDialog(self.root)
        if not password_dialog.password_correct:
            self.root.destroy()
            return

        try:
            self.root.iconbitmap(default=self.resource_path("icon.ico"))
        except:
            pass

        self.theme_manager = ThemeManager(self.root)

        self.settings = self.load_settings()
        self.history = self.load_history()

        self.theme_manager.set_theme(self.settings.get("theme", "Тёмная"))
        self.colors = self.theme_manager.colors

        # Переменные
        self.img_path = tk.StringVar()
        self.last_progress_update_time = 0
        self.extract_img_path = tk.StringVar()
        self.data_type = tk.StringVar(value=self.settings.get("data_type", "text"))
        self.method_var = tk.StringVar(value=self.settings.get("method", "lsb"))
        self.compression_level = tk.IntVar(value=self.settings.get("compression_level", 9))
        self.current_extracted = None
        self.is_dragging = False
        self.last_update_time = 0
        self.file_path_var = tk.StringVar()
        self.last_open_dir = self.settings.get("last_open_dir", os.path.expanduser("~"))
        self.last_save_dir = self.settings.get("last_save_dir", os.path.expanduser("~"))

        # Элементы интерфейса
        self.preview_img = None
        self.extract_preview = None
        self.text_input = None
        self.result_text = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.history_labels = []
        self.size_info_frame = None
        self.required_size_label = None
        self.capacity_labels = {}
        self.usage_var = tk.DoubleVar(value=0.0)
        self.usage_bar = None
        self.usage_label = None

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
        self._preview_photo = None
        self._extract_photo = None

        # Доп. элементы UX
        self.file_info_label = None
        self.file_entry_widget = None
        self.extract_drop_label = None
        self.text_menu = None
        self.result_menu = None
        self.history_menu = None
        self.open_file_button = None
        self.copy_hash_button = None
        self.last_extracted_hash = None

        self.setup_ui()
        self.bind_drag_drop()  # dnd для вкладки "Скрыть"
        self.bind_drag_drop_extract()  # dnd для вкладки "Извлечь"
        self.bind_file_drop()  # dnd для выбора файла на вкладке "Скрыть"
        self.refresh_history()
        self.bind_shortcuts()
        self.install_context_menus()
        self.install_tooltips()

        # Глобальный перехватчик ошибок (не мешает логике)
        def excepthook(exc_type, exc_value, exc_tb):
            import traceback
            traceback.print_exception(exc_type, exc_value, exc_tb)
            try:
                messagebox.showerror("Неожиданная ошибка", f"{exc_type.__name__}: {exc_value}")
            except:
                pass

        sys.excepthook = excepthook

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
            "window_size": "1000x800",
            "last_open_dir": os.path.expanduser("~"),
            "last_save_dir": os.path.expanduser("~")
        }

    def save_settings(self) -> None:
        settings = {
            "theme": self.theme_manager.current_theme,
            "method": self.method_var.get(),
            "data_type": self.data_type.get(),
            "compression_level": self.compression_level.get(),
            "window_size": self.root.geometry(),
            "last_open_dir": self.last_open_dir,
            "last_save_dir": self.last_save_dir
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
                    valid_history = [h for h in history if os.path.exists(h)]
                    if len(valid_history) != len(history):
                        self.save_history(valid_history)
                    return valid_history[:MAX_HISTORY]
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
        return []

    def save_history(self, history: list) -> None:
        try:
            with open(CONFIG["HISTORY_FILE"], 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def save_to_history(self, path: str) -> None:
        if not path:
            return
        hist = [path] + [h for h in self.history if h != path and os.path.exists(h)]
        self.history = hist[:MAX_HISTORY]
        self.save_history(self.history)
        self.refresh_history()

    def setup_ui(self) -> None:
        main_frame = ttk.Frame(self.root, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(main_frame)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.create_status_bar(main_frame)

        self.create_hide_tab()
        self.create_extract_tab()
        self.create_settings_tab()

        self.create_toast()

    def create_header(self, parent: ttk.Frame) -> None:
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_frame = ttk.Frame(header_frame, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

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

        menu_frame = ttk.Frame(header_frame, style="Card.TFrame")
        menu_frame.pack(side=tk.RIGHT)

        help_btn = ttk.Button(
            menu_frame,
            text="❓ Помощь",
            command=self.show_help,
            style="IconButton.TButton"
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(help_btn, "Открыть справку (F1)")

    def create_hide_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=15)
        self.notebook.add(frame, text="📦 Скрыть данные")

        container = ttk.LabelFrame(
            frame,
            text="🖼️ Изображение-контейнер",
            padding=15,
            style="Card.TLabelframe"
        )

        path_frame = ttk.Frame(container, style="Card.TFrame")
        path_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(path_frame, text="📂 Путь к изображению:", style="TLabel").pack(side=tk.LEFT)
        path_entry = ttk.Entry(
            path_frame, textvariable=self.img_path, state='readonly', width=50, style="TEntry"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        browse_btn = ttk.Button(
            path_frame, text="🔍 Обзор...", command=self.select_image, style="IconButton.TButton"
        )
        browse_btn.pack(side=tk.LEFT)
        folder_btn = ttk.Button(
            path_frame, text="📁 Открыть папку", command=lambda: Utils.open_in_file_manager(
                os.path.dirname(self.img_path.get()) if self.img_path.get() else "."), style="IconButton.TButton"
        )
        folder_btn.pack(side=tk.LEFT, padx=(5, 0))

        drop_frame = ttk.Frame(container, style="DropZone.TFrame")
        drop_frame.pack(fill=tk.X, pady=10)
        self.drop_label = ttk.Label(
            drop_frame,
            text="📥 Перетащите сюда изображение-контейнер\nили кликните для выбора файла",
            anchor="center", font=("Segoe UI", 12, "bold"), cursor="hand2", style="DropLabel.TLabel"
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.drop_label.bind("<Button-1>", lambda e: self.select_image())
        self.preview_img = ttk.Label(container)
        self.preview_img.pack(pady=5)

        data_group = ttk.LabelFrame(
            frame, text="📋 Скрываемые данные", padding=15, style="Card.TLabelframe"
        )
        type_frame = ttk.Frame(data_group, style="Card.TFrame")
        type_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(type_frame, text="📄 Тип данных:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(
            type_frame, text="Текст", variable=self.data_type, value="text", command=self.toggle_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(
            type_frame, text="Файл", variable=self.data_type, value="file", command=self.toggle_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT)

        self.text_frame = ttk.Frame(data_group, style="Card.TFrame")
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Маленькая панель инструментов над текстом
        text_toolbar = ttk.Frame(self.text_frame, style="Card.TFrame")
        text_toolbar.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(text_toolbar, text="🗑️ Очистить", style="IconButton.TButton", command=self.clear_text).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(text_toolbar, text="📋 Вставить", style="IconButton.TButton", command=self.paste_text).pack(
            side=tk.LEFT)

        self.text_input = scrolledtext.ScrolledText(
            self.text_frame, height=10, font=("Consolas", 10), wrap=tk.WORD,
            bg=self.colors["card"], fg=self.colors["text"], insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"], selectforeground="#ffffff", relief="flat", borderwidth=1
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        self.text_input.bind("<KeyRelease>", lambda e: self.update_size_info())

        self.file_frame = ttk.Frame(data_group, style="Card.TFrame")
        file_input_frame = ttk.Frame(self.file_frame, style="Card.TFrame")
        file_input_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(file_input_frame, text="📎 Файл для скрытия:", style="TLabel").pack(side=tk.LEFT)
        file_entry = ttk.Entry(
            file_input_frame, textvariable=self.file_path_var, state='readonly', width=40, style="TEntry"
        )
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.file_entry_widget = file_entry
        ttk.Button(
            file_input_frame, text="📂 Выбрать...", command=self.select_file, style="IconButton.TButton"
        ).pack(side=tk.LEFT)
        self.file_info_label = ttk.Label(self.file_frame, text="ℹ️ Поддерживаемые форматы: любые файлы до 50 МБ",
                                         style="Secondary.TLabel")
        self.file_info_label.pack(fill=tk.X, pady=(6, 0))

        options_frame = ttk.Frame(frame, style="Card.TFrame")
        method_frame = ttk.Frame(options_frame, style="Card.TFrame")
        method_frame.pack(side=tk.LEFT)
        ttk.Label(method_frame, text="⚙️ Метод скрытия:", style="TLabel").pack(side=tk.LEFT)
        method_combo = ttk.Combobox(
            method_frame, textvariable=self.method_var, values=list(STEGANO_METHODS.keys()),
            state="readonly", width=20, style="TCombobox"
        )
        method_combo.pack(side=tk.LEFT, padx=5)
        method_combo.bind("<<ComboboxSelected>>", lambda e: self.update_size_info())
        compression_frame = ttk.Frame(options_frame, style="Card.TFrame")
        compression_frame.pack(side=tk.LEFT, padx=(20, 0))
        ttk.Label(compression_frame, text="💾 Сжатие PNG:", style="TLabel").pack(side=tk.LEFT, padx=(10, 0))
        compression_combo = ttk.Combobox(
            compression_frame, textvariable=self.compression_level, values=list(range(0, 10)),
            state="readonly", width=5, style="TCombobox"
        )
        compression_combo.pack(side=tk.LEFT, padx=5)

        self.size_info_frame = ttk.LabelFrame(
            frame, text="📊 Анализ вместимости", padding=10, style="Card.TLabelframe"
        )
        self.required_size_label = ttk.Label(self.size_info_frame, text="📏 Требуется: выберите данные", style="TLabel")
        self.required_size_label.pack(anchor="w", padx=5)
        ttk.Separator(self.size_info_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        self.capacity_labels = {}
        capacity_pairs = [(["lsb", "noise"], "🟢 LSB / Adaptive-Noise"), (["aelsb", "hill"], "🔵 AELSB / HILL")]
        for methods, label_text in capacity_pairs:
            lbl = ttk.Label(self.size_info_frame, text=f"{label_text}: ожидание...", style="Secondary.TLabel")
            lbl.pack(anchor="w", padx=5)
            for method in methods:
                self.capacity_labels[method] = lbl

        # Индикатор заполнения выбранного метода
        ttk.Separator(self.size_info_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        self.usage_label = ttk.Label(self.size_info_frame, text="📈 Заполнение выбранного метода: не рассчитано",
                                     style="TLabel")
        self.usage_label.pack(anchor="w", padx=5, pady=(0, 6))
        self.usage_bar = ttk.Progressbar(self.size_info_frame, variable=self.usage_var, maximum=100,
                                         style="UsageGreen.Horizontal.TProgressbar")
        self.usage_bar.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.hide_button = ttk.Button(
            frame, text="🔐 Скрыть данные в изображении", style="Accent.TButton", command=self.start_hide
        )

        self.hide_button.pack(side=tk.BOTTOM, pady=(15, 0))
        self.size_info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))
        options_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))

        container.pack(fill=tk.X, pady=(0, 15))
        data_group.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        # Двойной клик по предпросмотру — открыть изображение
        self.preview_img.bind("<Double-Button-1>",
                              lambda e: Utils.open_in_default_app(self.img_path.get()) if self.img_path.get() else None)

    def create_extract_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(frame, text="🔍 Извлечь данные")

        container = ttk.LabelFrame(
            frame,
            text="🖼️ Изображение со скрытыми данными",
            padding=15,
            style="Card.TLabelframe"
        )
        container.pack(fill=tk.X, pady=(0, 15))

        path_frame = ttk.Frame(container, style="Card.TFrame")
        path_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(path_frame, text="📂 Путь к изображению:", style="TLabel").pack(side=tk.LEFT)

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
            text="🔍 Обзор...",
            command=self.select_extract_image,
            style="IconButton.TButton"
        )
        browse_btn.pack(side=tk.LEFT)

        folder_btn = ttk.Button(
            path_frame,
            text="📁 Открыть папку",
            command=lambda: Utils.open_in_file_manager(
                os.path.dirname(self.extract_img_path.get()) if self.extract_img_path.get() else "."),
            style="IconButton.TButton"
        )
        folder_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Дроп-зона для извлечения
        self.extract_drop_label = ttk.Label(
            container,
            text="📥 Перетащите сюда изображение со скрытыми данными\nили кликните для выбора файла",
            anchor="center", font=("Segoe UI", 11, "bold"), cursor="hand2", style="DropLabel.TLabel"
        )
        self.extract_drop_label.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.extract_drop_label.bind("<Button-1>", lambda e: self.select_extract_image())

        self.extract_preview = ttk.Label(container)
        self.extract_preview.pack(pady=5)
        self.extract_preview.bind("<Double-Button-1>", lambda e: Utils.open_in_default_app(
            self.extract_img_path.get()) if self.extract_img_path.get() else None)

        result_group = ttk.LabelFrame(
            frame,
            text="📋 Извлечённые данные",
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

        btn_frame = ttk.Frame(frame, style="Card.TFrame")
        btn_frame.pack(pady=(10, 0))

        self.extract_button = ttk.Button(
            btn_frame,
            text="🔍 Извлечь данные",
            style="Action.TButton",
            command=self.start_extract
        )
        self.extract_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(
            btn_frame,
            text="💾 Сохранить",
            style="Action.TButton",
            command=self.save_extracted,
            state="disabled"
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = ttk.Button(
            btn_frame,
            text="📋 Копировать",
            style="Action.TButton",
            command=self.copy_extracted,
            state="disabled"
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.open_file_button = ttk.Button(
            btn_frame,
            text="🗂 Открыть файл",
            style="Action.TButton",
            command=self.open_extracted_file,
            state="disabled"
        )
        self.open_file_button.pack(side=tk.LEFT, padx=5)

        self.copy_hash_button = ttk.Button(
            btn_frame,
            text="🔑 Копировать хеш",
            style="Action.TButton",
            command=self.copy_extracted_hash,
            state="disabled"
        )
        self.copy_hash_button.pack(side=tk.LEFT, padx=5)

        hist_frame = ttk.LabelFrame(
            frame,
            text="📚 Последние использованные файлы",
            padding=10,
            style="Card.TLabelframe"
        )
        hist_frame.pack(fill=tk.X, pady=(15, 0))

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
        self.notebook.add(frame, text="⚙️ Настройки")

        appearance_group = ttk.LabelFrame(
            frame,
            text="🎨 Тема интерфейса",
            padding=15,
            style="Card.TLabelframe"
        )
        appearance_group.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            appearance_group,
            text="🖌️ Выберите стиль оформления:",
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

        params_group = ttk.LabelFrame(
            frame,
            text="🔧 Параметры по умолчанию",
            padding=15,
            style="Card.TLabelframe"
        )
        params_group.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            params_group,
            text="🧪 Метод скрытия:",
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

        ttk.Label(
            params_group,
            text="📄 Тип данных:",
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

        ttk.Label(
            params_group,
            text="💾 Степень сжатия PNG:",
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

        btn_frame = ttk.Frame(frame, style="Card.TFrame")
        btn_frame.pack(pady=20)

        self.save_settings_button = ttk.Button(
            btn_frame,
            text="💾 Сохранить настройки",
            style="Accent.TButton",
            command=self.save_settings_ui
        )
        self.save_settings_button.pack(side=tk.LEFT, padx=10)

        self.reset_settings_button = ttk.Button(
            btn_frame,
            text="🔄 Сбросить настройки",
            style="TButton",
            command=self.reset_settings
        )
        self.reset_settings_button.pack(side=tk.LEFT, padx=10)

        info_group = ttk.LabelFrame(
            frame,
            text="ℹ️ О программе",
            padding=15,
            style="Card.TLabelframe"
        )
        info_group.pack(fill=tk.X, pady=(15, 0))

        info_text = f"""\
🌟 ØccultoNG v{VERSION}  •  Made with ❤️ by {AUTHOR}

🧩 Что внутри?
• Python 3.10+ – мозг и нервная система
• Pillow – глаза для работы с изображениями
• OpenCV – аналитик, ищущий «тихие» пиксели
• NumPy – скорость, миллионы операций за мгновение
• Tkinter + tkdnd2 – лицо и руки, удобный drag-and-drop

📜 Лицензия: MIT – используй, модифицируй, делись свободно.

💡 Совет: Чтобы получить лучший результат — используйте PNG/BMP/TIFF в качестве контейнера.
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
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.cancel_button = ttk.Button(
            status_frame,
            text="⛔ Отмена",
            command=self.cancel_operation,
            style="TButton"
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.status_label = ttk.Label(
            status_frame,
            text="✅ Готов к работе",
            font=("Segoe UI", 9),
            foreground=self.colors["text_secondary"],
            style="Secondary.TLabel"
        )
        self.status_label.pack(side=tk.RIGHT, padx=(10, 0))

        self.progress_bar.pack_forget()
        self.cancel_button.pack_forget()

    def create_toast(self) -> None:
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
        if self.toast_timer:
            self.root.after_cancel(self.toast_timer)
        self.toast_label.config(text=message)
        self.toast_label.place(relx=0.5, rely=0.9, anchor="center")
        self.toast_timer = self.root.after(duration, self.hide_toast)

    def hide_toast(self) -> None:
        self.toast_label.place_forget()
        self.toast_timer = None

    def on_drag_enter(self, event):
        self.drop_label.configure(style="DropLabelActive.TLabel")

    def on_drag_leave(self, event):
        self.drop_label.configure(style="DropLabel.TLabel")

    def animate_drop(self) -> None:
        original_text = self.drop_label.cget("text")
        self.drop_label.configure(text="✅ Файл успешно загружен!", style="DropLabelActive.TLabel")
        self.root.after(1500, lambda: self.drop_label.configure(text=original_text, style="DropLabel.TLabel"))

    def bind_drag_drop(self) -> None:
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_label.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_image)

    def bind_drag_drop_extract(self) -> None:
        if self.extract_drop_label:
            self.extract_drop_label.drop_target_register(DND_FILES)
            self.extract_drop_label.dnd_bind('<<DragEnter>>', lambda e: self.extract_drop_label.configure(
                style="DropLabelActive.TLabel"))
            self.extract_drop_label.dnd_bind('<<DragLeave>>',
                                             lambda e: self.extract_drop_label.configure(style="DropLabel.TLabel"))
            self.extract_drop_label.dnd_bind('<<Drop>>', self.on_drop_extract_image)

    def bind_file_drop(self) -> None:
        if self.file_entry_widget:
            try:
                self.file_entry_widget.drop_target_register(DND_FILES)
                self.file_entry_widget.dnd_bind('<<Drop>>', self.on_drop_hide_file)
            except Exception as e:
                print(f"DnD для поля файла не поддерживается: {e}")

    def on_drop_image(self, event: tk.Event) -> None:
        path = event.data.strip('{}')
        if os.path.isfile(path) and Utils.is_image_file(path):
            self.img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_size_info()
            self.animate_drop()
            self.show_toast("✅ Изображение загружено")
            self.update_thumbnail(path, self.preview_img)
        else:
            messagebox.showwarning(
                "❌ Неверный формат",
                "Поддерживаются только изображения в форматах:\nPNG, BMP, TIFF, TGA, JPG, JPEG"
            )

    def on_drop_extract_image(self, event: tk.Event) -> None:
        path = event.data.strip('{}')
        if os.path.isfile(path) and Utils.is_image_file(path):
            self.extract_img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.show_toast("✅ Изображение для извлечения загружено")
            self.extract_drop_label.configure(style="DropLabel.TLabel")
            self.update_thumbnail(path, self.extract_preview)
        else:
            messagebox.showwarning(
                "❌ Неверный формат",
                "Поддерживаются только изображения в форматах:\nPNG, BMP, TIFF, TGA, JPG, JPEG"
            )

    def on_drop_hide_file(self, event: tk.Event) -> None:
        path = event.data.strip('{}')
        if os.path.isfile(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb > CONFIG["MAX_FILE_SIZE_MB"]:
                messagebox.showwarning("⚠️ Слишком большой файл",
                                       f"Максимальный размер файла: {CONFIG['MAX_FILE_SIZE_MB']} МБ")
                return
            self.file_path_var.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_file_info_label()
            self.update_size_info()
            self.show_toast("✅ Файл для скрытия добавлен")
        else:
            messagebox.showwarning("❌ Ошибка", "Перетащен не файл.")

    def show_image_preview(self, image_path: str) -> None:
        if not os.path.exists(image_path):
            return

        preview_win = tk.Toplevel(self.root)
        preview_win.title(f"🖼️ Предпросмотр – {os.path.basename(image_path)}")
        preview_win.geometry("600x600")
        preview_win.resizable(True, True)
        preview_win.transient(self.root)
        preview_win.grab_set()
        preview_win.focus_set()
        preview_win.bind("<Escape>", lambda e: preview_win.destroy())

        with Image.open(image_path) as img:
            img.thumbnail((550, 550), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

        frame = ttk.Frame(preview_win, style="Card.TFrame")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        lbl = ttk.Label(frame, image=photo, style="Card.TFrame")
        lbl.image = photo
        lbl.pack(fill=tk.BOTH, expand=True)

        close_btn = ttk.Button(frame, text="❌ Закрыть", command=preview_win.destroy)
        close_btn.pack(pady=10)

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - preview_win.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - preview_win.winfo_reqheight()) // 2
        preview_win.geometry(f"+{x}+{y}")

    def select_image(self) -> None:
        path = filedialog.askopenfilename(
            title="📂 Выберите изображение-контейнер",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.last_open_dir
        )
        if path:
            self.img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_size_info()
            self.update_thumbnail(path, self.preview_img)

    def select_extract_image(self) -> None:
        path = filedialog.askopenfilename(
            title="📂 Выберите изображение с данными",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.last_open_dir
        )
        if path:
            self.extract_img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_thumbnail(path, self.extract_preview)

    def select_file(self) -> None:
        path = filedialog.askopenfilename(title="📂 Выберите файл для скрытия", initialdir=self.last_open_dir)
        if path:
            file_size = os.path.getsize(path) / (1024 * 1024)
            if file_size > CONFIG["MAX_FILE_SIZE_MB"]:
                messagebox.showwarning(
                    "⚠️ Слишком большой файл",
                    f"Максимальный размер файла: {CONFIG['MAX_FILE_SIZE_MB']} МБ"
                )
                return
            self.file_path_var.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_file_info_label()
            self.update_size_info()

    def update_file_info_label(self) -> None:
        try:
            fp = self.file_path_var.get()
            if not fp or not os.path.exists(fp):
                self.file_info_label.config(text="ℹ️ Файл не выбран")
                return
            size = os.path.getsize(fp)
            name = os.path.basename(fp)
            self.file_info_label.config(text=f"📄 {name} • {Utils.format_size(size)}")
        except Exception:
            self.file_info_label.config(text="❌ Ошибка чтения файла")

    def toggle_data_input(self) -> None:
        if self.data_type.get() == "text":
            self.file_frame.pack_forget()
            self.text_frame.pack(fill=tk.BOTH, expand=True)
            self.file_info_label.config(text="ℹ️ Введите текст для скрытия")
        else:
            self.text_frame.pack_forget()
            self.file_frame.pack(fill=tk.X, pady=(10, 0))
            self.file_info_label.config(text="ℹ️ Поддерживаемые форматы: любые файлы до 50 МБ")
        self.update_size_info()

    def update_size_info(self) -> None:
        current_time = time.time()
        if current_time - self.last_update_time < 0.2:
            return
        self.last_update_time = current_time

        self.required_size_label.config(text="📏 Требуется: выберите данные", style="TLabel")
        for _, lbl in self.capacity_labels.items():
            lbl.config(text=f"{lbl.cget('text').split(':')[0]}: ожидание...", style="Secondary.TLabel")
        if self.usage_label:
            self.usage_label.config(text="📈 Заполнение выбранного метода: не рассчитано")
        if self.usage_bar:
            self.usage_var.set(0)
            self.usage_bar.config(style="UsageGreen.Horizontal.TProgressbar")

        try:
            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                self.required_size_label.config(text="❌ Изображение не выбрано", style="Error.TLabel")
                return

            w, h, _ = ImageProcessor.get_image_info(img_path)
            total_pixels = w * h

            required_data_bytes = 0
            if self.data_type.get() == "text":
                text = self.text_input.get("1.0", tk.END).strip()
                if not text:
                    self.required_size_label.config(text="⚠️ Текст не введён", style="Warning.TLabel")
                    return
                required_data_bytes = len(text.encode('utf-8'))
            else:
                file_path = self.file_path_var.get()
                if not os.path.exists(file_path):
                    self.required_size_label.config(text="⚠️ Файл не выбран", style="Warning.TLabel")
                    return
                required_data_bytes = os.path.getsize(file_path)

            self.required_size_label.config(
                text=f"📏 Требуется для данных: {Utils.format_size(required_data_bytes)}",
                style="TLabel"
            )

            capacity_pairs = [
                (["lsb", "noise"], "🟢 LSB/Adaptive-Noise"),
                (["aelsb", "hill"], "🔵 AELSB/HILL")
            ]

            for methods, label_text in capacity_pairs:
                method = methods[0]
                available_data_bits = ImageProcessor.get_capacity_by_method(total_pixels, method)
                available_data_bytes = available_data_bits / 8

                if available_data_bits <= 0:
                    self.capacity_labels[method].config(
                        text=f"{label_text}: 0 B",
                        style="Error.TLabel"
                    )
                    continue

                usage_percent = (
                                        required_data_bytes * 8 / available_data_bits) * 100 if available_data_bits > 0 else 999

                if usage_percent <= 70:
                    style = "Success.TLabel"
                elif usage_percent <= 100:
                    style = "Warning.TLabel"
                else:
                    style = "Error.TLabel"

                selected_marker = ""
                for m in methods:
                    if m == self.method_var.get():
                        selected_marker = "▶ "
                        break

                info_text = (f"{selected_marker}{label_text}: "
                             f"{Utils.format_size(available_data_bytes)} "
                             f"({usage_percent:.1f}%)")

                for m in methods:
                    self.capacity_labels[m].config(text=info_text, style=style)

            # Индикатор заполнения по выбранному методу
            selected_method = self.method_var.get()
            sel_bits = ImageProcessor.get_capacity_by_method(total_pixels, selected_method)
            if sel_bits > 0:
                sel_usage = min(999.0, (required_data_bytes * 8 / sel_bits) * 100)
                self.usage_var.set(min(100.0, sel_usage if sel_usage >= 0 else 0))
                if sel_usage <= 70:
                    self.usage_bar.config(style="UsageGreen.Horizontal.TProgressbar")
                elif sel_usage <= 100:
                    self.usage_bar.config(style="UsageYellow.Horizontal.TProgressbar")
                else:
                    self.usage_bar.config(style="UsageRed.Horizontal.TProgressbar")
                self.usage_label.config(text=f"📈 Заполнение выбранного метода: {sel_usage:.1f}%")

        except Exception as e:
            self.required_size_label.config(text=f"❌ Ошибка: {Utils.truncate_path(str(e), 50)}", style="Error.TLabel")

    def update_thumbnail(self, path: str, target_label: tk.Widget) -> None:
        try:
            with Image.open(path) as img:
                img.thumbnail((200, 200), Image.Resampling.BOX)
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                tk_img = ImageTk.PhotoImage(img)
                target_label.configure(image=tk_img)
                target_label.image = tk_img
        except Exception as e:
            target_label.configure(image='', text=f'❌ Ошибка: {e}')

    def validate_before_hide(self) -> bool:
        img_path = self.img_path.get()
        if not img_path or not os.path.exists(img_path):
            messagebox.showerror("❌ Ошибка", "Изображение не выбрано или не существует")
            return False

        try:
            w, h, total_bits = ImageProcessor.get_image_info(img_path)
            if w < 100 or h < 100:
                messagebox.showwarning("⚠️ Предупреждение",
                                       "Изображение слишком маленькое. Рекомендуется использовать изображения размером не менее 100x100 пикселей.")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", f"Ошибка проверки изображения: {str(e)}")
            return False

        if self.data_type.get() == "text":
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("❌ Ошибка", "Текст для скрытия не введён")
                return False
        else:
            file_path = self.file_path_var.get()
            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("❌ Ошибка", "Файл для скрытия не выбран или не существует")
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
            self.set_progress_mode(True, "⏳ Подготовка данных...")
            self.toggle_buttons(False)
            self.cancel_event.clear()

            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                raise ValueError("❌ Изображение не выбрано или не существует")

            if self.data_type.get() == "text":
                text = self.text_input.get("1.0", tk.END).strip()
                if not text:
                    raise ValueError("❌ Текст для скрытия не введён")
                data = text.encode('utf-8')
            else:
                file_path = self.file_path_var.get()
                if not file_path or not os.path.exists(file_path):
                    raise ValueError("❌ Файл для скрытия не выбран или не существует")
                with open(file_path, 'rb') as f:
                    data = f.read()

            output = filedialog.asksaveasfilename(
                title="💾 Сохранить изображение с данными",
                defaultextension=".png",
                filetypes=[("PNG изображения", "*.png")],
                initialdir=self.last_save_dir
            )
            if not output:
                self.set_progress_mode(False)
                self.toggle_buttons(True)
                return
            self.last_save_dir = os.path.dirname(output)

            required_space_mb = os.path.getsize(img_path) / (1024 * 1024) * 1.1
            free_space_mb = Utils.get_free_space_mb(os.path.dirname(output) or '.')

            if free_space_mb < required_space_mb:
                raise ValueError(
                    f"❌ Недостаточно свободного места на диске.\nТребуется: {Utils.format_size(required_space_mb * 1024 * 1024)}\nДоступно: {Utils.format_size(free_space_mb * 1024 * 1024)}")

            start_time = time.time()

            def progress_callback(progress: float) -> None:
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")

                current_time = time.time()
                if current_time - self.last_progress_update_time < 0.1 and progress < 100:
                    return
                self.last_progress_update_time = current_time

                elapsed_time = current_time - start_time
                speed = (len(data) * (progress / 100)) / elapsed_time if elapsed_time > 0 else 0
                self.root.after(0, lambda: self.progress_var.set(progress))
                self.root.after(0, lambda: self.status_label.config(
                    text=f"⏳ Скрытие данных... {progress:.1f}% | Скорость: {Utils.format_size(speed)}/с"
                ))

            ImageProcessor.hide_data(
                img_path,
                data,
                "",
                output,
                method=self.method_var.get(),
                compression_level=self.compression_level.get(),
                progress_callback=progress_callback,
                cancel_event=self.cancel_event
            )

            self.save_to_history(output)

            def after_success():
                messagebox.showinfo(
                    "✅ Успех",
                    f"🎉 Данные успешно скрыты в изображении!\n\nФайл сохранён: {output}"
                )
                if messagebox.askyesno("📂 Открыть папку", "Открыть папку с сохраненным файлом?"):
                    Utils.open_in_file_manager(output)

            self.root.after(0, after_success)

        except Exception as e:
            if str(e) == "Операция отменена пользователем":
                self.root.after(0, lambda: messagebox.showinfo("⛔ Отмена", "Операция скрытия данных была отменена."))
            else:
                error_msg = f"Произошла ошибка при скрытии данных:\n{str(e)}"
                if "too small" in str(e).lower() or "слишком мало" in str(e).lower():
                    error_msg += "\n\n💡 Возможные причины:\n- Изображение слишком маленькое для объема данных.\n- Выбран неверный метод скрытия."
                    error_msg += "\n\n🛠️ Решения:\n- Используйте изображение большего размера.\n- Попробуйте другой метод скрытия данных."
                elif "not enough space" in str(e).lower() or "недостаточно" in str(e).lower():
                    error_msg += "\n\n💡 Возможные причины:\n- Недостаточно свободного места на диске."
                    error_msg += "\n\n🛠️ Решения:\n- Освободите место на диске и повторите попытку."
                elif "file not found" in str(e).lower() or "не найден" in str(e).lower():
                    error_msg += "\n\n💡 Возможные причины:\n- Указанный файл не существует или был перемещен."
                    error_msg += "\n\n🛠️ Решения:\n- Проверьте путь к файлу и повторите попытку."

                self.root.after(0, lambda: messagebox.showerror("❌ Ошибка", error_msg))
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
            self.set_progress_mode(True, "⏳ Подготовка к извлечению...")
            self.toggle_buttons(False)
            self.cancel_event.clear()
            path = self.extract_img_path.get()
            if not path or not os.path.exists(path):
                raise ValueError("❌ Файл не выбран или не существует")

            start_time = time.time()

            def progress_callback(progress, message=None):
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")

                current_time = time.time()
                if current_time - self.last_progress_update_time < 0.1 and progress < 100:
                    return
                self.last_progress_update_time = current_time

                self.root.after(0, lambda: self.progress_var.set(progress))
                status_text = message if message else f"⏳ Извлечение данных... {progress:.1f}%"
                self.root.after(0, lambda: self.status_label.config(text=status_text))

            extracted = ImageProcessor.extract_data(
                path,
                "",
                None,
                progress_callback,
                self.cancel_event
            )

            # Пытаемся распознать как текст
            try:
                text = extracted.decode('utf-8')
                self.current_extracted = ('text', text)
                self.last_extracted_hash = hashlib.sha256(extracted).hexdigest()
                self.root.after(0, lambda: self.result_text.config(state='normal'))
                self.root.after(0, lambda: self.result_text.delete("1.0", tk.END))
                self.root.after(0, lambda: self.result_text.insert("1.0", text))
                self.root.after(0, lambda: self.result_text.config(state='disabled'))
                self.root.after(0, lambda: self.copy_button.config(state="normal"))
                self.root.after(0, lambda: self.save_button.config(state="normal"))
                self.root.after(0, lambda: self.copy_hash_button.config(state="normal"))
                self.root.after(0, lambda: self.open_file_button.config(state="disabled"))
                self.show_toast("✅ Текст успешно извлечён")
            except UnicodeDecodeError:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(extracted)
                    tmp_file_path = tmp_file.name
                mime_type, encoding = mimetypes.guess_type(tmp_file_path)
                if mime_type:
                    ext = mimetypes.guess_extension(mime_type)
                    if ext:
                        new_name = tmp_file_path + ext
                        os.rename(tmp_file_path, new_name)
                        tmp_file_path = new_name
                self.current_extracted = ('binary', tmp_file_path)
                hex_hash = hashlib.sha256(extracted).hexdigest()
                self.last_extracted_hash = hex_hash
                self.root.after(0, lambda: self.result_text.config(state='normal'))
                self.root.after(0, lambda: self.result_text.delete("1.0", tk.END))
                self.root.after(0, lambda: self.result_text.insert(
                    "1.0",
                    f"📦 Бинарные данные: {len(extracted)} байт\n" +
                    f"🔑 Хеш SHA-256: {hex_hash}\n" +
                    f"📁 Временный файл: {tmp_file_path}"
                ))
                self.root.after(0, lambda: self.result_text.config(state='disabled'))
                self.root.after(0, lambda: self.save_button.config(state="normal"))
                self.root.after(0, lambda: self.copy_button.config(state="disabled"))
                self.root.after(0, lambda: self.copy_hash_button.config(state="normal"))
                self.root.after(0, lambda: self.open_file_button.config(state="normal"))
                self.show_toast("✅ Бинарные данные извлечены")

            self.save_to_history(path)

        except Exception as e:
            if str(e) == "Операция отменена пользователем":
                self.root.after(0, lambda: messagebox.showinfo("⛔ Отмена", "Операция извлечения данных была отменена."))
            else:
                error_msg = f"Произошла ошибка при извлечении данных:\n{str(e)}"
                if "incorrect data length" in str(e).lower() or "некорректная длина данных" in str(e).lower():
                    error_msg += "\n\n💡 Возможные причины:\n- В изображении нет скрытых данных.\n- Использован неверный пароль (если применяется).\n- Изображение повреждено или изменено после скрытия данных."
                    error_msg += "\n\n🛠️ Решения:\n- Убедитесь, что вы используете правильное изображение.\n- Проверьте правильность введенного пароля.\n- Попробуйте извлечь данные другим методом."
                elif "file not found" in str(e).lower() or "не найден" in str(e).lower():
                    error_msg += "\n\n💡 Возможные причины:\n- Указанный файл не существует или был перемещен."
                    error_msg += "\n\n🛠️ Решения:\n- Проверьте путь к файлу и повторите попытку."

                self.root.after(0, lambda: messagebox.showerror("❌ Ошибка", error_msg))
        finally:
            self.set_progress_mode(False)
            self.toggle_buttons(True)

    def save_extracted(self) -> None:
        if not self.current_extracted:
            messagebox.showerror("❌ Ошибка", "Сначала извлеките данные")
            return
        data_type, content = self.current_extracted
        if data_type == 'text':
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
                initialdir=self.last_save_dir
            )
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.last_save_dir = os.path.dirname(path)
                messagebox.showinfo("✅ Сохранено", f"Текст сохранён в файл: {path}")
        else:
            mime_type, encoding = mimetypes.guess_type(content)
            default_ext = ".bin"
            filetypes = [("Бинарные файлы", "*.bin"), ("Все файлы", "*.*")]
            if mime_type:
                ext = mimetypes.guess_extension(mime_type)
                if ext:
                    default_ext = ext
                    desc = mime_type.split('/')[0].capitalize() + " файлы"
                    filetypes.insert(0, (desc, f"*{ext}"))

            path = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                filetypes=filetypes,
                initialdir=self.last_save_dir
            )
            if path:
                shutil.copy(content, path)
                self.last_save_dir = os.path.dirname(path)
                messagebox.showinfo("✅ Сохранено", f"Данные сохранены в файл: {path}")

    def copy_extracted(self) -> None:
        if not self.current_extracted:
            messagebox.showerror("❌ Ошибка", "Нет данных для копирования")
            return
        data_type, content = self.current_extracted
        if data_type == 'text':
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="📋 Текст скопирован в буфер обмена")
            self.show_toast("✅ Скопировано в буфер обмена")
        else:
            messagebox.showwarning("⚠️ Внимание", "Бинарные данные нельзя скопировать в буфер")

    def open_extracted_file(self) -> None:
        if not self.current_extracted:
            return
        data_type, content = self.current_extracted
        if data_type == 'binary' and content and os.path.exists(content):
            Utils.open_in_default_app(content)
        else:
            messagebox.showwarning("❌ Нет файла", "Нет бинарного файла для открытия.")

    def copy_extracted_hash(self) -> None:
        if self.last_extracted_hash:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_extracted_hash)
            self.show_toast("✅ Хеш скопирован в буфер обмена")

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
            self.status_label.config(text="✅ Готов к работе")

    def toggle_buttons(self, enable: bool) -> None:
        self.buttons_disabled = not enable
        state = "normal" if enable else "disabled"
        self.hide_button.config(state=state)
        self.extract_button.config(state=state)
        # Кнопки извлечения активируются контекстно после извлечения
        if enable and self.current_extracted:
            data_type, content = self.current_extracted
            self.save_button.config(state="normal")
            self.copy_hash_button.config(state="normal")
            if data_type == 'text':
                self.copy_button.config(state="normal")
                self.open_file_button.config(state="disabled")
            else:
                self.copy_button.config(state="disabled")
                self.open_file_button.config(state="normal")
        else:
            self.save_button.config(state=state if self.current_extracted else "disabled")
            self.copy_button.config(
                state=state if (self.current_extracted and self.current_extracted[0] == 'text') else "disabled")
            self.open_file_button.config(
                state=state if (self.current_extracted and self.current_extracted[0] == 'binary') else "disabled")
            self.copy_hash_button.config(state=state if self.current_extracted else "disabled")

        self.save_settings_button.config(state=state)
        self.reset_settings_button.config(state=state)

    def cancel_operation(self) -> None:
        self.cancel_event.set()
        self.status_label.config(text="⛔ Отмена операции...")

    def refresh_history(self) -> None:
        for i, lbl in enumerate(self.history_labels):
            if i < len(self.history):
                lbl.config(
                    text=f"📌 {i + 1}. {Utils.truncate_path(self.history[i])}",
                    style="History.TLabel"
                )
                lbl.bind("<Button-1>", lambda e, idx=i: self.load_from_history(idx))
                lbl.bind("<Button-3>", lambda e, idx=i: self.show_history_menu(e, idx))
            else:
                lbl.config(text="", cursor="")
                lbl.unbind("<Button-1>")
                lbl.unbind("<Button-3>")

    def show_history_menu(self, event, idx: int) -> None:
        if not self.history_menu:
            self.history_menu = tk.Menu(self.root, tearoff=0)
            self.history_menu.add_command(label="🔍 Открыть",
                                          command=lambda: self.load_from_history(self.history_menu.index))
            self.history_menu.add_command(label="📁 Открыть папку",
                                          command=lambda: self.open_history_folder(self.history_menu.index))
            self.history_menu.add_separator()
            self.history_menu.add_command(label="🗑️ Удалить из истории",
                                          command=lambda: self.remove_history_item(self.history_menu.index))
        self.history_menu.index = idx
        try:
            self.history_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.history_menu.grab_release()

    def open_history_folder(self, idx: int) -> None:
        if 0 <= idx < len(self.history):
            Utils.open_in_file_manager(self.history[idx])

    def remove_history_item(self, idx: int) -> None:
        if 0 <= idx < len(self.history):
            del self.history[idx]
            self.save_history(self.history)
            self.refresh_history()

    def load_from_history(self, idx: int) -> None:
        if idx < len(self.history):
            path = self.history[idx]
            if os.path.exists(path):
                self.extract_img_path.set(path)
                self.update_thumbnail(path, self.extract_preview)
            else:
                messagebox.showwarning("❌ Файл не найден", "Файл был перемещён или удалён.")
                del self.history[idx]
                self.refresh_history()

    def change_theme(self, theme_name: str) -> None:
        self.theme_manager.set_theme(theme_name)
        self.colors = self.theme_manager.colors
        self.refresh_history()
        if hasattr(self, 'status_label'):
            self.status_label.config(foreground=self.colors["text_secondary"])
        self.check_theme_contrast()
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
        if self.toast_label:
            self.toast_label.config(
                bg=self.colors.get("shadow", "#333333"),
                fg=self.colors.get("text", "#ffffff"),
                highlightcolor=self.colors.get("accent", "#58A6FF")
            )

    def check_theme_contrast(self) -> None:
        c = self.colors
        contrast_ratio = Utils.get_contrast_ratio(c["fg"], c["bg"])
        if contrast_ratio < 4.5:
            print(
                f"⚠️ Предупреждение: Низкая контрастность текста и фона в теме '{self.theme_manager.current_theme}'."
            )

    def save_settings_ui(self) -> None:
        self.save_settings()
        messagebox.showinfo(
            "✅ Настройки сохранены",
            "Настройки успешно применены.\nНекоторые изменения вступят в силу после перезапуска программы."
        )

    def reset_settings(self) -> None:
        if messagebox.askyesno(
                "🔄 Подтверждение сброса",
                "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?\nЭто действие нельзя отменить."
        ):
            try:
                if os.path.exists(CONFIG["SETTINGS_FILE"]):
                    os.remove(CONFIG["SETTINGS_FILE"])
                if os.path.exists(CONFIG["HISTORY_FILE"]):
                    os.remove(CONFIG["HISTORY_FILE"])
                if hasattr(self, 'temp_extracted_file') and self.temp_extracted_file and os.path.exists(
                        self.temp_extracted_file.name):
                    os.unlink(self.temp_extracted_file.name)

                messagebox.showinfo(
                    "🔄 Сброс настроек",
                    "Настройки сброшены. Программа будет закрыта."
                )
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Не удалось сбросить настройки: {e}")

    def show_help(self) -> None:
        help_text = f"""
╔══════════════════════════════════════════════════════════════╗
║            ØccultoNG v{VERSION} – Полное руководство               ║
║        «Скрывай данные как профи, извлекай как детектив»     ║
╚══════════════════════════════════════════════════════════════╝

📌 Что это такое?
ØccultoNG – это современный стеганографический «швейцарский нож».
Он позволяет НЕЗАМЕТНО прятать внутри обычных изображений:
• Секретные тексты, пароли, исходный код, ключи.
• Любые файлы (PDF, ZIP, EXE, видео) размером до 50 МБ.

🔐 Всё, что вы спрячете, останется невидимым для глаза. После скрытия
вы получаете новый PNG-файл, который выглядит как оригинал, но несёт
в себе ваши данные.

──────────────────────────────────────────────────────────────
🧩 Четыре метода. Четыре уровня скрытности.
──────────────────────────────────────────────────────────────
1️⃣ Классический LSB (Least Significant Bit)
   • Плюсы: Максимальная вместимость. Очень быстро.
   • Минусы: Проще обнаружить стеганализом.

2️⃣ Adaptive-Noise
   • Плюсы: Лучше скрытность, чем LSB. Та же вместимость.
   • Минусы: Немного медленнее.

3️⃣ Adaptive-Edge-LSB (AELSB)
   • Плюсы: Устойчивость к помехам (код Хэмминга).
   • Минусы: Вместимость ниже (~42% от LSB).

4️⃣ HILL-CA LSB Matching
   • Плюсы: Максимальная скрытность (контент-адаптивный выбор).
   • Минусы: Ниже скорость и вместимость.

──────────────────────────────────────────────────────────────
🎮 Быстрый старт
──────────────────────────────────────────────────────────────
• «Скрыть»: выберите изображение, введите текст/выберите файл, метод → «🔐 Скрыть».
• «Извлечь»: выберите изображение → «🔍 Извлечь». Определение метода автоматически.

🔹 Горячие клавиши:
• F1 – помощь • Esc – отмена • Ctrl+Enter – действие на вкладке
• Ctrl+O – открыть (контейнер/извлечь) • Ctrl+E – извлечь • Ctrl+S – сохранить извлечённое • Ctrl+L – очистить текст

──────────────────────────────────────────────────────────────
🛠️ Советы
──────────────────────────────────────────────────────────────
• Используйте lossless-форматы (PNG, BMP, TIFF) как контейнер.
• «Анализ вместимости» и индикатор помогут оценить, поместятся ли данные.
• Используйте «Отмена» для прерывания долгих операций.

Автор: {AUTHOR}
"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Помощь")
        help_window.geometry("600x500")
        help_window.resizable(True, True)
        help_window.transient(self.root)
        help_window.grab_set()
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
        close_btn = ttk.Button(help_window, text="❌ Закрыть", command=help_window.destroy, style="TButton")
        close_btn.pack(pady=10)

    def run(self) -> None:
        if "window_size" in self.settings:
            self.root.geometry(self.settings["window_size"])
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
        if hasattr(self, 'temp_extracted_file') and self.temp_extracted_file and os.path.exists(
                self.temp_extracted_file.name):
            try:
                os.unlink(self.temp_extracted_file.name)
            except:
                pass
        self.root.destroy()

    # ─────────────────────────────
    # Доп. UX утилиты
    # ─────────────────────────────
    def bind_shortcuts(self) -> None:
        self.root.bind_all("<F1>", lambda e: self.show_help())
        self.root.bind_all("<Escape>", lambda e: self.cancel_operation())
        self.root.bind_all("<Control-Return>", self.on_ctrl_enter)
        self.root.bind_all("<Control-o>", self.on_ctrl_o)
        self.root.bind_all("<Control-e>", lambda e: self.start_extract())
        self.root.bind_all("<Control-s>", lambda e: self.save_extracted())
        self.root.bind_all("<Control-l>", lambda e: self.clear_text())

    def on_ctrl_enter(self, event=None):
        try:
            current = self.notebook.index(self.notebook.select())
            if current == 0:
                self.start_hide()
            elif current == 1:
                self.start_extract()
        except:
            pass

    def on_ctrl_o(self, event=None):
        try:
            current = self.notebook.index(self.notebook.select())
            if current == 0:
                self.select_image()
            elif current == 1:
                self.select_extract_image()
        except:
            pass

    def clear_text(self) -> None:
        try:
            self.text_input.delete("1.0", tk.END)
            self.update_size_info()
        except:
            pass

    def paste_text(self) -> None:
        try:
            self.text_input.insert(tk.INSERT, self.root.clipboard_get())
            self.update_size_info()
        except:
            pass

    def install_context_menus(self) -> None:
        # Контекстное меню для текстового ввода
        self.text_menu = tk.Menu(self.root, tearoff=0)
        self.text_menu.add_command(label="📋 Копировать", command=lambda: self.text_input.event_generate("<<Copy>>"))
        self.text_menu.add_command(label="📋 Вставить", command=lambda: self.text_input.event_generate("<<Paste>>"))
        self.text_menu.add_command(label="✂️ Вырезать", command=lambda: self.text_input.event_generate("<<Cut>>"))
        self.text_menu.add_separator()
        self.text_menu.add_command(label="📝 Выделить всё",
                                   command=lambda: self.text_input.event_generate("<<SelectAll>>"))
        self.text_menu.add_command(label="🗑️ Очистить", command=self.clear_text)

        def show_text_menu(event):
            try:
                self.text_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.text_menu.grab_release()

        self.text_input.bind("<Button-3>", show_text_menu)

        # Контекстное меню для результата
        self.result_menu = tk.Menu(self.root, tearoff=0)
        self.result_menu.add_command(label="📋 Копировать", command=self.copy_extracted)
        self.result_menu.add_command(label="💾 Сохранить", command=self.save_extracted)
        self.result_menu.add_separator()
        self.result_menu.add_command(label="🔑 Копировать хеш", command=self.copy_extracted_hash)
        self.result_menu.add_command(label="🗂 Открыть файл", command=self.open_extracted_file)

        def show_result_menu(event):
            try:
                self.result_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.result_menu.grab_release()

        self.result_text.bind("<Button-3>", show_result_menu)

    def install_tooltips(self) -> None:
        ToolTip(self.drop_label, "Перетащите файл изображения или кликните, чтобы выбрать")
        if self.extract_drop_label:
            ToolTip(self.extract_drop_label, "Перетащите картинку с данными или кликните для выбора")
        ToolTip(self.hide_button, "Начать скрытие данных (Ctrl+Enter)")
        ToolTip(self.extract_button, "Извлечь данные (Ctrl+Enter)")
        ToolTip(self.save_button, "Сохранить извлечённые данные (Ctrl+S)")
        ToolTip(self.copy_button, "Скопировать извлечённый текст")
        ToolTip(self.open_file_button, "Открыть извлечённый файл")
        ToolTip(self.copy_hash_button, "Скопировать SHA-256 хеш извлечённых данных")


if __name__ == "__main__":
    app = SteganographyUltimate()
    if hasattr(app, 'root') and app.root.winfo_exists():
        app.run()
