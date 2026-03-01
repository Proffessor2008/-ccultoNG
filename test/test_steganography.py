"""
Тесты для модулей стеганографии
"""
import pytest
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from PIL import Image
import numpy as np
import wave
import hashlib

# Импорты тестируемых классов
try:
    from steganography import AdvancedStego, JPEGStego, AudioStego, ImageProcessor
    from utils import Utils
except ImportError as e:
    pytest.skip(f"Не удалось импортировать модули: {e}", allow_module_level=True)


class TestAdvancedStego:
    """Тесты для класса AdvancedStego"""

    def test_hide_extract_lsb_basic(self, test_image_rgb, test_secret_data, test_dir):
        """Тест базового скрытия и извлечения LSB"""
        output_path = os.path.join(test_dir, "output_lsb.png")
        password = "test123"

        # Скрытие
        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password=password,
            output_path=output_path
        )

        # Проверка существования файла
        assert os.path.exists(output_path), "Выходной файл не создан"

        # Извлечение
        extracted_data = AdvancedStego.extract_lsb(
            image_path=output_path,
            password=password
        )

        # Проверка целостности данных
        assert extracted_data == test_secret_data, "Извлеченные данные не совпадают"

    def test_hide_extract_lsb_empty_data(self, test_image_rgb, test_dir):
        """Тест скрытия пустых данных"""
        output_path = os.path.join(test_dir, "output_empty.png")

        with pytest.raises(ValueError):
            AdvancedStego.hide_lsb(
                container_path=test_image_rgb,
                data=b"",
                password="test",
                output_path=output_path
            )

    def test_hide_lsb_data_too_large(self, test_image_rgb, test_dir):
        """Тест попытки скрыть данные превышающие вместимость"""
        output_path = os.path.join(test_dir, "output_large.png")
        # Создаем данные больше вместимости изображения 200x200
        large_data = b"X" * (200 * 200 * 3 + 1000)

        with pytest.raises(ValueError, match="Данные слишком велики"):
            AdvancedStego.hide_lsb(
                container_path=test_image_rgb,
                data=large_data,
                password="test",
                output_path=output_path
            )

    def test_hide_extract_noise_method(self, test_image_rgb, test_secret_data, test_dir):
        """Тест метода Adaptive-Noise"""
        output_path = os.path.join(test_dir, "output_noise.png")
        password = "noisetest"

        AdvancedStego.hide_noise(
            container_path=test_image_rgb,
            data=test_secret_data,
            password=password,
            output_path=output_path
        )

        assert os.path.exists(output_path)

        extracted = AdvancedStego.extract_noise(
            image_path=output_path,
            password=password
        )

        assert extracted == test_secret_data

    def test_hide_extract_aelsb_method(self, test_image_rgb, test_secret_data, test_dir):
        """Тест метода AELSB с кодом Хэмминга"""
        output_path = os.path.join(test_dir, "output_aelsb.png")
        password = "aelsbtest"

        AdvancedStego.hide_aelsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password=password,
            output_path=output_path
        )

        assert os.path.exists(output_path)

        extracted = AdvancedStego.extract_aelsb(
            image_path=output_path,
            password=password
        )

        assert extracted == test_secret_data

    def test_hide_extract_hill_method(self, test_image_rgb, test_secret_data, test_dir):
        """Тест метода HILL-CA"""
        output_path = os.path.join(test_dir, "output_hill.png")
        password = "hilltest"

        AdvancedStego.hide_hill(
            container_path=test_image_rgb,
            data=test_secret_data,
            password=password,
            output_path=output_path
        )

        assert os.path.exists(output_path)

        extracted = AdvancedStego.extract_hill(
            image_path=output_path,
            password=password
        )

        assert extracted == test_secret_data

    def test_extract_wrong_password(self, test_image_rgb, test_secret_data, test_dir):
        """Тест извлечения с неправильным паролем"""
        output_path = os.path.join(test_dir, "output_wrong.png")

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="correct_password",
            output_path=output_path
        )

        # Попытка извлечь с неправильным паролем
        with pytest.raises(ValueError):
            AdvancedStego.extract_lsb(
                image_path=output_path,
                password="wrong_password"
            )

    def test_extract_from_non_stego_image(self, test_image_rgb):
        """Тест извлечения из изображения без скрытых данных"""
        with pytest.raises(ValueError, match="Магические байты не найдены"):
            AdvancedStego.extract_lsb(
                image_path=test_image_rgb,
                password="any"
            )

    def test_rgba_image_support(self, test_image_rgba, test_secret_data, test_dir):
        """Тест поддержки RGBA изображений"""
        output_path = os.path.join(test_dir, "output_rgba.png")

        AdvancedStego.hide_lsb(
            container_path=test_image_rgba,
            data=test_secret_data,
            password="test",
            output_path=output_path
        )

        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password="test"
        )

        assert extracted == test_secret_data

    def test_image_quality_preserved(self, test_image_rgb, test_dir):
        """Тест сохранения качества изображения после скрытия"""
        output_path = os.path.join(test_dir, "output_quality.png")

        # Получаем размеры оригинала
        with Image.open(test_image_rgb) as img:
            orig_size = img.size
            orig_mode = img.mode

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=b"test",
            password="test",
            output_path=output_path
        )

        # Проверяем размеры выходного изображения
        with Image.open(output_path) as img:
            assert img.size == orig_size, "Размеры изображения изменились"
            assert img.mode in ['RGB', 'RGBA'], "Режим цвета изменился"

    def test_header_integrity(self, test_image_rgb, test_secret_data, test_dir):
        """Тест целостности заголовка"""
        output_path = os.path.join(test_dir, "output_header.png")

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="test",
            output_path=output_path
        )

        # Повреждаем файл (изменяем байты)
        with open(output_path, 'r+b') as f:
            f.seek(100)
            f.write(b'\xFF\xFF\xFF\xFF')

        # Попытка извлечения должна вызвать ошибку контрольной суммы
        with pytest.raises(ValueError, match="Ошибка контрольной суммы"):
            AdvancedStego.extract_lsb(
                image_path=output_path,
                password="test"
            )


