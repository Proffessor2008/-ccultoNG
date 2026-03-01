"""
Тесты для модуля шифрования EncryptionManager
"""
import pytest
import os
import sys
import json
import base64
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from stegoproexp import EncryptionManager
except ImportError as e:
    pytest.skip(f"Не удалось импортировать EncryptionManager: {e}", allow_module_level=True)


class TestEncryptionManager:
    """Тесты для EncryptionManager"""

    def test_encrypt_decrypt_aes_cbc(self, test_secret_data, test_password):
        """Тест AES-256 CBC шифрования"""
        encrypted = EncryptionManager.encrypt_aes_cbc(
            data=test_secret_data,
            password=test_password
        )

        # Проверка структуры зашифрованных данных
        assert 'ciphertext' in encrypted
        assert 'salt' in encrypted
        assert 'iv' in encrypted
        assert 'checksum' in encrypted
        assert encrypted['algorithm'] == 'aes_256_cbc'

        # Дешифрование
        decrypted = EncryptionManager.decrypt_aes_cbc(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_encrypt_decrypt_aes_gcm(self, test_secret_data, test_password):
        """Тест AES-256 GCM шифрования"""
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        assert 'ciphertext' in encrypted
        assert 'nonce' in encrypted
        assert 'tag' in encrypted
        assert encrypted['algorithm'] == 'aes_256_gcm'

        decrypted = EncryptionManager.decrypt_aes_gcm(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_encrypt_decrypt_aes_ctr(self, test_secret_data, test_password):
        """Тест AES-256 CTR шифрования"""
        encrypted = EncryptionManager.encrypt_aes_ctr(
            data=test_secret_data,
            password=test_password
        )

        assert 'ciphertext' in encrypted
        assert 'nonce' in encrypted
        assert 'initial_counter' in encrypted
        assert encrypted['algorithm'] == 'aes_256_ctr'

        decrypted = EncryptionManager.decrypt_aes_ctr(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_encrypt_decrypt_chacha20(self, test_secret_data, test_password):
        """Тест ChaCha20 шифрования"""
        encrypted = EncryptionManager.encrypt_chacha20(
            data=test_secret_data,
            password=test_password
        )

        assert 'ciphertext' in encrypted
        assert 'nonce' in encrypted
        assert encrypted['algorithm'] == 'chacha20'

        decrypted = EncryptionManager.decrypt_chacha20(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_encrypt_decrypt_chacha20_poly1305(self, test_secret_data, test_password):
        """Тест ChaCha20-Poly1305 шифрования"""
        encrypted = EncryptionManager.encrypt_chacha20_poly1305(
            data=test_secret_data,
            password=test_password
        )

        assert 'ciphertext' in encrypted
        assert 'nonce' in encrypted
        assert 'tag' in encrypted
        assert 'aad' in encrypted
        assert encrypted['algorithm'] == 'chacha20_poly1305'

        decrypted = EncryptionManager.decrypt_chacha20_poly1305(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_wrong_password_decryption(self, test_secret_data, test_password):
        """Тест дешифрования с неправильным паролем"""
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        with pytest.raises(ValueError, match="Ошибка аутентификации|Неверный пароль"):
            EncryptionManager.decrypt_aes_gcm(
                encrypted_data=encrypted,
                password="wrong_password"
            )

    def test_serialize_deserialize(self, test_secret_data, test_password):
        """Тест сериализации и десериализации"""
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        # Сериализация
        serialized = EncryptionManager.serialize_encrypted_data(encrypted)

        # Проверка что это валидный JSON
        json_data = json.loads(serialized)
        assert 'ciphertext' in json_data
        assert 'algorithm' in json_data
        assert 'timestamp' in json_data
        assert 'format' in json_data

        # Десериализация
        deserialized = EncryptionManager.deserialize_encrypted_data(serialized)

        # Дешифрование десериализованных данных
        decrypted = EncryptionManager.decrypt_aes_gcm(
            encrypted_data=deserialized,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_save_load_encrypted_file(self, test_secret_data, test_password, test_dir):
        """Тест сохранения и загрузки зашифрованного файла"""
        file_path = os.path.join(test_dir, "test_encrypted.ongcrypt")

        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        # Сохранение
        EncryptionManager.save_encrypted_file(
            encrypted_data=encrypted,
            filepath=file_path
        )

        assert os.path.exists(file_path)

        # Загрузка
        loaded = EncryptionManager.load_encrypted_file(filepath=file_path)

        # Дешифрование
        decrypted = EncryptionManager.decrypt_aes_gcm(
            encrypted_data=loaded,
            password=test_password
        )

        assert decrypted == test_secret_data

    def test_corrupted_data_detection(self, test_secret_data, test_password):
        """Тест обнаружения поврежденных данных"""
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        # Повреждаем ciphertext
        encrypted['ciphertext'] = encrypted['ciphertext'][:-1] + b'\x00'

        with pytest.raises(ValueError):
            EncryptionManager.decrypt_aes_gcm(
                encrypted_data=encrypted,
                password=test_password
            )

    def test_weak_password_validation(self, test_secret_data):
        """Тест валидации слабых паролей"""
        weak_password = "123"  # Менее 8 символов

        with pytest.raises(ValueError, match="минимум 8 символов"):
            EncryptionManager.encrypt_aes_gcm(
                data=test_secret_data,
                password=weak_password
            )

    def test_empty_data_encryption(self, test_password):
        """Тест шифрования пустых данных"""
        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=b"",
            password=test_password
        )

        decrypted = EncryptionManager.decrypt_aes_gcm(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == b""

    def test_large_data_encryption(self, test_password, test_dir):
        """Тест шифрования больших данных"""
        large_data = b"X" * (1024 * 1024)  # 1 MB

        encrypted = EncryptionManager.encrypt_aes_gcm(
            data=large_data,
            password=test_password
        )

        decrypted = EncryptionManager.decrypt_aes_gcm(
            encrypted_data=encrypted,
            password=test_password
        )

        assert decrypted == large_data
        assert len(decrypted) == len(large_data)

    def test_xor_encryption(self, test_secret_data):
        """Тест XOR шифрования (учебный)"""
        key = "test_key"

        encrypted = EncryptionManager.encrypt_xor(
            data=test_secret_data,
            key=key
        )

        assert encrypted['algorithm'] == 'xor'

        decrypted = EncryptionManager.decrypt_xor(
            encrypted_data=encrypted
        )

        assert decrypted == test_secret_data

    def test_base64_encoding(self, test_secret_data):
        """Тест Base64 кодирования"""
        encoded = EncryptionManager.encrypt_base64(
            data=test_secret_data
        )

        assert encoded['algorithm'] == 'base64'
        assert 'encoded' in encoded

        decoded = EncryptionManager.decrypt_base64(
            encrypted_data=encoded
        )

        assert decoded == test_secret_data

    def test_algorithm_info(self):
        """Тест получения информации об алгоритме"""
        info = EncryptionManager.get_algorithm_info("aes_256_gcm")

        assert 'name' in info
        assert 'description' in info
        assert 'security' in info
        assert 'use_cases' in info
        assert 'limitations' in info

    def test_security_levels(self):
        """Тест уровней безопасности алгоритмов"""
        assert EncryptionManager.SECURITY_LEVELS["aes_256_gcm"] == "very_high"
        assert EncryptionManager.SECURITY_LEVELS["aes_256_cbc"] == "high"
        assert EncryptionManager.SECURITY_LEVELS["xor"] == "none"
        assert EncryptionManager.SECURITY_LEVELS["base64"] == "none"

    def test_different_passwords_different_output(self, test_secret_data):
        """Тест что разные пароли дают разный вывод"""
        encrypted1 = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password="password1"
        )

        encrypted2 = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password="password2"
        )

        # Salt должен быть разным
        assert encrypted1['salt'] != encrypted2['salt']

        # Ciphertext тоже должен быть разным из-за разного salt
        assert encrypted1['ciphertext'] != encrypted2['ciphertext']

    def test_same_password_same_data_different_output(self, test_secret_data, test_password):
        """Тест что одинаковые данные с тем же паролем дают разный вывод (из-за salt)"""
        encrypted1 = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        encrypted2 = EncryptionManager.encrypt_aes_gcm(
            data=test_secret_data,
            password=test_password
        )

        # Salt должен быть разным для каждой операции
        assert encrypted1['salt'] != encrypted2['salt']

        # Оба должны дешифроваться в одинаковые данные
        decrypted1 = EncryptionManager.decrypt_aes_gcm(encrypted1, test_password)
        decrypted2 = EncryptionManager.decrypt_aes_gcm(encrypted2, test_password)

        assert decrypted1 == decrypted2 == test_secret_data