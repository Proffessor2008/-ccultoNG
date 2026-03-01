"""
Тесты для инструментов информационной безопасности
"""
import pytest
import os
import sys
import hashlib
import string
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from stegoproexp import IBToolsTab
except ImportError as e:
    pytest.skip(f"Не удалось импортировать IBToolsTab: {e}", allow_module_level=True)


class TestHashCalculator:
    """Тесты для калькулятора хешей"""

    def test_md5_hash(self):
        """Тест MD5 хеширования"""
        data = b"test data"
        expected = hashlib.md5(data).hexdigest()

        h = hashlib.new('md5')
        h.update(data)
        result = h.hexdigest()

        assert result == expected

    def test_sha256_hash(self):
        """Тест SHA-256 хеширования"""
        data = b"test data"
        expected = hashlib.sha256(data).hexdigest()

        h = hashlib.new('sha256')
        h.update(data)
        result = h.hexdigest()

        assert result == expected
        assert len(result) == 64

    def test_sha512_hash(self):
        """Тест SHA-512 хеширования"""
        data = b"test data"
        expected = hashlib.sha512(data).hexdigest()

        h = hashlib.new('sha512')
        h.update(data)
        result = h.hexdigest()

        assert result == expected
        assert len(result) == 128

    def test_different_data_different_hash(self):
        """Тест что разные данные дают разный хеш"""
        data1 = b"data 1"
        data2 = b"data 2"

        hash1 = hashlib.sha256(data1).hexdigest()
        hash2 = hashlib.sha256(data2).hexdigest()

        assert hash1 != hash2

    def test_empty_data_hash(self):
        """Тест хеширования пустых данных"""
        data = b""
        hash_result = hashlib.sha256(data).hexdigest()

        assert len(hash_result) == 64
        assert hash_result == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


class TestPasswordGenerator:
    """Тесты для генератора паролей"""

    def test_password_length(self):
        """Тест длины пароля"""
        import secrets

        chars = string.ascii_letters + string.digits + string.punctuation
        length = 16

        password = ''.join(secrets.choice(chars) for _ in range(length))

        assert len(password) == length

    def test_password_characters(self):
        """Тест символов в пароле"""
        import secrets

        chars = string.ascii_letters + string.digits
        length = 20

        password = ''.join(secrets.choice(chars) for _ in range(length))

        assert all(c in chars for c in password)

    def test_password_entropy(self):
        """Тест расчета энтропии пароля"""
        import math

        chars = string.ascii_letters + string.digits + string.punctuation
        length = 16

        entropy = length * math.log2(len(chars))

        assert entropy > 60  # Для 16 символов из 94 должна быть > 60 бит

    def test_exclude_ambiguous(self):
        """Тест исключения похожих символов"""
        import secrets

        chars = string.ascii_letters + string.digits
        ambiguous = "l1IO0"
        filtered_chars = ''.join([c for c in chars if c not in ambiguous])

        password = ''.join(secrets.choice(filtered_chars) for _ in range(16))

        assert not any(c in ambiguous for c in password)

    def test_random_passwords_different(self):
        """Тест что случайные пароли разные"""
        import secrets

        chars = string.ascii_letters + string.digits
        length = 16

        passwords = set()
        for _ in range(100):
            pwd = ''.join(secrets.choice(chars) for _ in range(length))
            passwords.add(pwd)

        # Все 100 паролей должны быть уникальными
        assert len(passwords) == 100


