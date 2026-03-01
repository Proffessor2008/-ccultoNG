"""
Конфигурация и фикстуры для тестов ØccultoNG Pro
"""
import os
import shutil
import struct
import sys
import tempfile
import wave
from pathlib import Path

import pytest
from PIL import Image

# Добавляем корень проекта в path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Импорты тестируемых модулей
from Crypto.Random import get_random_bytes


@pytest.fixture(scope="session")
def test_dir():
    """Создает временную директорию для тестов"""
    temp_dir = tempfile.mkdtemp(prefix="occulto_test_")
    yield temp_dir
    # Очистка после всех тестов
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_image_rgb(test_dir):
    """Создает тестовое RGB изображение"""
    img_path = os.path.join(test_dir, "test_image.png")
    img = Image.new('RGB', (200, 200), color=(128, 128, 128))
    img.save(img_path, format='PNG')
    return img_path


@pytest.fixture
def test_image_rgba(test_dir):
    """Создает тестовое RGBA изображение"""
    img_path = os.path.join(test_dir, "test_image_rgba.png")
    img = Image.new('RGBA', (200, 200), color=(128, 128, 128, 255))
    img.save(img_path, format='PNG')
    return img_path


@pytest.fixture
def test_image_large(test_dir):
    """Создает большое тестовое изображение"""
    img_path = os.path.join(test_dir, "test_image_large.png")
    img = Image.new('RGB', (1000, 1000), color=(100, 150, 200))
    img.save(img_path, format='PNG')
    return img_path


@pytest.fixture
def test_wav_file(test_dir):
    """Создает тестовый WAV файл"""
    wav_path = os.path.join(test_dir, "test_audio.wav")
    with wave.open(wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        # Генерируем 1 секунду тишины
        frames = struct.pack('<' + 'h' * 44100, *[0] * 44100)
        wav_file.writeframes(frames)
    return wav_path


@pytest.fixture
def test_text_file(test_dir):
    """Создает тестовый текстовый файл"""
    txt_path = os.path.join(test_dir, "test_data.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("Тестовые данные для скрытия\n" * 10)
    return txt_path


@pytest.fixture
def test_binary_file(test_dir):
    """Создает тестовый бинарный файл"""
    bin_path = os.path.join(test_dir, "test_data.bin")
    with open(bin_path, 'wb') as f:
        f.write(get_random_bytes(1024))
    return bin_path


@pytest.fixture
def test_password():
    """Возвращает тестовый пароль"""
    return "TestPassword123!"


@pytest.fixture
def test_secret_data():
    """Возвращает тестовые секретные данные"""
    return b"Secret message for steganography testing!"


@pytest.fixture(scope="session")
def supported_formats():
    """Возвращает список поддерживаемых форматов"""
    return {
        'images': ['.png', '.bmp', '.tiff', '.tga', '.jpg', '.jpeg'],
        'audio': ['.wav'],
        'all': ['.png', '.bmp', '.tiff', '.tga', '.jpg', '.jpeg', '.wav']
    }


@pytest.fixture
def cleanup_files(test_dir):
    """Фикстура для очистки файлов после теста"""
    created_files = []
    yield created_files
    for file_path in created_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
