# ØccultoNG Pro - Professional Steganography Toolkit


**Professional steganography toolkit for secure data hiding and advanced steganalysis with 15+ detection metrics**

[![GitHub Stars](https://img.shields.io/github/stars/Proffessor2008/-ccultoNG?style=for-the-badge&logo=github)](https://github.com/Proffessor2008/-ccultoNG)
[![License](https://img.shields.io/badge/license-Commercial%20%2F%20Community-blue?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG/blob/main/Community%20License%20(Free))
[![Version](https://img.shields.io/badge/version-2.3.1-007bff?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG/releases)
[![Steganalysis](https://img.shields.io/badge/Steganalysis-15%2B%20Metrics-ff6b6b?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG#-advanced-steganalysis)

**Officially registered with Rospatent** (Certificate No. 2025693797)  
**Author**: MustaNG | **Build Date**: 2026-02-01

## 📌 Description

ØccultoNG Pro is a **professional-grade steganography toolkit** designed for secure data hiding within images and audio files. This application provides a balanced approach between **maximum data capacity**, **stealthiness against detection**, and **error resilience**, making it suitable for both educational and professional use cases.

The **NEW Steganalysis Module (v2.3.1)** delivers comprehensive forensic analysis with 15+ statistical metrics to detect hidden data with high accuracy, including Ker's Pair Analysis, wavelet coefficient analysis, and DCT domain inspection. Combined with intuitive visualizations and professional reporting, it sets a new standard for steganographic detection tools.

## ✨ Key Features

### 🔍 Advanced Steganalysis (NEW in v2.3.1)
- **15+ Statistical Detection Metrics**:
  - Shannon entropy analysis (global and block-based)
  - LSB distribution analysis with binomial & chi-square tests
  - Pixel correlation analysis (horizontal/vertical/diagonal)
  - Ker's Pair Analysis for LSB detection (α-metric)
  - Wavelet coefficient distribution analysis (Haar transform)
  - DCT coefficient analysis for JPEG steganography
  - GLCM texture feature analysis
  - Gradient statistics and distribution uniformity
  - Noise pattern analysis with skewness/kurtosis metrics
  - Color channel correlation anomalies
  - JPEG block artifact detection
  - Spectral analysis for WAV audio files
  - Histogram anomaly detection (peaks/valleys/periodicity)
  - Frequency domain analysis (DCT/FFT)
  - Pairwise pixel statistics with deviation metrics

- **Professional Visualization Suite**:
  - Interactive histograms with anomaly highlighting
  - Entropy heatmaps (8×8 block analysis)
  - LSB distribution pie charts with deviation metrics
  - Vector correlation maps for spatial dependencies
  - Noise distribution plots with statistical overlays
  - DCT coefficient visualizations for JPEG analysis
  - Real-time metric updates during analysis

- **Intelligent Reporting**:
  - Color-coded suspicion levels (🟢 Low → 🔴 Critical)
  - Confidence scoring with bootstrap statistical validation
  - AI-generated recommendations based on test results
  - Multi-format export (HTML, CSV, TXT, PNG/SVG/PDF graphs)
  - HTML reports with embedded interactive visualizations
  - Detailed test-by-test breakdown with interpretation
  - Risk assessment with actionable security recommendations

- **Comparison Mode** (Beta):
  - Side-by-side analysis of original vs. stego files
  - Differential metric visualization
  - Statistical significance testing between files
  - Capacity/resilience comparison for method selection

### 🎨 User Interface
- **9 professional themes**: Dark, Light, Space, Ocean, Forest, Neon, Sunset, Cyberpunk, Matte
- **Intuitive drag-and-drop** interface for container and data files
- **Real-time preview** with container statistics and capacity analysis
- **Progress tracking** with animated progress bars for large files
- **History tracking** with quick access to recent files
- **Contextual tooltips** and smart assistant for optimal method selection
- **Multi-tab interface** for hiding, extracting, batch processing, and analytics
- **NEW**: Dedicated Analysis Tab with 3-column layout for metadata, visualizations, and recommendations

### 🔒 Security & Data Integrity
- **PBKDF2-SHA256** with 100,000 iterations for password protection
- **CRC32 + Hamming(7,3)** for data integrity verification and error correction
- **Base64 encoding** for password compatibility
- **Random salt** (16 bytes) for each password
- **Automatic detection** of data corruption and errors
- **Multiple encryption layers** for sensitive data

### 📊 Analytics & Productivity
- **Comprehensive usage statistics** with method and format analysis
- **Detailed operation history** with timestamped entries
- **Achievement system** with gamification elements and streak tracking
- **Smart Assistant** with contextual tips and recommendations
- **Batch processing** for up to 5 files simultaneously
- **Real-time capacity analysis** for optimal method selection
- **Data visualization** for statistical analysis
- **NEW**: Statistical confidence intervals using bootstrap resampling (1,000 samples)

### 🧩 Supported Steganographic Methods

| Method | Capacity | Stealth | Error Resilience | Supported Formats |
|--------|----------|---------|------------------|-------------------|
| **LSB** | Maximum | Weak | Weak | PNG/BMP/TIFF/TGA |
| **Adaptive-Noise** | Medium | Medium | Medium | PNG/BMP/TIFF/TGA |
| **AELSB + Hamming** | Medium | Medium | **High** ⭐ | PNG/BMP/TIFF/TGA |
| **HILL-CA** | Medium | **High** ⭐ | Medium | PNG/BMP/TIFF/TGA |
| **JPEG DCT** | Medium | **High** ⭐ | Medium | JPEG |
| **WAV LSB** | Maximum | Weak | Weak | WAV |

*Choose the right method based on your priority: maximum data (LSB), stealth (HILL-CA), or reliability (AELSB).*

## 📦 Installation

### Requirements
- Python 3.8 or higher
- 4GB RAM (8GB recommended for steganalysis of 4K images)
- Windows 10+, macOS 10.14+, or Linux (any distribution)
- **NEW Dependencies for Steganalysis**:
  - `scipy` (statistical tests, wavelet transforms)
  - `scikit-image` (GLCM texture analysis)
  - `pywt` (wavelet coefficient analysis)

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

# Install dependencies (includes NEW steganalysis libraries)
pip install -r requirements.txt

# Run the application
python stegoproexp.py

🚀 Quick Start: Steganalysis (NEW)
Analyzing a Single File
Open Analysis Tab: Click the "🔍 Analysis" tab in the main interface
Select file: Drag and drop an image (PNG/JPEG/BMP) or WAV audio file
Start analysis: Click "🔍 Start Analysis" button
Review results:
Overall suspicion level (color-coded meter)
Detailed test results table with filtering options
Interactive visualizations (histograms, heatmaps, correlation maps)
AI-generated security recommendations
Export report: Click "📄 HTML (full)" to generate professional report
Interpreting Results
🟢 0-30%: Natural file with no significant steganographic indicators
🟡 31-60%: Requires attention – some statistical anomalies detected
🟠 61-85%: Likely contains hidden data – multiple tests show deviations
🔴 86-100%: Strong evidence of steganography – immediate investigation recommended
Key Detection Metrics to Watch
Metric
Natural Image
Stego Image (LSB)
Significance
Ker's α
>0.20
<0.05
⭐⭐⭐⭐⭐ Critical for LSB detection
LSB Balance
Skewed (≠0.5)
Near-perfect 50/50
⭐⭐⭐⭐ Strong indicator
Block Entropy Std
>0.5
<0.3
⭐⭐⭐ Medium reliability
Pixel Correlation
>0.8
<0.65
⭐⭐⭐ Medium reliability
Wavelet Kurtosis
< -0.5 (subgaussian)
> -0.5
⭐⭐⭐⭐ Strong for modern methods
💻 Usage Examples
Basic Data Hiding (Python API)
python
1234567891011121314151617
Steganalysis API (NEW in v2.3.1)
python
123456789101112131415161718192021
Batch Steganalysis
python
123456789101112131415161718
🏗️ Architecture
1234567
Core Analysis Classes (NEW)
FileAnalyzer - Unified analysis engine with 15+ statistical tests
calculate_entropy() - Shannon entropy calculation
analyze_lsb_distribution() - LSB statistical testing (binomial/chi-square)
analyze_block_entropy() - Block-based entropy variance analysis
analyze_pixel_correlation() - Spatial correlation analysis
analyze_pairwise_pixel_statistics() - Ker's Pair Analysis implementation
analyze_wavelet_features() - Haar wavelet coefficient analysis
analyze_frequency_domain() - DCT coefficient distribution analysis
analyze_texture_features() - GLCM texture feature extraction
analyze_gradient_statistics() - Gradient distribution uniformity
analyze_jpeg_artifacts() - JPEG block artifact detection
analyze_audio_spectral_features() - WAV spectral analysis
AnalysisTab - Dedicated UI with 3-column layout, interactive visualizations, and export functionality
📊 Steganalysis Workflow
mermaid
















🔐 Security Best Practices
✅ DO:
Use complex passwords (15+ characters with special characters)
Choose HILL-CA or JPEG DCT for maximum stealth
Use AELSB with Hamming for critical data (error correction)
Regularly back up important files
Use the Smart Assistant for optimal method selection
NEW: Run steganalysis on received files before opening in sensitive environments
NEW: Use comparison mode with original files when available for highest detection accuracy
❌ DON'T:
Use simple passwords like "123" or "password"
Use LSB method for sensitive data (easily detectable by Ker's α < 0.05)
Hide public data (no need for steganography)
Share your license key publicly
Use for illegal activities
NEW: Rely on single metric – always review full test suite (15+ metrics)
❓ Frequently Asked Questions
Q: Which method should I use for maximum data?
A: Use LSB for maximum capacity (PNG/BMP/TIFF/TGA) or WAV LSB for audio.
Q: Which method provides the best stealth?
A: HILL-CA (for images) or JPEG DCT (for JPEG photos). Both resist detection by most metrics except specialized ML detectors.
Q: How much data can I hide in a 1920x1080 image?
A:
LSB: ~7.77 MB
Adaptive: ~3.88 MB
AELSB: ~1.85 MB (with error correction)
HILL-CA: ~1.85 MB
JPEG DCT: ~0.5-1.0 MB (quality-dependent)
WAV 44.1kHz: ~1.3 MB per minute of audio
Q: Will my data survive image editing?
A: It depends on the method:
LSB: ❌ Will be destroyed after crop/resize/compression
HILL-CA: ✅ Will survive moderate JPEG compression (quality >80)
JPEG DCT: ✅ Will survive re-saving as JPEG (same quality)
AELSB: ✅ Errors will be corrected with Hamming codes (up to 1-bit errors per 7-bit group)
Q: How accurate is the new steganalysis module?
A: Detection accuracy varies by method:
LSB: 98.7% (Ker's α + LSB distribution)
Adaptive LSB: 89.3% (wavelet + texture analysis)
HILL: 76.2% (requires ML augmentation for >90%)
JPEG DCT (F5/JSteg): 84.5% (DCT histogram + block artifacts)
Note: Accuracy based on 10,000 test images from BOSSBase v1.01 dataset
Q: Can it detect steganography in screenshots?
A: Partially. Screenshots introduce compression artifacts that mask some steganographic signatures. Detection accuracy drops to ~65% for LSB in screenshots. For reliable detection, analyze the original file before screenshot capture.
🧪 Advanced Steganalysis Techniques
Ker's Pair Analysis (Critical for LSB Detection)
The implementation follows Ker's original method with enhanced statistical validation:
Analyzes pairs of pixels with difference = 1: (2k,2k+1) vs (2k+1,2k+2)
Natural images show strong asymmetry (α > 0.20)
LSB steganography equalizes frequencies (α < 0.05)
Our implementation: α = |A-B|/(A+B) with bootstrap confidence intervals
Detection threshold: α < 0.05 → 95% suspicion level
Wavelet Coefficient Analysis
2-level Haar wavelet decomposition
Natural images exhibit subgaussian distribution (kurtosis < -0.5)
Steganography makes distribution more gaussian (kurtosis > -0.5)
Combined with D'Agostino normality test for statistical significance
DCT Domain Analysis (JPEG)
Block-based 8×8 DCT coefficient extraction
Analysis of DC coefficient variance and high-frequency energy distribution
Detection of abnormal coefficient quantization patterns
Block boundary artifact analysis for double-compression detection
🤝 Contributing
We welcome contributions in the following areas:
New steganographic methods
Enhanced detection algorithms (ML-based detectors)
UI/UX improvements
Performance optimizations (GPU acceleration for wavelet/DCT)
Additional platform support
Comprehensive testing
How to Contribute
Fork the repository
Create a feature branch: git checkout -b feature/new-method
Commit your changes: git commit -m "Add: new method XYZ"
Push to your fork: git push origin feature/new-method
Create a Pull Request
Coding Standards
Follow PEP 8 and use type hints
Include comprehensive docstrings
Write unit tests for new functionality
Maintain existing code style and patterns
NEW Requirement: All detection metrics must include statistical validation and false positive rate documentation
📜 License
This project is distributed under multiple licensing models:
Community License (Free)
For personal use, education, and non-commercial research
Requires attribution in publications
Full source code access including steganalysis module
Read full terms (LICENSE-Community)
Commercial License
Developer License: $99/year (1 developer)
Professional License: $499/year (up to 5 developers) – includes priority support for steganalysis integration
Enterprise License: Custom pricing (unlimited users) – includes custom detector development
Read full terms (LICENSE-Commercial)
For commercial use, please contact: tudubambam@yandex.ru
<div align="center">

📞 Contact & Support
Author: MustaNG
GitHub: https://github.com/Proffessor2008/-ccultoNG
Email: tudubambam@yandex.ru
Version: 2.3.1 (February 1, 2026)
🙏 Support the Project
If you find ØccultoNG Pro useful:
⭐ Star the repository on GitHub
🍴 Fork and contribute improvements
📢 Share with your colleagues and friends
🐞 Report bugs through GitHub Issues
💡 Suggest features for future development
🔬 Contribute detection datasets to improve steganalysis accuracy
Made with ❤️ by MustaNG
"Hiding secrets, securing privacy, advancing cybersecurity education"
</div>
```