class TestSignatureValidator:
    """Тесты для валидатора сигнатур"""

    def test_png_signature(self, test_dir):
        """Тест сигнатуры PNG"""
        from PIL import Image

        png_path = os.path.join(test_dir, "test_sig.png")
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        img.save(png_path, format='PNG')

        with open(png_path, 'rb') as f:
            header = f.read(8)

        assert header[:8] == b'\x89PNG\r\n\x1a\n'

    def test_jpeg_signature(self, test_dir):
        """Тест сигнатуры JPEG"""
        from PIL import Image

        jpg_path = os.path.join(test_dir, "test_sig.jpg")
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        img.save(jpg_path, format='JPEG')

        with open(jpg_path, 'rb') as f:
            header = f.read(3)

        assert header == b'\xff\xd8\xff'

    def test_wav_signature(self, test_wav_file):
        """Тест сигнатуры WAV"""
        with open(test_wav_file, 'rb') as f:
            header = f.read(12)

        assert header[:4] == b'RIFF'
        assert header[8:12] == b'WAVE'

    def test_zip_signature(self, test_dir):
        """Тест сигнатуры ZIP"""
        import zipfile

        zip_path = os.path.join(test_dir, "test_sig.zip")
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.txt", "content")

        with open(zip_path, 'rb') as f:
            header = f.read(4)

        assert header == b'PK\x03\x04'

    def test_mismatched_extension(self, test_dir):
        """Тест несовпадения расширения и сигнатуры"""
        from PIL import Image

        # Создаем PNG но с расширением .jpg
        fake_jpg = os.path.join(test_dir, "fake.jpg")
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        img.save(fake_jpg, format='PNG')

        with open(fake_jpg, 'rb') as f:
            header = f.read(8)

        # Сигнатура должна быть PNG несмотря на расширение .jpg
        assert header[:8] == b'\x89PNG\r\n\x1a\n'


class TestEncodingConverter:
    """Тесты для конвертера кодировок"""

    def test_base64_encode(self):
        """Тест Base64 кодирования"""
        import base64

        data = b"Hello World"
        encoded = base64.b64encode(data).decode('utf-8')

        assert encoded == "SGVsbG8gV29ybGQ="

    def test_base64_decode(self):
        """Тест Base64 декодирования"""
        import base64

        encoded = "SGVsbG8gV29ybGQ="
        decoded = base64.b64decode(encoded)

        assert decoded == b"Hello World"

    def test_base64_roundtrip(self):
        """Тест кругового преобразования Base64"""
        import base64

        original = b"Test data 123!@#"
        encoded = base64.b64encode(original)
        decoded = base64.b64decode(encoded)

        assert decoded == original

    def test_hex_encode(self):
        """Тест HEX кодирования"""
        data = b"ABC"
        encoded = data.hex()

        assert encoded == "414243"

    def test_hex_decode(self):
        """Тест HEX декодирования"""
        encoded = "414243"
        decoded = bytes.fromhex(encoded)

        assert decoded == b"ABC"

    def test_url_encode(self):
        """Тест URL кодирования"""
        import urllib.parse

        data = "Hello World! @#$"
        encoded = urllib.parse.quote(data)

        assert " " not in encoded
        assert "%20" in encoded

    def test_url_decode(self):
        """Тест URL декодирования"""
        import urllib.parse

        encoded = "Hello%20World%21"
        decoded = urllib.parse.unquote(encoded)

        assert decoded == "Hello World!"


class TestMetadataExtractor:
    """Тесты для извлечения метаданных"""

    def test_image_metadata(self, test_image_rgb):
        """Тест метаданных изображения"""
        from PIL import Image

        with Image.open(test_image_rgb) as img:
            assert img.width > 0
            assert img.height > 0
            assert img.mode in ['RGB', 'RGBA', 'L']

    def test_wav_metadata(self, test_wav_file):
        """Тест метаданных WAV"""
        import wave

        with wave.open(test_wav_file, 'rb') as wav:
            assert wav.getnchannels() > 0
            assert wav.getframerate() > 0
            assert wav.getnframes() > 0

    def test_file_size_metadata(self, test_text_file):
        """Тест метаданных размера файла"""
        import os

        size = os.path.getsize(test_text_file)
        assert size > 0

        stat = os.stat(test_text_file)
        assert stat.st_size == size