class TestJPEGStego:
    """Тесты для JPEG DCT стеганографии"""

    def test_hide_extract_jpeg_dct(self, test_dir):
        """Тест скрытия и извлечения JPEG DCT"""
        # Создаем тестовое JPEG изображение
        img_path = os.path.join(test_dir, "test.jpg")
        img = Image.new('RGB', (256, 256), color=(100, 150, 200))
        img.save(img_path, format='JPEG', quality=100)

        output_path = os.path.join(test_dir, "output_dct.jpg")
        secret_data = b"JPEG DCT test data"

        # Скрытие
        JPEGStego.hide_dct(
            container_path=img_path,
            data=secret_data,
            output_path=output_path
        )

        assert os.path.exists(output_path)

        # Извлечение
        extracted = JPEGStego.extract_dct(stego_path=output_path)

        assert extracted == secret_data

    def test_jpeg_capacity_calculation(self, test_dir):
        """Тест расчета вместимости JPEG"""
        img_path = os.path.join(test_dir, "capacity_test.jpg")
        img = Image.new('RGB', (256, 256), color=(128, 128, 128))
        img.save(img_path, format='JPEG', quality=100)

        capacity = JPEGStego.calculate_capacity(img_path)

        # Для 256x256: (256/8) * (256/8) / 8 = 128 байт примерно
        assert capacity > 0, "Вместимость должна быть больше 0"
        assert capacity < 256 * 256, "Вместимость не может превышать размер изображения"

    def test_jpeg_quality_requirement(self, test_dir):
        """Тест требования качества JPEG 100%"""
        img_path = os.path.join(test_dir, "test_low_quality.jpg")
        img = Image.new('RGB', (256, 256), color=(100, 150, 200))
        img.save(img_path, format='JPEG', quality=50)  # Низкое качество

        output_path = os.path.join(test_dir, "output_low.jpg")
        secret_data = b"Test"

        JPEGStego.hide_dct(
            container_path=img_path,
            data=secret_data,
            output_path=output_path
        )

        # При низком качестве извлечение может не работать
        # Это ожидаемое поведение
        extracted = JPEGStego.extract_dct(stego_path=output_path)
        # Данные могут не совпасть из-за сжатия
        # Тест проверяет что операция выполняется без ошибок


class TestAudioStego:
    """Тесты для аудио стеганографии"""

    def test_hide_extract_wav_lsb(self, test_wav_file, test_secret_data, test_dir):
        """Тест скрытия и извлечения в WAV файле"""
        output_path = os.path.join(test_dir, "output_audio.wav")

        AudioStego.hide_lsb_wav(
            container_path=test_wav_file,
            data=test_secret_data,
            output_path=output_path
        )

        assert os.path.exists(output_path)

        extracted = AudioStego.extract_lsb_wav(stego_path=output_path)

        assert extracted == test_secret_data

    def test_wav_parameters_preserved(self, test_wav_file, test_dir):
        """Тест сохранения параметров WAV файла"""
        output_path = os.path.join(test_dir, "output_params.wav")

        # Получаем оригинальные параметры
        with wave.open(test_wav_file, 'rb') as wav:
            orig_channels = wav.getnchannels()
            orig_sample_width = wav.getsampwidth()
            orig_framerate = wav.getframerate()

        AudioStego.hide_lsb_wav(
            container_path=test_wav_file,
            data=b"test",
            output_path=output_path
        )

        # Проверяем параметры выходного файла
        with wave.open(output_path, 'rb') as wav:
            assert wav.getnchannels() == orig_channels
            assert wav.getsampwidth() == orig_sample_width
            assert wav.getframerate() == orig_framerate

    def test_wav_data_too_large(self, test_wav_file, test_dir):
        """Тест превышения вместимости WAV"""
        output_path = os.path.join(test_dir, "output_wav_large.wav")
        # Создаем данные больше чем может вместить WAV
        large_data = b"X" * 1000000

        with pytest.raises(ValueError, match="Слишком большой объём"):
            AudioStego.hide_lsb_wav(
                container_path=test_wav_file,
                data=large_data,
                output_path=output_path
            )


