"""
Тесты для утилит Utils
"""
import pytest
import os
import sys
import hashlib
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from stegoproexp import Utils
except ImportError as e:
    pytest.skip(f"Не удалось импортировать Utils: {e}", allow_module_level=True)


class TestUtils:
    """Тесты для Utils"""

    def test_safe_int_valid(self):
        """Тест safe_int с валидными данными"""
        assert Utils.safe_int("123") == 123
        assert Utils.safe_int("0") == 0
        assert Utils.safe_int("-456") == -456

    def test_safe_int_invalid(self):
        """Тест safe_int с невалидными данными"""
        assert Utils.safe_int("abc") == 0
        assert Utils.safe_int("") == 0
        assert Utils.safe_int(None) == 0
        assert Utils.safe_int("12.34") == 0

    def test_safe_int_fallback(self):
        """Тест safe_int с fallback значением"""
        assert Utils.safe_int("abc", fallback=-1) == -1
        assert Utils.safe_int("", fallback=100) == 100

    def test_truncate_path_short(self):
        """Тест truncate_path для короткого пути"""
        path = "/short/path.txt"
        result = Utils.truncate_path(path, max_len=40)
        assert result == path

    def test_truncate_path_long(self):
        """Тест truncate_path для длинного пути"""
        path = "/very/long/path/that/should/be/truncated.txt"
        result = Utils.truncate_path(path, max_len=20)
        assert len(result) <= 20
        assert result.startswith("...")

    def test_format_size_bytes(self):
        """Тест форматирования размера в байтах"""
        assert Utils.format_size(0) == "0.00 B"
        assert Utils.format_size(100) == "100.00 B"
        assert Utils.format_size(1023) == "1023.00 B"

    def test_format_size_kb(self):
        """Тест форматирования размера в КБ"""
        assert Utils.format_size(1024) == "1.00 KB"
        assert Utils.format_size(2048) == "2.00 KB"

    def test_format_size_mb(self):
        """Тест форматирования размера в МБ"""
        assert Utils.format_size(1024 * 1024) == "1.00 MB"
        assert Utils.format_size(5 * 1024 * 1024) == "5.00 MB"

    def test_format_size_gb(self):
        """Тест форматирования размера в ГБ"""
        assert Utils.format_size(1024 * 1024 * 1024) == "1.00 GB"

    def test_format_size_negative(self):
        """Тест форматирования отрицательного размера"""
        assert Utils.format_size(-100) == "0 B"

    def test_get_file_checksum(self, test_text_file):
        """Тест получения контрольной суммы файла"""
        checksum = Utils.get_file_checksum(test_text_file)

        assert len(checksum) == 64  # SHA-256 = 64 hex символа
        assert all(c in '0123456789abcdef' for c in checksum)

        # Проверка что одинаковые файлы дают одинаковый хеш
        checksum2 = Utils.get_file_checksum(test_text_file)
        assert checksum == checksum2

    def test_get_file_checksum_different_files(self, test_text_file, test_binary_file):
        """Тест что разные файлы дают разный хеш"""
        checksum1 = Utils.get_file_checksum(test_text_file)
        checksum2 = Utils.get_file_checksum(test_binary_file)

        assert checksum1 != checksum2

    def test_is_supported_container_image(self, test_image_rgb):
        """Тест проверки поддерживаемого контейнера (изображение)"""
        assert Utils.is_supported_container(test_image_rgb) is True

    def test_is_supported_container_audio(self, test_wav_file):
        """Тест проверки поддерживаемого контейнера (аудио)"""
        assert Utils.is_supported_container(test_wav_file) is True

    def test_is_supported_container_invalid(self, test_dir):
        """Тест проверки неподдерживаемого контейнера"""
        invalid_path = os.path.join(test_dir, "invalid.xyz")
        with open(invalid_path, 'w') as f:
            f.write("test")

        assert Utils.is_supported_container(invalid_path) is False

    def test_is_supported_container_nonexistent(self):
        """Тест проверки несуществующего файла"""
        assert Utils.is_supported_container("/nonexistent/file.png") is False

    def test_get_file_info_image(self, test_image_rgb):
        """Тест получения информации об изображении"""
        info = Utils.get_file_info(test_image_rgb)

        assert 'name' in info
        assert 'size' in info
        assert 'size_formatted' in info
        assert 'created' in info
        assert 'modified' in info
        assert 'extension' in info
        assert info['type'] == 'image'
        assert 'dimensions' in info

    def test_get_file_info_audio(self, test_wav_file):
        """Тест получения информации об аудио"""
        info = Utils.get_file_info(test_wav_file)

        assert info['type'] == 'audio'
        assert 'channels' in info
        assert 'sample_rate' in info
        assert 'duration' in info

    def test_get_file_info_nonexistent(self):
        """Тест получения информации о несуществующем файле"""
        info = Utils.get_file_info("/nonexistent/file.txt")

        assert 'error' in info

    def test_create_backup(self, test_text_file, test_dir):
        """Тест создания резервной копии"""
        backup_path = Utils.create_backup(test_text_file)

        assert backup_path != ""
        assert os.path.exists(backup_path)
        assert "backup" in backup_path.lower()

    def test_create_backup_nonexistent(self):
        """Тест создания резервной копии несуществующего файла"""
        backup_path = Utils.create_backup("/nonexistent/file.txt")
        assert backup_path == ""

    def test_calculate_brightness(self):
        """Тест расчета яркости цвета"""
        # Белый цвет
        brightness_white = Utils.calculate_brightness("#FFFFFF")
        assert 0.9 <= brightness_white <= 1.0

        # Черный цвет
        brightness_black = Utils.calculate_brightness("#000000")
        assert 0.0 <= brightness_black <= 0.1

        # Серый цвет
        brightness_gray = Utils.calculate_brightness("#808080")
        assert 0.2 <= brightness_gray <= 0.6

    def test_get_contrast_ratio(self):
        """Тест расчета коэффициента контраста"""
        # Черный на белом
        ratio = Utils.get_contrast_ratio("#000000", "#FFFFFF")
        assert ratio > 20  # Максимальный контраст

        # Одинаковые цвета
        ratio_same = Utils.get_contrast_ratio("#808080", "#808080")
        assert ratio_same == 1.0

    def test_open_in_file_manager(self, test_dir):
        """Тест открытия в файловом менеджере"""
        # Тест не должен вызывать ошибок
        try:
            Utils.open_in_file_manager(test_dir)
        except Exception as e:
            pytest.fail(f"open_in_file_manager вызвал ошибку: {e}")

    def test_get_system_info(self):
        """Тест получения информации о системе"""
        info = Utils.get_system_info()

        assert 'platform' in info
        assert 'python_version' in info
        assert 'working_directory' in info
        assert 'home_directory' in info