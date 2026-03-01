"""
Тесты для FileAnalyzer
"""
import os
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from stegoproexp import FileAnalyzer
except ImportError as e:
    pytest.skip(f"Не удалось импортировать FileAnalyzer: {e}", allow_module_level=True)


class TestFileAnalyzer:
    """Тесты для FileAnalyzer"""

    def test_calculate_entropy_random_data(self):
        """Тест энтропии для случайных данных"""
        random_data = np.random.bytes(10000)
        entropy = FileAnalyzer.calculate_entropy(random_data)

        # Энтропия случайных данных должна быть близка к 8
        assert 7.5 <= entropy <= 8.0, f"Энтропия {entropy} должна быть близка к 8"

    def test_calculate_entropy_uniform_data(self):
        """Тест энтропии для равномерных данных"""
        uniform_data = b'\x00' * 10000
        entropy = FileAnalyzer.calculate_entropy(uniform_data)

        # Энтропия равномерных данных должна быть 0
        assert entropy == 0.0, f"Энтропия равномерных данных должна быть 0, получено {entropy}"

    def test_analyze_lsb_distribution_natural(self, test_image_rgb):
        """Тест анализа LSB для естественного изображения"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        lsb_analysis = FileAnalyzer.analyze_lsb_distribution(pixels)

        assert 'balance' in lsb_analysis
        assert 'p_value' in lsb_analysis
        assert 'suspicion_level' in lsb_analysis
        assert 0 <= lsb_analysis['suspicion_level'] <= 100

    def test_analyze_pixel_correlation(self, test_image_rgb):
        """Тест анализа корреляции пикселей"""
        # Создаем изображение с градиентом для корректной корреляции
        from PIL import Image
        import numpy as np
        import os

        # Создаем изображение с естественным градиентом
        img_array = np.zeros((200, 200, 3), dtype=np.uint8)
        for i in range(200):
            for j in range(200):
                img_array[i, j] = [i, j, (i + j) % 256]

        # Создаем временный файл с градиентом
        gradient_img_path = os.path.join(os.path.dirname(test_image_rgb), "gradient_test.png")
        gradient_img = Image.fromarray(img_array)
        gradient_img.save(gradient_img_path)

        with Image.open(gradient_img_path) as img:
            pixels = np.array(img)

        corr_analysis = FileAnalyzer.analyze_pixel_correlation(pixels)

        # Для градиентного изображения корреляция должна быть высокой
        assert corr_analysis['avg_corr'] > 0.5, f"Корреляция {corr_analysis['avg_corr']} должна быть > 0.5"

        # Очищаем временный файл
        os.remove(gradient_img_path)

    def test_analyze_file_for_stego_image(self, test_image_rgb):
        """Тест полного анализа изображения"""
        results = FileAnalyzer.analyze_file_for_stego(test_image_rgb)

        assert results['status'] == 'success'
        assert 'file_info' in results
        assert 'tests' in results
        assert 'overall_suspicion' in results
        assert 0 <= results['overall_suspicion'] <= 100
        assert 'confidence' in results
        assert 'recommendations' in results

    def test_analyze_file_for_stego_wav(self, test_wav_file):
        """Тест полного анализа WAV файла"""
        results = FileAnalyzer.analyze_file_for_stego(test_wav_file)

        assert results['status'] == 'success'
        assert 'file_info' in results
        assert 'tests' in results

    def test_block_entropy_analysis(self, test_image_rgb):
        """Тест анализа энтропии по блокам"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        block_entropy = FileAnalyzer.calculate_block_entropy(pixels)

        assert 'mean_entropy' in block_entropy
        assert 'std_entropy' in block_entropy
        assert 'block_count' in block_entropy
        assert block_entropy['block_count'] > 0

    def test_histogram_analysis(self, test_image_rgb):
        """Тест гистограммного анализа"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        histogram = FileAnalyzer.analyze_histogram(pixels)

        assert 'histogram' in histogram
        assert 'smoothness' in histogram
        assert len(histogram['histogram']) == 256

    def test_noise_pattern_analysis(self, test_image_rgb):
        """Тест анализа шумового паттерна"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        noise = FileAnalyzer.analyze_noise_pattern(pixels)

        assert 'std_deviation' in noise
        assert 'mean' in noise
        assert 'skewness' in noise
        assert 'kurtosis' in noise

    def test_gradient_statistics(self, test_image_rgb):
        """Тест статистики градиентов"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        gradient = FileAnalyzer.analyze_gradient_statistics(pixels)

        assert 'gradient_mean' in gradient
        assert 'gradient_std' in gradient
        assert 'suspicion_level' in gradient

    def test_frequency_domain_analysis(self, test_image_rgb):
        """Тест частотного анализа"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        freq = FileAnalyzer.analyze_frequency_domain(pixels)

        assert 'dc_std' in freq
        assert 'hf_mean' in freq
        assert 'hf_std' in freq

    def test_texture_features(self, test_image_rgb):
        """Тест текстурных признаков"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        texture = FileAnalyzer.analyze_texture_features(pixels)

        assert 'contrast_mean' in texture
        assert 'homogeneity_mean' in texture
        assert 'energy_mean' in texture

    def test_pairwise_pixel_statistics(self, test_image_rgb):
        """Тест статистики пар пикселей (метод Кера)"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        pairwise = FileAnalyzer.analyze_pairwise_pixel_statistics(pixels)

        assert 'alpha' in pairwise
        assert 'regularity' in pairwise
        assert 'count_group_a' in pairwise
        assert 'count_group_b' in pairwise

    def test_color_channel_correlation(self, test_image_rgb):
        """Тест корреляции цветовых каналов"""
        with Image.open(test_image_rgb) as img:
            pixels = np.array(img)

        color_corr = FileAnalyzer.analyze_color_channel_correlation(pixels)

        assert 'correlation_r_g' in color_corr
        assert 'correlation_g_b' in color_corr
        assert 'correlation_r_b' in color_corr

    def test_jpeg_artifacts_analysis(self, test_dir):
        """Тест анализа JPEG артефактов"""
        jpg_path = os.path.join(test_dir, "test_artifacts.jpg")
        img = Image.new('RGB', (256, 256), color=(100, 150, 200))
        img.save(jpg_path, format='JPEG', quality=100)

        artifacts = FileAnalyzer.analyze_jpeg_artifacts(jpg_path)

        assert 'artifact_score' in artifacts
        assert 'blockiness' in artifacts
        assert 'quality_estimate' in artifacts

    def test_audio_spectral_analysis(self, test_wav_file):
        """Тест спектрального анализа аудио"""
        spectral = FileAnalyzer.analyze_audio_spectral_features(test_wav_file)

        assert 'spectral_centroid_mean' in spectral
        assert 'spectral_flatness_mean' in spectral
        assert 'zero_crossing_rate' in spectral

    def test_export_report_html(self, test_image_rgb, test_dir):
        """Тест экспорта HTML отчета"""
        results = FileAnalyzer.analyze_file_for_stego(test_image_rgb)
        html_path = os.path.join(test_dir, "report.html")

        success = FileAnalyzer.export_report_html(
            results=results,
            output_path=html_path,
            original_file_path=test_image_rgb
        )

        assert success is True
        assert os.path.exists(html_path)

        # Проверка что файл содержит HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '<!DOCTYPE html>' in content
            assert '<html' in content

    def test_export_report_csv(self, test_image_rgb, test_dir):
        """Тест экспорта CSV отчета"""
        results = FileAnalyzer.analyze_file_for_stego(test_image_rgb)
        csv_path = os.path.join(test_dir, "report.csv")

        success = FileAnalyzer.export_report_csv(
            results=results,
            output_path=csv_path
        )

        assert success is True
        assert os.path.exists(csv_path)

    def test_export_report_txt(self, test_image_rgb, test_dir):
        """Тест экспорта TXT отчета"""
        results = FileAnalyzer.analyze_file_for_stego(test_image_rgb)
        txt_path = os.path.join(test_dir, "report.txt")

        success = FileAnalyzer.export_report_txt(
            results=results,
            output_path=txt_path,
            original_file_path=test_image_rgb
        )

        assert success is True
        assert os.path.exists(txt_path)

    def test_analysis_cancellation(self, test_image_rgb, test_dir):
        """Тест отмены анализа"""
        import threading

        cancel_event = threading.Event()
        cancel_event.set()  # Устанавливаем отмену сразу

        results = FileAnalyzer.analyze_file_for_stego(
            test_image_rgb,
            cancel_event=cancel_event
        )

        assert results['status'] == 'cancelled'