class TestImageProcessor:
    """Тесты для ImageProcessor"""

    def test_get_image_info(self, test_image_rgb):
        """Тест получения информации об изображении"""
        w, h, bits = ImageProcessor.get_image_info(test_image_rgb)

        assert w > 0, "Ширина должна быть больше 0"
        assert h > 0, "Высота должна быть больше 0"
        assert bits > 0, "Количество бит должно быть больше 0"

    def test_get_capacity_by_method(self, test_image_rgb):
        """Тест расчета вместимости по методам"""
        w, h, total_bits = ImageProcessor.get_image_info(test_image_rgb)

        # LSB должен иметь максимальную вместимость
        capacity_lsb = ImageProcessor.get_capacity_by_method(total_bits, "lsb", w, h)
        capacity_noise = ImageProcessor.get_capacity_by_method(total_bits, "noise", w, h)
        capacity_aelsb = ImageProcessor.get_capacity_by_method(total_bits, "aelsb", w, h)

        assert capacity_lsb > 0
        assert capacity_lsb >= capacity_aelsb, "LSB должен иметь вместимость >= AELSB"

    def test_hide_data_universal(self, test_image_rgb, test_secret_data, test_dir):
        """Тест универсального метода скрытия"""
        output_path = os.path.join(test_dir, "output_universal.png")

        ImageProcessor.hide_data(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="test",
            output_path=output_path,
            method="lsb"
        )

        assert os.path.exists(output_path)

        extracted = ImageProcessor.extract_data(
            image_path=output_path,
            password="test",
            method="lsb"
        )

        assert extracted == test_secret_data

    def test_auto_detect_method(self, test_image_rgb, test_secret_data, test_dir):
        """Тест автоматического определения метода"""
        output_path = os.path.join(test_dir, "output_auto.png")

        # Скрываем с методом lsb
        ImageProcessor.hide_data(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="test",
            output_path=output_path,
            method="lsb"
        )

        # Извлекаем с автоопределением (method=None)
        extracted = ImageProcessor.extract_data(
            image_path=output_path,
            password="test",
            method=None
        )

        assert extracted == test_secret_data


class TestStegoEdgeCases:
    """Тесты граничных случаев"""

    def test_unicode_data(self, test_image_rgb, test_dir):
        """Тест скрытия Unicode данных"""
        output_path = os.path.join(test_dir, "output_unicode.png")
        unicode_data = "Привет мир! 你好世界! مرحبا بالعالم!".encode('utf-8')

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=unicode_data,
            password="test",
            output_path=output_path
        )

        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password="test"
        )

        assert extracted == unicode_data

    def test_special_characters_password(self, test_image_rgb, test_secret_data, test_dir):
        """Тест пароля со специальными символами"""
        output_path = os.path.join(test_dir, "output_special.png")
        password = "P@$$w0rd!#$%^&*()"

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password=password,
            output_path=output_path
        )

        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password=password
        )

        assert extracted == test_secret_data

    def test_empty_password(self, test_image_rgb, test_secret_data, test_dir):
        """Тест с пустым паролем"""
        output_path = os.path.join(test_dir, "output_empty_pwd.png")

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="",
            output_path=output_path
        )

        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password=""
        )

        assert extracted == test_secret_data

    def test_minimum_image_size(self, test_dir):
        """Тест минимального размера изображения"""
        # Создаем минимальное изображение
        img_path = os.path.join(test_dir, "min_image.png")
        img = Image.new('RGB', (10, 10), color=(128, 128, 128))
        img.save(img_path)

        output_path = os.path.join(test_dir, "output_min.png")
        small_data = b"Hi"

        AdvancedStego.hide_lsb(
            container_path=img_path,
            data=small_data,
            password="test",
            output_path=output_path
        )

        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password="test"
        )

        assert extracted == small_data

    def test_consecutive_operations(self, test_image_rgb, test_dir):
        """Тест последовательных операций"""
        data1 = b"First message"
        data2 = b"Second message"

        output1 = os.path.join(test_dir, "output1.png")
        output2 = os.path.join(test_dir, "output2.png")

        # Первая операция
        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=data1,
            password="test1",
            output_path=output1
        )

        extracted1 = AdvancedStego.extract_lsb(
            image_path=output1,
            password="test1"
        )

        # Вторая операция с другим изображением
        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=data2,
            password="test2",
            output_path=output2
        )

        extracted2 = AdvancedStego.extract_lsb(
            image_path=output2,
            password="test2"
        )

        assert extracted1 == data1
        assert extracted2 == data2