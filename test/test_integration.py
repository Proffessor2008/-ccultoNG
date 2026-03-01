"""
Интеграционные тесты для ØccultoNG Pro
"""
import os
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from stegoproexp import AdvancedStego, ImageProcessor
    from stegoproexp import EncryptionManager
    from stegoproexp import FileAnalyzer
except ImportError as e:
    pytest.skip(f"Не удалось импортировать модули: {e}", allow_module_level=True)


class TestIntegrationStegoEncryption:
    """Интеграционные тесты стеганография + шифрование"""

    def test_encrypt_then_hide(self, test_image_rgb, test_secret_data, test_password, test_dir):
        """Тест: шифрование -> скрытие -> извлечение -> дешифрование"""
        # 1. Шифрование данных
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )
        serialized = EncryptionManager.serialize_encrypted_data(encrypted)

        # 2. Скрытие зашифрованных данных
        output_path = os.path.join(test_dir, "output_encrypted.png")

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=serialized.encode('utf-8'),
            password="stego_pwd",
            output_path=output_path
        )

        # 3. Извлечение
        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password="stego_pwd"
        )

        # 4. Десериализация
        encrypted_data = EncryptionManager.deserialize_encrypted_data(
            extracted.decode('utf-8')
        )

        # 5. Дешифрование
        decrypted = EncryptionManager.decrypt_aes_gcm(
            encrypted_data=encrypted_data,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_hide_then_analyze(self, test_image_rgb, test_secret_data, test_dir):
        """Тест: скрытие -> анализ файла"""
        output_path = os.path.join(test_dir, "output_analyze.png")

        # Скрытие данных
        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="test",
            output_path=output_path
        )

        # Анализ файла со скрытыми данными
        results = FileAnalyzer.analyze_file_for_stego(output_path)

        assert results['status'] == 'success'
        # Уровень подозрительности должен быть повышен
        assert results['overall_suspicion'] > 30

    def test_multiple_methods_comparison(self, test_image_rgb, test_secret_data, test_dir):
        """Тест сравнения разных методов стеганографии"""
        methods = ['lsb', 'noise', 'aelsb']
        results = {}

        for method in methods:
            output_path = os.path.join(test_dir, f"output_{method}.png")

            if method == 'lsb':
                AdvancedStego.hide_lsb(
                    container_path=test_image_rgb,
                    data=test_secret_data,
                    password="test",
                    output_path=output_path
                )
                extracted = AdvancedStego.extract_lsb(output_path, "test")
            elif method == 'noise':
                AdvancedStego.hide_noise(
                    container_path=test_image_rgb,
                    data=test_secret_data,
                    password="test",
                    output_path=output_path
                )
                extracted = AdvancedStego.extract_noise(output_path, "test")
            elif method == 'aelsb':
                AdvancedStego.hide_aelsb(
                    container_path=test_image_rgb,
                    data=test_secret_data,
                    password="test",
                    output_path=output_path
                )
                extracted = AdvancedStego.extract_aelsb(output_path, "test")

            results[method] = {
                'success': extracted == test_secret_data,
                'file_size': os.path.getsize(output_path)
            }

        # Все методы должны успешно извлечь данные
        for method, result in results.items():
            assert result['success'] is True, f"Метод {method} не прошел"

    def test_large_scale_operation(self, test_image_large, test_dir):
        """Тест масштабной операции с большим изображением"""
        # Создаем большие данные (100 КБ)
        large_data = b"X" * (100 * 1024)
        output_path = os.path.join(test_dir, "output_large.png")

        # Скрытие
        AdvancedStego.hide_lsb(
            container_path=test_image_large,
            data=large_data,
            password="test",
            output_path=output_path
        )

        # Извлечение
        extracted = AdvancedStego.extract_lsb(
            image_path=output_path,
            password="test"
        )

        assert extracted == large_data
        assert len(extracted) == len(large_data)

    def test_workflow_complete(self, test_image_rgb, test_text_file, test_password, test_dir):
        """Полный тест рабочего процесса"""
        # 1. Чтение файла
        with open(test_text_file, 'rb') as f:
            original_data = f.read()

        # 2. Шифрование
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=original_data,
            password=test_password
        )
        serialized = EncryptionManager.serialize_encrypted_data(encrypted)

        # 3. Скрытие
        stego_path = os.path.join(test_dir, "workflow.png")
        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=serialized.encode('utf-8'),
            password="stego",
            output_path=stego_path
        )

        # 4. Анализ
        analysis = FileAnalyzer.analyze_file_for_stego(stego_path)
        assert analysis['status'] == 'success'

        # 5. Извлечение
        extracted = AdvancedStego.extract_lsb(stego_path, "stego")

        # 6. Десериализация
        encrypted_data = EncryptionManager.deserialize_encrypted_data(
            extracted.decode('utf-8')
        )

        # 7. Дешифрование
        decrypted = EncryptionManager.decrypt_aes_gcm(encrypted_data, test_password)

        # 8. Проверка
        assert decrypted == original_data

        # 9. Сохранение
        output_file = os.path.join(test_dir, "restored.txt")
        with open(output_file, 'wb') as f:
            f.write(decrypted)

        assert os.path.exists(output_file)

        # 10. Финальная проверка
        with open(output_file, 'rb') as f:
            restored_data = f.read()

        assert restored_data == original_data


class TestErrorHandling:
    """Тесты обработки ошибок"""

    def test_corrupted_file_handling(self, test_image_rgb, test_secret_data, test_dir):
        """Тест обработки поврежденного файла"""
        output_path = os.path.join(test_dir, "corrupted.png")

        AdvancedStego.hide_lsb(
            container_path=test_image_rgb,
            data=test_secret_data,
            password="test",
            output_path=output_path
        )

        # Повреждаем файл (изменяем байты в начале файла - заголовок PNG)
        with open(output_path, 'r+b') as f:
            f.seek(10)  # Не повреждаем заголовок PNG, но повреждаем данные
            f.write(b'\xFF' * 100)

        # Может быть вызвана либо ValueError (ошибка контрольной суммы),
        # либо OSError (поврежденный файл не читается PIL)
        with pytest.raises((ValueError, OSError)):
            AdvancedStego.extract_lsb(output_path, "test")

    def test_missing_file_handling(self):
        """Тест обработки отсутствующего файла"""
        with pytest.raises(Exception):
            AdvancedStego.extract_lsb("/nonexistent/file.png", "test")

    def test_invalid_format_handling(self, test_text_file):
        """Тест обработки неверного формата"""
        with pytest.raises(Exception):
            AdvancedStego.hide_lsb(
                container_path=test_text_file,
                data=b"test",
                password="test",
                output_path="/tmp/out.png"
            )


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
