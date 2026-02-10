# ØccultoNG Pro - Professional Steganography Toolkit

**Professional steganography toolkit for secure data hiding in images and audio with advanced methods and comprehensive analytics**

[![GitHub Stars](https://img.shields.io/github/stars/Proffessor2008/-ccultoNG?style=for-the-badge&logo=github)](https://github.com/Proffessor2008/-ccultoNG)
[![License](https://img.shields.io/badge/license-Commercial%20%2F%20Community-blue?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG/blob/main/Community%20License%20(Free))
[![Version](https://img.shields.io/badge/version-2.3.3-007bff?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG/releases)

**Officially registered with Rospatent** (Certificate No. 2025693797)  
**Author**: MustaNG | **Build Date**: 2026-02-01

## 📌 Description

ØccultoNG Pro is a **professional-grade steganography toolkit** designed for secure data hiding within images and audio files. This application provides a balanced approach between **maximum data capacity**, **stealthiness against detection**, and **error resilience**, making it suitable for both educational and professional use cases.

The tool features a **modern UI** with drag-and-drop functionality, real-time analytics, and multiple advanced steganographic methods to suit various security requirements. It includes comprehensive **integrity verification** (CRC32 + Hamming codes) and **password protection** (PBKDF2-SHA256) for secure data hiding.

**NEW IN 2.3.1**: Advanced steganalysis module with 15+ statistical tests for detecting hidden data in images and audio files, complete with interactive visualizations and professional reporting.

## ✨ Key Features

### 🎨 User Interface
- **9 professional themes**: Dark, Light, Space, Ocean, Forest, Neon, Sunset, Cyberpunk, Matte
- **Intuitive drag-and-drop** interface for container and data files
- **Real-time preview** with container statistics and capacity analysis
- **Progress tracking** with animated progress bars for large files
- **History tracking** with quick access to recent files
- **Contextual tooltips** and smart assistant for optimal method selection
- **Multi-tab interface** for hiding, extracting, batch processing, analytics, and **advanced steganalysis**

### 🔒 Security & Data Integrity
- **PBKDF2-SHA256** with 100,000 iterations for password protection
- **CRC32 + Hamming(7,3)** for data integrity verification and error correction
- **Base64 encoding** for password compatibility
- **Random salt** (16 bytes) for each password
- **Automatic detection** of data corruption and errors
- **Multiple encryption layers** for sensitive data

### 🔍 Advanced Steganalysis (NEW in 2.3.1)
- **15+ statistical detection tests** for comprehensive analysis:
  - Shannon entropy analysis (global and block-based)
  - LSB distribution analysis with binomial and chi-square tests
  - Pixel correlation analysis (horizontal, vertical, diagonal)
  - Noise pattern analysis with skewness/kurtosis metrics
  - Histogram anomaly detection (peaks, valleys, periodicity)
  - Color channel correlation analysis
  - JPEG artifact analysis (blockiness, DCT coefficient distribution)
  - Spectral analysis for WAV audio files
  - Gradient statistics analysis
  - Frequency domain analysis (DCT coefficients)
  - Texture analysis via GLCM (Gray-Level Co-occurrence Matrix)
  - Wavelet coefficient distribution analysis
  - Ker's Pair Analysis for LSB detection (α-metric)
- **Interactive visualizations**:
  - Histogram distribution charts
  - Entropy heatmaps by image blocks
  - Noise distribution plots
  - LSB balance pie charts
  - Pixel correlation vector maps
- **Professional reporting**:
  - HTML reports with embedded visualizations
  - CSV export for statistical analysis
  - TXT summary reports
  - Confidence scoring with bootstrap validation
- **Comparison mode**: Side-by-side analysis of two files to detect subtle differences
- **Smart recommendations**: Context-aware suggestions based on test results

### 📊 Analytics & Productivity
- **Comprehensive usage statistics** with method and format analysis
- **Detailed operation history** with timestamped entries
- **Achievement system** with gamification elements and streak tracking
- **Smart Assistant** with contextual tips and recommendations
- **Batch processing** for up to 5 files simultaneously
- **Real-time capacity analysis** for optimal method selection
- **Data visualization** for statistical analysis

### 🧩 Supported Steganographic Methods

| Method | Capacity | Stealth | Error Resilience | Supported Formats |
|--------|----------|---------|------------------|-------------------|
| **LSB** | Maximum | Weak | Weak | PNG/BMP/TIFF/TGA |
| **Adaptive-Noise** | Medium | Medium | Medium | PNG/BMP/TIFF/TGA |
| **AELSB + Hamming** | Medium | Medium | **High** ⭐ | PNG/BMP/TIFF/TGA |
| **HILL-CA** | Medium | **High** ⭐ | Medium | PNG/BMP/TIFF/TGA |
| **JPEG DCT** | Medium | **High** ⭐ | Medium | JPEG |
| **WAV LSB** | Maximum | Weak | Weak | WAV |

### 🔎 Steganalysis Detection Methods (NEW)

| Test Category | Detection Strength | Best For | Formats |
|---------------|-------------------|----------|---------|
| **Ker's Pair Analysis** | ⭐⭐⭐⭐⭐ | LSB detection | PNG/BMP/TIFF |
| **Block Entropy** | ⭐⭐⭐⭐ | Adaptive methods | All images |
| **LSB Distribution** | ⭐⭐⭐⭐⭐ | LSB methods | All formats |
| **Pixel Correlation** | ⭐⭐⭐⭐ | All spatial methods | PNG/BMP |
| **DCT Analysis** | ⭐⭐⭐⭐⭐ | JPEG steganography | JPEG |
| **Wavelet Analysis** | ⭐⭐⭐ | Advanced methods | PNG/BMP |
| **Texture Analysis (GLCM)** | ⭐⭐⭐ | F5, JSteg | PNG/BMP |
| **Spectral Analysis** | ⭐⭐⭐⭐ | Audio steganography | WAV |

*Detection strength: 5 stars = highest reliability for detecting specific steganographic methods*

## 📦 Installation

### Requirements
- Python 3.8 or higher
- 4GB RAM (for large files and analysis)
- Windows 10+, macOS 10.14+, or Linux (any distribution)
- **Additional dependencies for analysis**: `scipy`, `scikit-image`, `PyWavelets`

### Steps
```bash
# Clone the repository
git clone https://github.com/Proffessor2008/-ccultoNG.git
cd -ccultoNG

# Create and activate virtual environment
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies (including analysis modules)
pip install -r requirements.txt

# Run the application
python stegoproexp.py
```

## 🚀 Quick Start

### Hiding Data
1. **Select container**: Drag and drop a PNG/JPEG/WAV file or click to select
2. **Choose data type**: Text or file (up to 100 MB)
3. **Select method**: Choose from the dropdown based on your needs
4. **Click "Hide"**: Select output location and save
5. **Data hidden!**: The file is now secured with hidden data

### Extracting Data
1. **Drop stego-file**: Drag your container with hidden data
2. **Automatic detection**: The tool identifies the correct method
3. **Enter password**: If one was set during hiding
4. **Click "Extract"**: Data is revealed and ready for use
5. **Data extracted!**: Copy, save, or analyze the results

### 🔍 Analyzing Files for Hidden Data (NEW)
1. **Open Analysis tab**: Navigate to the dedicated steganalysis workspace
2. **Select file**: Drag and drop image or audio file to analyze
3. **Start analysis**: Click "Analyze" to run 15+ statistical tests
4. **Review results**: 
   - Check overall suspicion level (0-100%)
   - Examine individual test results with color-coded risk levels
   - View interactive visualizations (histograms, heatmaps, correlation maps)
5. **Export report**: Generate professional HTML/CSV/TXT reports with findings
6. **Compare files** (optional): Load second file to detect subtle differences

## 💻 Usage Examples

### Basic Data Hiding (Python API)
```python
from stegoproexp import AdvancedStego, ImageProcessor

# Hide data in PNG
AdvancedStego.hide_lsb(
    container_path="photo.png",
    data=b"Secret message",
    password="MyPassword123",
    output_path="stego_result.png",
    progress_callback=lambda p: print(f"Progress: {p}%")
)

# Extract data
extracted_data = AdvancedStego.extract_lsb(
    "stego_result.png",
    "MyPassword123"
)
print(extracted_data)  # b"Secret message"
```

### JPEG DCT Method
```python
from stegoproexp import JPEGStego

# Hide data in JPEG
JPEGStego.hide_dct(
    "photo.jpg",
    b"Secret data",
    "password",
    "stego_photo.jpg"
)

# Extract data from JPEG
data = JPEGStego.extract_dct("stego_photo.jpg", "password")
print(data)  # b"Secret data"
```

### 🔍 Steganalysis API (NEW in 2.3.1)
```python
from stegoproexp import FileAnalyzer

# Analyze image for hidden data
results = FileAnalyzer.analyze_file_for_stego("suspect_image.png")

# Get overall suspicion level
print(f"Suspicion level: {results['overall_suspicion']}%")
print(f"Confidence: {results['confidence']:.0f}%")

# Check specific test results
lsb_test = results['tests']['lsb_distribution']
print(f"LSB balance: {lsb_test['value']:.3f}")
print(f"Interpretation: {lsb_test['interpretation']}")

# Export professional HTML report
FileAnalyzer.export_report_html(
    results, 
    "analysis_report.html", 
    "suspect_image.png"
)
```

### Capacity Analysis
```python
from stegoproexp import ImageProcessor

# Calculate capacity for Full HD image
capacity = ImageProcessor.get_capacity_by_method(
    total_pixels=1920*1080*3,
    method="lsb"
)
print(f"LSB Capacity: {capacity} bytes")  # ~7.77 MB
```

## 🏗️ Architecture

```
stegoproexp/
├── stegoproexp.py          # Main application file
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
├── stego_settings_pro.json # User configuration (auto-created)
└── analysis/
    ├── file_analyzer.py    # Core steganalysis engine (15+ tests)
    └── visualization.py    # Interactive plot generation
```

### Core Classes
- `AdvancedStego` - Core steganographic methods (LSB, Noise, AELSB, HILL)
- `JPEGStego` - JPEG DCT method implementation
- `AudioStego` - WAV LSB method
- `ImageProcessor` - Image handling and analysis
- `FileAnalyzer` - **NEW**: Comprehensive steganalysis engine with 15+ statistical tests
- `AnalysisTab` - **NEW**: UI interface for steganalysis with visualizations
- `ThemeManager` - UI theme management
- `HistoryLog` - Operation history tracking
- `SmartAssistant` - Contextual recommendations
- `NotificationManager` - User notifications
- `AchievementManager` - Gamification system
- `AnalyticsManager` - Usage statistics

## 🧪 Advanced Features

### Batch Processing
- Process up to 5 files simultaneously
- Analyze capacity and method suitability
- Export detailed processing reports
- Save results automatically
- Monitor progress with real-time updates

### 🔍 Steganalysis Deep Dive (NEW)
- **Statistical significance testing**: Binomial tests, chi-square, Kolmogorov-Smirnov
- **Multi-scale analysis**: Global metrics + block-based localized analysis
- **Cross-method validation**: Multiple independent tests to reduce false positives
- **Confidence scoring**: Bootstrap validation for result reliability assessment
- **Adaptive thresholds**: Dynamic risk assessment based on file characteristics
- **Artifact detection**: JPEG block boundaries, compression artifacts, noise patterns
- **Audio-specific analysis**: Spectral flatness, zero-crossing rate, MFCC analysis

### Data Analysis
- Statistical tests for hidden data detection
- Histogram analysis for LSB patterns
- Noise pattern analysis for steganalysis
- Entropy analysis for data integrity
- DCT coefficient analysis for JPEG files
- **NEW**: Ker's Pair Analysis for robust LSB detection (α-metric < 0.05 indicates steganography)

### Smart Assistant
- Contextual tips based on current operation
- Method recommendations for optimal results
- Security warnings for potential vulnerabilities
- Capacity analysis for data size planning
- **NEW**: Steganalysis interpretation guidance based on test results
- Learning system that adapts to user preferences

### Achievement System
- 20+ achievements with multiple rarity levels
- Streak tracking (daily usage)
- Experience points and leveling system
- Visual badges for completed achievements
- Detailed statistics and progress tracking

## 🔐 Security Best Practices

### ✅ DO:
- Use complex passwords (15+ characters with special characters)
- Choose HILL-CA or JPEG DCT for maximum stealth
- Use AELSB with Hamming for critical data (error correction)
- Regularly back up important files
- Use the Smart Assistant for optimal method selection
- **NEW**: Run steganalysis on suspicious files before opening/processing
- **NEW**: Compare files with known originals when possible (use comparison mode)

### ❌ DON'T:
- Use simple passwords like "123" or "password"
- Use LSB method for sensitive data (easily detectable by modern steganalysis)
- Hide public data (no need for steganography)
- Share your license key publicly
- Use for illegal activities
- **NEW**: Rely on single-test results—always review comprehensive analysis

## ❓ Frequently Asked Questions

**Q: Which method should I use for maximum data?**  
A: Use **LSB** for maximum capacity (PNG/BMP/TIFF/TGA) or **WAV LSB** for audio.

**Q: Which method provides the best stealth?**  
A: **HILL-CA** (for images) or **JPEG DCT** (for JPEG photos). Both resist modern steganalysis techniques.

**Q: How much data can I hide in a 1920x1080 image?**  
A: 
- LSB: ~7.77 MB
- Adaptive: ~3.88 MB
- AELSB: ~1.85 MB (with error correction)
- HILL-CA: ~1.85 MB
- JPEG DCT: ~0.5-1.0 MB (quality-dependent)
- WAV 44.1kHz: ~1.3 MB per minute of audio

**Q: Will my data survive image editing?**  
A: It depends on the method:
- LSB: ❌ Will be destroyed after crop/resize/compression
- HILL-CA: ✅ Will survive moderate JPEG compression
- JPEG DCT: ✅ Will survive saving as JPEG (within quality limits)
- AELSB: ✅ Errors will be corrected with Hamming codes (limited resilience)

**Q: 🔍 How reliable is the steganalysis module?**  
A: The module uses **15+ independent statistical tests** with cross-validation:
- High confidence (>85% suspicion): Strong indicator of steganography (false positive rate < 5%)
- Medium confidence (55-85%): Requires manual verification or comparison with original
- Low confidence (<40%): Likely clean file, but not guaranteed (advanced methods may evade detection)
- **Note**: No steganalysis tool is 100% accurate—always combine with other verification methods

**Q: 🔍 What does the Ker's Pair Analysis (α-metric) mean?**  
A: This advanced test detects LSB steganography by analyzing pixel pair distributions:
- α < 0.03: **Critical** - Very strong evidence of LSB steganography
- α < 0.05: **High** - Strong evidence (original Ker threshold)
- α < 0.10: **Medium** - Possible steganography
- α > 0.20: **Low** - Natural image characteristics preserved
- Natural images show asymmetry in adjacent pixel pairs; LSB steganography artificially balances these distributions

**Q: 🔍 Can I detect steganography in JPEG files?**  
A: Yes! The tool includes specialized JPEG analysis:
- DCT coefficient histogram analysis
- Block boundary artifact detection
- JPEG quality estimation and recompression detection
- Best detection for F5, JSteg, and OutGuess methods
- Note: Detection is harder in highly compressed JPEGs (>85% quality)

## 🤝 Contributing

We welcome contributions in the following areas:

- **New steganographic methods**
- **Advanced steganalysis techniques**
- **UI/UX improvements**
- **Performance optimizations**
- **Additional platform support**
- **Comprehensive testing**

### How to Contribute
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-method`
3. Commit your changes: `git commit -m "Add: new method XYZ"`
4. Push to your fork: `git push origin feature/new-method`
5. Create a Pull Request

### Coding Standards
- Follow PEP 8 and use type hints
- Include comprehensive docstrings
- Write unit tests for new functionality
- Maintain existing code style and patterns
- **For analysis modules**: Include statistical validation and false positive rate documentation

## 📜 License

This project is distributed under multiple licensing models:

### Community License (Free)
- For personal use, education, and non-commercial research
- Requires attribution in publications
- Full source code access
- Read full terms ([LICENSE-Community](https://github.com/Proffessor2008/-ccultoNG/blob/main/Community%20License%20(Free)))

### Commercial License
- **Developer License**: $99/year (1 developer)
- **Professional License**: $499/year (up to 5 developers)
- **Enterprise License**: Custom pricing (unlimited users + priority support)
- Read full terms ([LICENSE-Commercial](https://github.com/Proffessor2008/-ccultoNG/blob/main/Commercial%20License%20(Paid)))

For commercial use, please contact: **tudubambam@yandex.ru**

<div align="center">

## 📞 Contact & Support

**Author**: MustaNG  
**GitHub**: [https://github.com/Proffessor2008/-ccultoNG](https://github.com/Proffessor2008/-ccultoNG)  
**Email**: tudubambam@yandex.ru  
**Version**: 2.3.1 (February 1, 2026)

## 🙏 Support the Project

If you find ØccultoNG Pro useful:

- ⭐ **Star** the repository on GitHub
- 🍴 **Fork** and contribute improvements
- 📢 **Share** with your colleagues and friends
- 🐞 **Report bugs** through GitHub Issues
- 💡 **Suggest features** for future development (especially new steganalysis techniques!)

---
**Made with ❤️ by MustaNG**  
*"Hiding secrets, securing privacy, advancing cybersecurity education"*
</div>
