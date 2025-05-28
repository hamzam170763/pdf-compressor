# PDF Compressor 📄🗜️

A high-quality Python script that automatically compresses all PDF files in the current directory while preserving text clarity and visual fidelity. The compressed files are saved in a separate directory to keep your workspace organized.

## ✨ Features

- **🎯 Smart Compression**: Automatically detects text-heavy vs image-heavy pages and applies optimal compression strategies
- **📁 Organized Output**: Saves all compressed files in a separate `compressed_pdfs` directory
- **🔤 Text Preservation**: Maintains high text clarity using intelligent DPI scaling and format selection
- **🖼️ Image Optimization**: Optimizes images while preserving visual quality
- **📊 Detailed Reports**: Shows compression ratios, file sizes, and space saved
- **🔄 Dual Methods**: Uses PyMuPDF (primary) with PyPDF2 fallback for maximum compatibility
- **⚡ Batch Processing**: Processes all PDFs in the current directory automatically
- **🛡️ Safe Operations**: Original files remain untouched

## 🚀 Quick Start

### Prerequisites

Install the required Python libraries:

```bash
pip install PyPDF2 PyMuPDF Pillow
```

### Installation

1. Download the `pdf_compressor.py` script
2. Place it in the directory containing your PDF files
3. Run the script:

```bash
python pdf_compressor.py
```

## 📋 Requirements

- **Python 3.6+**
- **PyPDF2**: Basic PDF manipulation and fallback compression
- **PyMuPDF (fitz)**: Advanced PDF processing and high-quality compression
- **Pillow (PIL)**: Image processing and optimization

## ⚙️ Configuration

The script uses optimized default settings that work well for most documents:

| Setting | Default Value | Description |
|---------|---------------|-------------|
| JPEG Quality | 80% | Balance between quality and file size |
| DPI | 300 | High resolution for crisp text |
| Compression Method | Auto | PyMuPDF with PyPDF2 fallback |
| Text Preservation | Enabled | Maintains text clarity |

### Customizing Settings

You can modify these settings in the `main()` function:

```python
# Enhanced configuration for better quality
compression_method = 'auto'  # 'auto', 'pymupdf', or 'pypdf2'
quality = 80          # JPEG quality (1-100)
dpi = 300            # DPI for text clarity
```

## 📊 How It Works

### Intelligent Processing

1. **File Detection**: Scans current directory for PDF files
2. **Content Analysis**: Analyzes each page to detect text vs image content
3. **Smart Compression**:
   - **Text-heavy pages**: Uses higher DPI and PNG format for clarity
   - **Image-heavy pages**: Applies JPEG compression with quality optimization
4. **Output Generation**: Saves compressed files with descriptive names

### Compression Strategies

- **Text Content**: Higher DPI (300) + PNG format for maximum clarity
- **Image Content**: Moderate upscaling (1.2x) + JPEG compression
- **Mixed Content**: Adaptive approach based on content analysis
- **Vector Graphics**: Preserves vector elements when possible

## 📁 Output Structure

```
your-directory/
├── document1.pdf          # Original files (untouched)
├── document2.pdf
├── pdf_compressor.py      # The script
└── compressed_pdfs/       # Generated output directory
    ├── document1_compressed.pdf
    └── document2_compressed.pdf
```

## 📈 Example Output

```
PDF Compressor - High Quality Compression to Separate Directory

Output directory: /path/to/your/directory/compressed_pdfs

Found 3 PDF file(s) to compress:

Compression settings:
  - Method: auto
  - JPEG Quality: 80%
  - DPI: 300
  - Text preservation: Enabled
  - Vector graphics: Preserved when possible

Compressing: large_document.pdf
  Original size: 15.34 MB
  Compressed size: 4.87 MB
  Compression ratio: 68.3%
  Saved to: /path/to/compressed_pdfs/large_document_compressed.pdf

============================================================
COMPRESSION SUMMARY
============================================================
Files processed: 3
Successfully compressed: 3
Output directory: /path/to/your/directory/compressed_pdfs
Total original size: 45.67 MB
Total compressed size: 12.34 MB
Overall compression: 73.0%
Space saved: 33.33 MB

Quality settings used:
  - JPEG Quality: 80% (High)
  - DPI: 300 (Enhanced)
  - Text preservation: ON

All compressed files saved in: /path/to/your/directory/compressed_pdfs
```

## 🔧 Advanced Usage

### Command Line Integration

You can integrate this into your workflow by creating an alias:

```bash
# Add to your ~/.bashrc or ~/.zshrc
alias pdfcompress='python /path/to/pdf_compressor.py'
```

### Batch Processing Multiple Directories

To process PDFs in different directories, simply copy the script to each directory or modify the `directory` parameter in `find_pdf_files()`.

## 🐛 Troubleshooting

### Common Issues

**"Missing required library" error:**
```bash
pip install PyPDF2 PyMuPDF Pillow
```

**"No PDF files found" message:**
- Ensure PDF files are in the same directory as the script
- Check that files have `.pdf` extension
- Verify files aren't already processed (ending with `_compressed.pdf`)

**Compression fails on specific files:**
- Some PDFs may have restrictions or unusual formatting
- The script will skip problematic files and continue with others
- Check the error message for specific details

### Performance Tips

- **Large Files**: The script handles large files well but may take time
- **Many Files**: Processing is sequential; larger batches take longer
- **Quality vs Speed**: Lower quality settings process faster

## 🤝 Contributing

Feel free to submit issues, feature requests, or improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility (3.6+)
4. Check file permissions in your directory

## 📚 Technical Details

### Compression Methods

- **PyMuPDF**: Primary method with advanced image processing
- **PyPDF2**: Fallback method for basic compression
- **PIL/Pillow**: Image optimization and format conversion

### Quality Preservation

- **Text Detection**: Analyzes page content to identify text regions
- **Adaptive DPI**: Uses higher resolution for text-heavy content
- **Format Selection**: PNG for text, JPEG for images
- **Vector Preservation**: Maintains vector graphics when possible

---

**Happy compressing! 🎉**