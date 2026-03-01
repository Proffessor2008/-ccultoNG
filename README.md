# ØccultoNG Pro - Professional Steganography Toolkit

**Professional steganography toolkit for secure data hiding in images and audio with advanced methods, comprehensive analytics, and integrated InfoSec utilities**

[![GitHub Stars](https://img.shields.io/github/stars/Proffessor2008/-ccultoNG?style=for-the-badge&logo=github)](https://github.com/Proffessor2008/-ccultoNG)
[![License](https://img.shields.io/badge/license-Commercial%20%2F%20Community-blue?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG/blob/main/Community%20License%20(Free))
[![Version](https://img.shields.io/badge/version-2.6.1-007bff?style=for-the-badge)](https://github.com/Proffessor2008/-ccultoNG/releases)

**Officially registered with Rospatent** (Certificate No. 2025693797)  
**Author**: MustaNG | **Build Date**: 2026-02-28

## 📌 Description

ØccultoNG Pro is a **professional-grade steganography toolkit** designed for secure data hiding within images and audio files. This application provides a balanced approach between **maximum data capacity**, **stealthiness against detection**, and **error resilience**, making it suitable for both educational and professional use cases.

The tool features a **modern UI** with drag-and-drop functionality, real-time analytics, and multiple advanced steganographic methods to suit various security requirements. It includes comprehensive **integrity verification** (CRC32 + Hamming codes) and **password protection** (PBKDF2-SHA256) for secure data hiding.

**NEW in v2.5.1**: Integrated **InfoSec Tools** module with hash calculators, password generators, file signature validators, encoding converters, and professional metadata extraction for digital forensics workflows.

Advanced steganalysis module with 15+ statistical tests for detecting hidden data in images and audio files, complete with interactive visualizations and professional reporting.

## Why ØccultoNG Pro?

| Feature | Your Current Tool | ØccultoNG Pro |
|---------|-------------------|---------------|
| **Formats** | PNG/JPG only | PNG/BMP/TIFF/TGA/JPG/WAV |
| **Stego Methods** | LSB only | 6+ advanced (HILL, DCT, AELSB) |
| **Steganalysis** | ❌ None | **15+ tests** w/ visualizations |
| **Encryption** | ❌ None | **AES-256 GCM** + ChaCha20 |
| **InfoSec Tools** | ❌ None | **Hash/Password/Signatures/Metadata** |
| **Reports** | ❌ None | HTML/CSV w/ graphs |
| **UI** | CLI/Basic GUI | **Modern 9-theme GUI** + drag-drop |
| **API** | ❌ None | **Full Python API** + batch |
| **Price** | Free (limited) | Free / **$99/year** commercial |

**TL;DR:** Professional forensics-grade stego toolkit with GUI, analytics, encryption, and InfoSec utilities. Free for education, $99/year for commercial.

## ✨ Key Features

### 🎨 User Interface
- **9 professional themes**: Dark, Light, Space, Ocean, Forest, Neon, Sunset, Cyberpunk, Matte
- **Intuitive drag-and-drop** interface for container and data files
- **Real-time preview** with container statistics and capacity analysis
- **Progress tracking** with animated progress bars for large files
- **History tracking** with quick access to recent files
- **Contextual tooltips** for optimal method selection
- **Multi-tab interface** for hiding, extracting, batch processing, analytics, encryption, and **InfoSec tools**

### 🔒 Security & Data Integrity
- **PBKDF2-SHA256** with 100,000 iterations for password protection
- **CRC32 + Hamming(7,3)** for data integrity verification and error correction
- **Base64 encoding** for password compatibility
- **Random salt** (16 bytes) for each password
- **Automatic detection** of data corruption and errors
- **Multiple encryption layers** for sensitive data

### 🔍 Advanced Steganalysis
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

### 🔐 Advanced Encryption Module
- **7 cryptographic algorithms**: AES-256 GCM/CBC/CTR/OFB, ChaCha20-Poly1305, ChaCha20, XOR (educational), Base64
- **PBKDF2-HMAC-SHA256** with 600,000 iterations for key derivation
- **Proprietary .ongcrypt format** with automatic detection and metadata
- **Memory-safe key handling** with zeroization after use
- **Dual-layer security**: Encrypt data first, then hide via steganography

# 🛡️ InfoSec Tools Module (UPDATED in v2.6.1)

> **NEW in v2.6.1**: Major expansion of the InfoSec Tools module with **8 new professional utilities**, enhanced existing tools, and improved workflow integration for digital forensics, incident response, and security auditing.

A comprehensive suite of **13 independent utilities** for information security professionals, digital forensics analysts, and cybersecurity specialists. All tools work **completely offline** with no external API dependencies, ensuring data privacy and operational security.

---

## 🆕 What's New in v2.6.1

### 🔹 New Tools Added

| Tool | Purpose | Key Benefit |
|------|---------|-------------|
| **📊 Entropy Analyzer** | Detect encrypted, compressed, or random data in files | Identify hidden payloads, steganography containers, or packed malware without deep reverse engineering |
| **🔤 String Extractor** | Find readable text patterns in binary files (executables, memory dumps, network captures) | Quickly locate URLs, IPs, credentials, or suspicious strings during incident investigation |
| **🔎 Steganoanalysis** | Detect hidden data in images using statistical methods (Chi-square, RS-analysis, LSB plane analysis) | Verify if an image contains steganographic content before further analysis |
| **💾 PE Analyzer** | Inspect Windows executable headers (DOS, PE, sections, imports) | Rapid triage of suspicious EXE/DLL files without running them |
| **📦 Archive Analyzer** | View contents of ZIP/TAR archives without extraction | Safely audit email attachments or downloaded archives for malicious payloads |
| **🆔 UUID/GUID Generator** | Generate RFC 4122 compliant unique identifiers (v1, v3, v4, v5) | Create secure IDs for logging, session tokens, or database keys |
| **⏱️ Unix Time Converter** | Convert between Unix timestamps and human-readable dates across timezones | Correlate events from logs, filesystems, and network captures with different time formats |
| **🌐 IP/Domain Validator** | Validate and convert IP addresses (IPv4/IPv6) and domain names | Clean and verify IOC lists, firewall rules, or threat intelligence feeds |

### 🔹 Enhanced Existing Tools

#### 🔐 Hash Calculator - Now with Professional Features
```
✅ 11 algorithms: MD5, SHA-1, SHA-256/512, SHA3-256/512, BLAKE2b/s, RIPEMD160
✅ Batch processing: Hash multiple files or entire folders recursively
✅ Reference comparison: Verify files against published hashes instantly
✅ Export options: JSON, CSV, or TXT reports for audit documentation
✅ History tracking: Review last 1000 hash operations with timestamps
```

**Why it matters**: Critical for verifying software integrity, documenting evidence in forensic cases, and ensuring data hasn't been tampered with during transfer.

#### 🔑 Password Generator - Smarter & More Flexible
```
✅ 4 generation modes: Random, Passphrase, PIN, XKCD-style memorable passwords
✅ Strength evaluation: Real-time entropy calculation + crack time estimation
✅ Custom wordlists: Russian/English word banks for passphrase generation
✅ Export to password managers: KeePass-compatible CSV format
✅ History with filtering: Track generated passwords without storing them insecurely
```

**Why it matters**: Generate cryptographically strong credentials for services, encryption keys, or test accounts - with confidence in their actual security level.

#### 🕵️ File Signature Validator - Deeper Inspection
```
✅ 100+ file format signatures: Images, documents, archives, executables, databases
✅ Deep scanning (carving): Detect embedded files within containers
✅ Structure validation: Check for truncated or malformed file headers
✅ Detailed reporting: HEX signature, MIME type, and risk assessment in one view
```

**Why it matters**: Catch file type spoofing attacks (e.g., malware disguised as PDF) before they reach your system - essential for email security and upload validation.

#### 🔣 Encoding Converter - Broader Format Support
```
✅ 14 encoding operations: Base32/64/85, Hex, URL, HTML, Unicode Escape, and more
✅ File support: Encode/decode entire files, not just text snippets
✅ Auto-detection: Smart recognition of input encoding to prevent errors
✅ Batch mode: Process multiple files with consistent settings
```

**Why it matters**: Decode obfuscated payloads from logs, prepare data for API transmission, or analyze network traffic - all without leaving the application.

#### 🔍 Metadata Extractor - Forensic-Grade Analysis
```
✅ Office document support: Extract author, edit history, and custom properties from DOCX/XLSX/PPTX
✅ Thumbnail extraction: Recover embedded preview images from files
✅ Edit timeline analysis: Track modification history in XMP/IPTC metadata
✅ Hidden data detection: Flag suspicious or stripped metadata fields
✅ Multi-format export: JSON for automation, CSV for spreadsheets, TXT for reports
```

**Why it matters**: Uncover digital provenance, verify document authenticity, or identify privacy leaks in shared files - critical for investigations and compliance.

---

## 🎯 How to Use InfoSec Tools (Quick Start)

### General Workflow
```
1. Open the "🛡️ InfoSec Tools" tab in the main interface
2. Select the tool you need from the categorized notebook:
   • 🔐 Cryptography (Hash, Password, UUID)
   • 🔬 File Analysis (Signatures, Entropy, Strings, PE, Archives)
   • 🔄 Data & Encoding (Converter, Metadata, Time)
   • 🌐 Network Tools (IP/Domain, Steganoanalysis)
3. Follow the tool-specific interface:
   • Drag-and-drop files where supported
   • Configure options via checkboxes, sliders, or dropdowns
   • Click the primary action button (🚀 / 🔍 / 🎲)
4. Review results in the formatted output area
5. Export, copy, or save results as needed
```

### Practical Examples

#### 🔐 Verify a Downloaded File
```
Scenario: You downloaded "security_tool.exe" and want to confirm it matches the vendor's published SHA-256 hash.

1. Go to "🔐 Hash Calculator"
2. Click "📂 Add Files" and select security_tool.exe
3. Ensure SHA-256 is checked in algorithm list
4. Paste the vendor's hash into "Reference hash" field
5. Click "🔍 Compare"
6. Result: ✅ "MATCH" = file is authentic | ❌ "NO MATCH" = file may be tampered
```

#### 🔍 Investigate a Suspicious Image
```
Scenario: An employee received "invoice.png" from an unknown sender.

1. Go to "🔎 Steganoanalysis"
2. Drag the image into the analysis area
3. Enable Chi-square + RS-analysis + Visual LSB checks
4. Click "🔍 Start Analysis"
5. Review results:
   • Chi-square p-value < 0.05 → possible hidden data
   • RS-analysis asymmetry → LSB manipulation detected
   • LSB entropy ≈ 1.0 → random-looking bit plane (suspicious)
6. If suspicious: quarantine file and run full antivirus scan
```

#### 📊 Analyze a Binary File for Hidden Strings
```
Scenario: You have a memory dump and need to find embedded URLs or credentials.

1. Go to "🔤 String Extractor"
2. Load the binary file
3. Set minimum string length to 6 (filters noise)
4. Enable ASCII + UTF-16 LE encoding detection
5. Optional: Add regex filter like "https?://\S+" to find URLs only
6. Click "🔍 Extract Strings"
7. Review results table with offset, string, and length
8. Copy suspicious entries for further investigation
```

#### 🕵️ Validate Email Attachments in Bulk
```
Scenario: Audit 50 email attachments for file type spoofing.

1. Go to "🕵️ Signature Validator"
2. Click "📁 Add Folder" and select the attachments directory
3. Enable "Deep scan (carving)" to detect nested payloads
4. Click "🚀 Check All"
5. Review summary:
   • ✅ Green = extension matches signature
   • ❌ Red = mismatch → investigate further
6. Export report to CSV for documentation
```

---

## 💡 Why These Tools Matter

### For Security Professionals
- **Speed**: Perform common forensic tasks in seconds, not minutes
- **Accuracy**: Use cryptographically sound algorithms and statistically validated detection methods
- **Documentation**: Export professional reports for case files, audits, or compliance
- **Safety**: All analysis is read-only and offline - no risk of executing malicious code

### For Developers & DevSecOps
- **Integration**: Copy-paste hashes, UUIDs, or encoded values directly into code/configs
- **Testing**: Generate test credentials, validate input sanitization, or simulate IOC feeds
- **Debugging**: Decode obfuscated logs, inspect binary outputs, or verify timestamp handling

### For Education & Training
- **Hands-on learning**: Experiment with cryptography, encoding, and steganalysis concepts safely
- **Visual feedback**: See entropy graphs, signature hex dumps, and metadata trees in real-time
- **Best practices**: Built-in warnings and recommendations reinforce secure habits

---

## 🔐 Security & Privacy Guarantees

✅ **100% offline operation** - No data leaves your machine  
✅ **No telemetry or analytics** - Your usage is never tracked  
✅ **Read-only analysis** - Files are never modified during inspection  
✅ **Memory-safe handling** - Sensitive data (passwords, keys) is zeroized after use  
✅ **Open algorithms** - All cryptographic methods use well-vetted, standard libraries  

> ℹ️ **Note**: InfoSec Tools are designed to *assist* security workflows - not replace professional judgment. Always corroborate findings with additional tools and expert review.

---

## 🔄 Integration with Core Steganography Features

The InfoSec Tools module complements ØccultoNG Pro's primary steganography functions:

```
🔐 Dual-Layer Security Workflow:
1. Encrypt sensitive data using "🔐 Encryption" tab (AES-256 GCM)
2. Hide the encrypted payload using steganography ("📦 Hide Data" tab)
3. Verify integrity using "🔐 Hash Calculator" (SHA-256 of final stego-file)
4. Document the process using metadata export and report generation

🔍 Forensic Analysis Workflow:
1. Suspect image received → analyze with "🔎 Steganoanalysis"
2. If hidden data suspected → extract with "🔍 Extract Data" tab
3. If extracted data is encrypted → decrypt using "🔐 Encryption" tab
4. Verify final content using hash comparison and metadata review
```

This integrated approach enables end-to-end secure communication and thorough incident investigation - all within a single, cohesive application.

---

### 📊 Analytics & Productivity
- **Comprehensive usage statistics** with method and format analysis
- **Detailed operation history** with timestamped entries
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

### 🔎 Steganalysis Detection Methods

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

### 🔍 Analyzing Files for Hidden Data
1. **Open Analysis tab**: Navigate to the dedicated steganalysis workspace
2. **Select file**: Drag and drop image or audio file to analyze
3. **Start analysis**: Click "Analyze" to run 15+ statistical tests
4. **Review results**: 
   - Check overall suspicion level (0-100%)
   - Examine individual test results with color-coded risk levels
   - View interactive visualizations (histograms, heatmaps, correlation maps)
5. **Export report**: Generate professional HTML/CSV/TXT reports with findings
6. **Compare files** (optional): Load second file to detect subtle differences

### 🔐 Encrypting Sensitive Data
1. **Open Encryption tab**: Navigate to the dedicated encryption workspace (🔐 icon)
2. **Choose data type**: Select "Text" or "File" for encryption
3. **Enter data**: Type text or select file to protect
4. **Select algorithm**: Choose AES-256 GCM (recommended) or ChaCha20-Poly1305
5. **Create strong password**: Use 12+ characters with mixed case, numbers, and symbols
6. **Click "Encrypt"**: Process completes in seconds (depending on data size)
7. **Save encrypted file**: Save as `.ongcrypt` for automatic format recognition
8. **Verify immediately**: Decrypt once to confirm password correctness before storage

> 💡 **Pro Tip**: For maximum security, encrypt data FIRST, then hide the encrypted payload using steganography. This creates dual-layer protection where even if steganalysis detects hidden data, the attacker still faces 256-bit encryption.

### 🛡️ Using InfoSec Tools (NEW in 2.5.1)

#### Hash Calculator Workflow
```
1. Navigate to "🛡️ InfoSec Tools" → "🔐 Hash Sums" tab
2. Option A - File hashing:
   • Click "Browse" and select target file
   • Hashes calculate automatically
   • Click "📋 Copy" next to SHA-256 for verification
3. Option B - Text hashing:
   • Paste text in upper field (Ctrl+V supported)
   • Hashes update in real-time as you type
   • Use "Copy All" to export full hash report
4. Verify downloaded software against published hashes
```

#### Password Generator Workflow
```
1. Navigate to "🛡️ InfoSec Tools" → "🔑 Password Generator"
2. Configure parameters:
   • Set length to 16+ for critical accounts
   • Enable all character sets for maximum entropy
   • Check "Exclude ambiguous" if password will be typed manually
3. Click "🎲 Generate"
4. Review entropy indicator:
   • 🟢 Green (>60 bits): Suitable for banking, email, etc.
   • 🟡 Yellow (40-60 bits): Acceptable for low-risk services
   • 🔴 Red (<40 bits): Increase length or character diversity
5. Click "📋 Copy" and paste into password manager
6. ⚠️ Never reuse generated passwords across services
```

#### Signature Validator Workflow
```
1. Navigate to "🛡️ InfoSec Tools" → "🕵️ Signature Validator"
2. Select suspicious file (e.g., "report.exe" claiming to be PDF)
3. Click "Check Signature"
4. Interpret results:
   ✅ "MATCH: Extension corresponds to signature"
      → File type is genuine, proceed with caution
   ❌ "MISMATCH: Possible extension spoofing!"
      → File may be malicious; quarantine and scan with antivirus
5. For mismatches:
   • Do NOT open the file directly
   • Upload to VirusTotal or similar service
   • Report to security team if in enterprise environment
```

#### Encoding Converter Workflow
```
1. Navigate to "🛡️ InfoSec Tools" → "🔣 Encoding Converter"
2. Paste encoded data in input field
3. Select conversion type:
   • "→ Base64" to decode Base64 strings
   • "→ Hex" to convert hex dumps to binary
   • "→ URL" to decode URL-encoded parameters
4. Click "Convert"
5. Review output:
   • Valid conversions appear in lower field
   • Errors display clear messages (e.g., "Invalid Base64 padding")
6. Copy result for further analysis or use
```

#### Metadata Extractor Workflow
```
1. Navigate to "🛡️ InfoSec Tools" → "🔍 Metadata"
2. Click "Browse..." and select target file
   • Supported: PNG, JPG, BMP, TIFF, WAV, PDF
3. Click "🔍 Extract Metadata"
   • Analysis runs asynchronously; UI remains responsive
   • Progress shown in status bar
4. Review grouped results in TreeView:
   • 📁 File: Basic file information
   • 📷 EXIF: Camera settings, GPS coordinates
   • 🏷️ IPTC: Copyright, author, keywords
   • 🌍 GPS: Latitude/longitude if available
5. Use search filter to find specific fields
6. Right-click any value → "Copy value" or "Copy group"
7. Export complete report:
   • JSON: For programmatic processing
   • CSV: For spreadsheet analysis
   • TXT: For human-readable documentation
```

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

### 🔍 Steganalysis API
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

### 🛡️ InfoSec Tools API Examples

#### Hash Calculation
```python
import hashlib

# Calculate SHA-256 for file verification
def verify_file(filepath, expected_hash):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_hash

# Usage
if verify_file("downloaded_app.exe", "a1b2c3..."):
    print("✅ File integrity verified")
else:
    print("❌ File may be corrupted or tampered")
```

#### Password Generation
```python
import secrets
import string

def generate_password(length=16, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# Generate strong password
pwd = generate_password(20)
print(f"Generated: {pwd}")
# Example output: J7$mP9#kL2@nQ5vX!R8t
```

#### File Signature Check
```python
def check_file_signature(filepath):
    """Check if file extension matches magic bytes"""
    signatures = {
        b'\x89PNG\r\n\x1a\n': '.png',
        b'\xff\xd8\xff': '.jpg',
        b'%PDF': '.pdf',
        b'PK\x03\x04': '.zip',
        b'MZ': '.exe',
    }
    with open(filepath, 'rb') as f:
        header = f.read(16)
    for sig, ext in signatures.items():
        if header.startswith(sig):
            return ext
    return None

# Detect spoofed file
detected = check_file_signature("suspicious.jpg")
if detected != ".jpg":
    print(f"⚠️ Warning: File signature indicates {detected}, not .jpg")
```

#### Metadata Extraction (Images)
```python
from PIL import Image
from PIL.ExifTags import TAGS

def extract_image_metadata(filepath):
    """Extract EXIF metadata from image"""
    metadata = {}
    with Image.open(filepath) as img:
        exif = img.getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = value
    return metadata

# Usage
meta = extract_image_metadata("photo.jpg")
if 'GPSLatitude' in meta:
    print(f"📍 Location: {meta['GPSLatitude']}")
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
├── ib_tools.py            # InfoSec Tools module (NEW in 2.5.1)
└── analysis/
    ├── file_analyzer.py    # Core steganalysis engine (15+ tests)
    └── visualization.py    # Interactive plot generation
```

### Core Classes
- `AdvancedStego` - Core steganographic methods (LSB, Noise, AELSB, HILL)
- `JPEGStego` - JPEG DCT method implementation
- `AudioStego` - WAV LSB method
- `ImageProcessor` - Image handling and analysis
- `FileAnalyzer` - Comprehensive steganalysis engine with 15+ statistical tests
- `AnalysisTab` - UI interface for steganalysis with visualizations
- `IBToolsTab` - **NEW**: InfoSec utilities (hash, password, signatures, encoding, metadata)
- `EncryptionManager` - Cryptographic operations module
- `ThemeManager` - UI theme management
- `HistoryLog` - Operation history tracking
- `NotificationManager` - User notifications
- `AnalyticsManager` - Usage statistics

## 🧪 Advanced Features

### Batch Processing
- Process up to 5 files simultaneously
- Analyze capacity and method suitability
- Export detailed processing reports
- Save results automatically
- Monitor progress with real-time updates

### 🔍 Steganalysis Deep Dive
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
- **Ker's Pair Analysis** for robust LSB detection (α-metric < 0.05 indicates steganography)

### 🔐 Encryption Integration
- Encrypt data before steganographic hiding for dual-layer security
- Support for modern AEAD ciphers (AES-GCM, ChaCha20-Poly1305)
- Memory-safe key handling with automatic zeroization
- Proprietary `.ongcrypt` format for reliable file identification

### 🛡️ InfoSec Tools Integration
- All tools operate offline with no external dependencies
- Async processing prevents UI blocking during analysis
- Smart caching reduces redundant computations
- Professional export formats for forensic documentation
- Context-aware error handling with actionable guidance

## 🔐 Security Best Practices

### ✅ DO:
- Use complex passwords (15+ characters with special characters)
- Choose HILL-CA or JPEG DCT for maximum stealth
- Use AELSB with Hamming for critical data (error correction)
- Regularly back up important files
- **Run steganalysis on suspicious files before opening/processing**
- **Compare files with known originals when possible (use comparison mode)**
- **Verify file signatures before executing downloaded files**
- **Use hash verification for software integrity checks**
- **Encrypt sensitive data before steganographic hiding**

### ❌ DON'T:
- Use simple passwords like "123" or "password"
- Use LSB method for sensitive data (easily detectable by modern steganalysis)
- Hide public data (no need for steganography)
- Share your license key publicly
- Use for illegal activities
- **Rely on single-test steganalysis results** - always review comprehensive analysis
- **Open files with mismatched signatures** without antivirus scanning
- **Reuse passwords** across different encryption operations
- **Store passwords** in the same location as encrypted files

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
- **Note**: No steganalysis tool is 100% accurate - always combine with other verification methods

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

**Q: 🔐 Should I encrypt data before or after steganographic hiding?**  
A: **ALWAYS encrypt BEFORE hiding**. This creates dual-layer security:
1. Steganography hides the *existence* of data
2. Encryption protects the *content* if hiding is detected  
Even if an attacker detects hidden data via steganalysis, they still face 256-bit encryption without the password.

**Q: 🔐 What's the difference between XOR and real encryption?**  
A: XOR is a **bitwise operation**, not encryption:
- XOR with same key twice = original data (trivially reversible)
- No key derivation, no salt, no authentication
- Vulnerable to known-plaintext attacks
- Included ONLY for educational demonstrations  
**Never use XOR for real data protection.** Always use AES-256 GCM or ChaCha20-Poly1305.

**Q: 🔐 How strong should my encryption password be?**  
A: Minimum requirements:
- **Absolute minimum**: 12 characters with mixed case + numbers + symbols
- **Recommended**: 16+ characters with all character types
- **Ideal**: 20+ characters generated by password manager  
Example of strong password: `J7$mP9#kL2@nQ5vX!R8*tY3`  
Weak password example (avoid): `Password123` - crackable in hours.

**Q: 🔐 What happens if I forget my encryption password?**  
A: **Data is permanently lost**. Modern encryption (AES-256) is designed to be mathematically impossible to break without the key. There is no backdoor, no master key, and no recovery mechanism. Always:
1. Verify decryption immediately after encryption
2. Store password in a secure password manager
3. Create backup copies of critical passwords in secure locations

**Q: 🔐 Can I use the same password for multiple files?**  
A: **Technically yes, but strongly discouraged**. Using unique passwords per file:
- Prevents compromise of all files if one password is leaked
- Limits blast radius of password reuse attacks
- Follows zero-trust security principles  
Use a password manager to generate and store unique passwords for each encryption operation.

**Q: 🛡️ Are InfoSec Tools safe to use on sensitive files?**  
A: **Yes, completely safe**:
- All tools run locally with no network communication
- No data is transmitted to external servers
- Metadata extraction is read-only (no file modification)
- Hash calculations use standard cryptographic libraries
- Password generation uses `secrets` module (cryptographically secure RNG)

**Q: 🛡️ Can I automate InfoSec Tools via script?**  
A: The tools are designed for GUI use, but core functionality is accessible via Python imports:
```python
# Example: Programmatic hash calculation
import hashlib
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```
For full automation, consider using the underlying libraries directly (`hashlib`, `Pillow`, etc.).

## 🤝 Contributing

We welcome contributions in the following areas:

- **New steganographic methods**
- **Advanced steganalysis techniques**
- **InfoSec Tools enhancements** (new hash algorithms, metadata parsers, etc.)
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
- **For InfoSec Tools**: Ensure offline operation and clear error messaging

## 📜 License

This project is distributed under multiple licensing models:

### Community License (Free)
- For personal use, education, and non-commercial research
- Requires attribution in publications
- Full source code access
- Read full terms ([LICENSE-Community](https://github.com/Proffessor2008/-ccultoNG/blob/main/Community%20License%20(Free)))

### Commercial License
- **Developer License**: $99/year (1 developer)
- **Professional License**: $1000/year (up to 5 developers)
- **Enterprise License**: Custom pricing (unlimited users + priority support)
- Read full terms ([LICENSE-Commercial](https://github.com/Proffessor2008/-ccultoNG/blob/main/Commercial%20License%20(Paid)))

For commercial use, please contact: **tudubambam@yandex.ru**

<div align="center">

## 📞 Contact & Support

**Author**: MustaNG  
**GitHub**: [https://github.com/Proffessor2008/-ccultoNG](https://github.com/Proffessor2008/-ccultoNG)  
**Email**: tudubambam@yandex.ru  
**Version**: 2.5.1 (February 28, 2026)

## 🙏 Support the Project

If you find ØccultoNG Pro useful:

- ⭐ **Star** the repository on GitHub
- 🍴 **Fork** and contribute improvements
- 📢 **Share** with your colleagues and friends
- 🐞 **Report bugs** through GitHub Issues
- 💡 **Suggest features** for future development (especially new steganalysis techniques or InfoSec tools!)

---
**Made with ❤️ by MustaNG**  
*"Hiding secrets, securing privacy, advancing cybersecurity education"*
</div>
