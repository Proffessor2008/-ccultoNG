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
VERSION = "0.2.1"
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
            b2_idx = b0_idx + 2
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

                # ─── ИСПРАВЛЕННАЯ ЛОГИКА ИЗМЕНЕНИЯ ПИКСЕЛЯ (LSB Matching) ───
                # Эта новая логика гарантирует, что LSB будет изменен корректно
                # для всех значений от 0 до 255, устраняя ошибку контрольной суммы.
                if val == 0:
                    # Если 0, можно изменить только на 1
                    pixels_flat_rgb[idx_p, idx_c] = 1
                elif val == 255:
                    # Если 255, можно изменить только на 254
                    pixels_flat_rgb[idx_p, idx_c] = 254
                else:
                    # Для всех остальных случаев меняем на +1 или -1.
                    # Эта простая операция всегда меняет четность (LSB).
                    if val % 2 == 1:  # Если нечетное, делаем четным
                        pixels_flat_rgb[idx_p, idx_c] = val - 1
                    else:  # Если четное, делаем нечетным
                        pixels_flat_rgb[idx_p, idx_c] = val + 1
                # ──────────────────────────────────────────────────────────

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
            # Эти методы используют все доступные LSB
            capacity_bits = total_lsb_bits
        elif method in ("aelsb", "hill"):
            # Код Хэмминга (7,3) использует 7 LSB для 3 бит данных
            capacity_bits = int(total_lsb_bits * (3 / 7))
        else:
            return 0  # Неизвестный метод

        # Вычитаем размер фиксированного заголовка, чтобы получить полезную ёмкость
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
            # Пробуем все по очереди, включая HILL
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

                # Внутренняя функция для передачи прогресса
                def internal_progress(p):
                    if progress_callback:
                        # Масштабируем прогресс, чтобы показать проверку каждого метода
                        base_progress = methods_to_try.index(method_name) * (100 / len(methods_to_try))
                        scaled_progress = p / len(methods_to_try)
                        progress_callback(base_progress + scaled_progress)

                # Пробуем извлечь
                data = extractor(image_path, password, internal_progress, cancel_event)

                # Если мы здесь, значит, извлечение удалось и чексумма верна
                if progress_callback:
                    progress_callback(100.0,
                                      f"Данные найдены методом: {STEGANO_METHODS.get(method_name, method_name)}!")
                return data

            except (ValueError, IndexError, InterruptedError) as e:
                # Эти ошибки ожидаемы, если метод не тот или данные повреждены
                last_error = e
                # Просто переходим к следующему методу
                continue

        # Если ни один метод не сработал
        if isinstance(last_error, InterruptedError):
            raise last_error
        if last_error:
            raise ValueError(
                f"Не удалось извлечь данные. Возможно, изображение не содержит скрытой информации или данные повреждены. Последняя ошибка: {last_error}")
        else:
            raise ValueError("Не удалось извлечь данные. Ни один из поддерживаемых методов не подошел.")


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
        self.last_progress_update_time = 0
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
        self.size_info_frame = None
        self.required_size_label = None
        self.capacity_labels = {}

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
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            style="DropLabel.TLabel"
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
        method_combo.bind("<<ComboboxSelected>>", lambda e: self.update_size_info())

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
        self.size_info_frame = ttk.LabelFrame(
            frame,
            text="Анализ вместимости",
            padding=10,
            style="Card.TLabelframe"
        )
        self.size_info_frame.pack(fill=tk.X, pady=(15, 5))

        self.required_size_label = ttk.Label(self.size_info_frame, text="Требуется: -", style="TLabel")
        self.required_size_label.pack(anchor="w", padx=5)

        ttk.Separator(self.size_info_frame, orient="horizontal").pack(fill=tk.X, pady=5)

        self.capacity_labels = {}
        for method_key, method_name in STEGANO_METHODS.items():
            lbl = ttk.Label(self.size_info_frame, text=f"{method_name}: -", style="Secondary.TLabel")
            lbl.pack(anchor="w", padx=5)
            self.capacity_labels[method_key] = lbl
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

    def on_drag_enter(self, event):
        # Акцентируем дроп-зону
        self.drop_label.configure(style="DropLabelActive.TLabel")

    def on_drag_leave(self, event):
        # Возвращаем спокойный вид
        self.drop_label.configure(style="DropLabel.TLabel")

    def animate_drop(self) -> None:
        original_text = self.drop_label.cget("text")
        self.drop_label.configure(text="✅ Файл загружен!", style="DropLabelActive.TLabel")
        self.root.after(1500, lambda: self.drop_label.configure(text=original_text, style="DropLabel.TLabel"))

    def bind_drag_drop(self) -> None:
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_label.dnd_bind('<<DragLeave>>', self.on_drag_leave)
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
        if current_time - self.last_update_time < 0.2:  # Ограничение частоты обновлений
            return
        self.last_update_time = current_time

        # Сначала очищаем все метки
        self.required_size_label.config(text="Требуется: -")
        for method_key, lbl in self.capacity_labels.items():
            lbl.config(text=f"{STEGANO_METHODS[method_key]}: -", style="Secondary.TLabel")

        try:
            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                self.required_size_label.config(text="Изображение не выбрано", style="Error.TLabel")
                return

            w, h, _ = ImageProcessor.get_image_info(img_path)
            total_pixels = w * h

            # Определяем требуемый размер данных
            required_data_bytes = 0
            if self.data_type.get() == "text":
                text = self.text_input.get("1.0", tk.END).strip()
                if not text:
                    self.required_size_label.config(text="Текст не введён", style="Warning.TLabel")
                    return
                required_data_bytes = len(text.encode('utf-8'))
            else:
                file_path = self.file_path_var.get()
                if not os.path.exists(file_path):
                    self.required_size_label.config(text="Файл не выбран", style="Warning.TLabel")
                    return
                required_data_bytes = os.path.getsize(file_path)

            total_required_bits = (required_data_bytes + HEADER_FULL_LEN) * 8
            self.required_size_label.config(
                text=f"Требуется для данных: {Utils.format_size(required_data_bytes)}",
                style="TLabel"
            )

            # Рассчитываем и отображаем вместимость для каждого метода
            selected_method = self.method_var.get()

            for method_key, lbl in self.capacity_labels.items():
                # Получаем полезную вместимость в битах (заголовок уже вычтен)
                available_data_bits = ImageProcessor.get_capacity_by_method(total_pixels, method_key)
                available_data_bytes = available_data_bits / 8

                if available_data_bits <= 0:
                    lbl.config(text=f"{STEGANO_METHODS[method_key]}: 0 B", style="Error.TLabel")
                    continue

                # Процент использования от ПОЛЕЗНОЙ вместимости метода
                usage_percent = (
                                        required_data_bytes * 8 / available_data_bits) * 100 if available_data_bits > 0 else 999

                if usage_percent <= 70:
                    style = "Success.TLabel"
                elif usage_percent <= 100:
                    style = "Warning.TLabel"
                else:
                    style = "Error.TLabel"

                # Добавляем маркер для выбранного метода
                prefix = "▶ " if method_key == selected_method else "  "

                info_text = (f"{prefix}{STEGANO_METHODS[method_key]}: "
                             f"{Utils.format_size(available_data_bytes)} "
                             f"({usage_percent:.1f}%)")

                lbl.config(text=info_text, style=style)

        except Exception as e:
            self.required_size_label.config(text=f"Ошибка: {Utils.truncate_path(str(e), 50)}", style="Error.TLabel")

    def update_thumbnail(self, path: str, target_label: tk.Widget) -> None:
        """Создаёт и показывает миниатюру 200×200 в указанной метке."""
        try:
            with Image.open(path) as img:
                img.thumbnail((200, 200), Image.Resampling.BOX)
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

            start_time = time.time()

            def progress_callback(progress: float) -> None:
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")

                current_time = time.time()
                if current_time - self.last_progress_update_time < 0.1 and progress < 100:  # Обновлять не чаще 10 раз/сек
                    return
                self.last_progress_update_time = current_time

                elapsed_time = current_time - start_time
                speed = progress / 100 * len(data) / elapsed_time if elapsed_time > 0 else 0
                self.root.after(0, lambda: self.progress_var.set(progress))
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Скрытие данных... {progress:.1f}% | {Utils.format_size(speed)}/s"
                ))

            ImageProcessor.hide_data(
                img_path,
                data,
                "",  # Пустой пароль
                output,
                method=self.method_var.get(),
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

            # Извлечение данных с автоматическим определением метода
            start_time = time.time()

            def progress_callback(progress, message=None):
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")

                current_time = time.time()
                if current_time - self.last_progress_update_time < 0.1 and progress < 100:
                    return
                self.last_progress_update_time = current_time

                self.root.after(0, lambda: self.progress_var.set(progress))
                status_text = message if message else f"Извлечение данных... {progress:.1f}%"
                self.root.after(0, lambda: self.status_label.config(text=status_text))

            # Передаем None для автоматического определения метода
            extracted = ImageProcessor.extract_data(
                path,
                "",  # Пустой пароль
                None,  # Автоматическое определение метода
                progress_callback,
                self.cancel_event
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
           • Как работает: Последовательно заменяет самый незначительный бит
             в каждом цветовом канале (R, G, B) на бит ваших данных.
             Это как писать карандашом на последней странице каждой книги в библиотеке.
           • Плюсы: Максимальная вместимость (до 12.5% от размера файла). Очень быстро.
           • Минусы: Легко обнаруживается статистическим анализом (стеганализом).
           • Когда использовать: Когда скорость и объём важнее скрытности.
             Идеально для личных архивов, где никто не будет искать подвох.

        2️⃣ Adaptive-Noise
           • Как работает: "Разбрасывает" биты ваших данных по пикселям изображения
             в псевдослучайном порядке. Порядок определяется паролем (даже если он пустой).
             Это как вырвать страницы из книги и спрятать их в случайных местах по всей библиотеке.
           • Плюсы: Гораздо устойчивее к простому стеганализу, чем LSB.
           • Минусы: Та же вместимость, что и у LSB, но чуть медленнее.
           • Когда использовать: Хороший баланс между скоростью и безопасностью.
             Затрудняет обнаружение данных без знания "карты" (пароля).

        3️⃣ Adaptive-Edge-LSB (AELSB)
           • Как работает: Этот метод использует код Хэмминга (7,3). Он берёт 3 бита
             ваших данных и кодирует их с помощью 7 битов в изображении.
             Это добавляет избыточность, которая помогает выявить и исправить ошибки.
           • Плюсы: Повышенная устойчивость к случайным помехам и незначительным искажениям.
           • Минусы: Вместимость значительно ниже (примерно 3/7 или ~42% от LSB).
           • Когда использовать: Когда целостность данных важнее максимального объёма.

        4️⃣ HILL-CA LSB Matching (Content-Adaptive)
           • Как работает: Самый продвинутый метод. Сначала алгоритм HILL анализирует
             изображение и находит самые "шумные", текстурированные области (трава, волосы,
             рябь на воде). Затем он встраивает данные с помощью кода Хэмминга (как в AELSB),
             но только в эти, наименее заметные для глаза, места.
           • Плюсы: Максимальный уровень скрытности. Чрезвычайно трудно обнаружить
             как визуально, так и с помощью программ-анализаторов.
           • Минусы: Самая низкая вместимость и самая низкая скорость работы.
           • Когда использовать: Когда скрытность — абсолютный приоритет. Идеально для
             публикации в открытых источниках, где изображение могут изучать.

        ──────────────────────────────────────────────────────────────
        🎮 Быстрый старт: Скрыть за 30 секунд
        ──────────────────────────────────────────────────────────────
        1. Вкладка «Скрыть»: перетащите или выберите картинку-контейнер.
        2. Введите текст или выберите файл для скрытия.
        3. Выберите подходящий метод из списка выше.
        4. Нажмите «🔐 Скрыть» и сохраните новый PNG-файл.

        Готово! Ваша картинка визуально не изменилась, но внутри – ваш секрет.

        ──────────────────────────────────────────────────────────────
        🔍 Извлечение данных: Еще проще
        ──────────────────────────────────────────────────────────────
        1. Вкладка «Извлечь»: выберите изображение со скрытыми данными.
        2. Нажмите «🔍 Извлечь».

        Программа сама переберёт все методы и найдёт данные, если они есть.
        Если извлечён файл, его можно сразу сохранить. Если текст — скопировать.

        ──────────────────────────────────────────────────────────────
        🛠️ Продвинутые советы
        ──────────────────────────────────────────────────────────────
        • Используйте PNG без сжатия (или другие lossless-форматы) как контейнер.
          JPG-изображения тоже можно, но их артефакты сжатия могут мешать.
        • Сохранённый файл всегда будет в формате PNG, чтобы избежать потерь данных.
        • Строка статуса «Требуется/Доступно» поможет оценить, поместятся ли ваши
          данные. Зелёный – отлично, жёлтый – приемлемо, красный – риск быть замеченным.
        • Кнопка «Отмена» прервёт любую долгую операцию.

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
