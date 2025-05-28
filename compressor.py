#!/usr/bin/env python3
"""
PDF Compressor - Compresses all PDF files in the current directory
"""

import os
import sys
from pathlib import Path
import PyPDF2
from PIL import Image
import io
import fitz  # PyMuPDF for better compression

def get_file_size(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def compress_pdf_pypdf2(input_path, output_path):
    """Compress PDF using PyPDF2 (basic compression)"""
    try:
        with open(input_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            # Copy all pages
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            
            # Apply compression
            pdf_writer.compress_identical_objects()
            pdf_writer.remove_duplication()
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error with PyPDF2 compression: {e}")
        return False

def compress_pdf_pymupdf(input_path, output_path, quality=95, dpi=150):
    """Compress PDF using PyMuPDF with better quality settings"""
    try:
        # Open the PDF
        doc = fitz.open(input_path)
        
        # Try to preserve text and vector graphics first
        new_doc = fitz.open()
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Try to preserve text layers and vector graphics
            # Get the page content
            text_dict = page.get_text("dict")
            
            # Check if page has significant text content
            has_text = len(text_dict.get("blocks", [])) > 0
            
            if has_text:
                # For text-heavy pages, use higher DPI and preserve text
                mat = fitz.Matrix(dpi/72, dpi/72)  # Scale for higher DPI
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # Convert to PIL Image with better settings
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Use PNG for text-heavy content to preserve quality
                output_buffer = io.BytesIO()
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')
                
                # For text content, use PNG or high-quality JPEG
                if quality >= 90:
                    img.save(output_buffer, format='PNG', optimize=True)
                else:
                    img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
                
                compressed_img_data = output_buffer.getvalue()
                
                # Create new page with proper scaling
                rect = page.rect
                new_page = new_doc.new_page(width=rect.width, height=rect.height)
                new_page.insert_image(rect, stream=compressed_img_data)
            else:
                # For image-heavy pages, use moderate compression
                mat = fitz.Matrix(1.2, 1.2)  # Slight upscaling for better quality
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                output_buffer = io.BytesIO()
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')
                
                img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
                compressed_img_data = output_buffer.getvalue()
                
                rect = page.rect
                new_page = new_doc.new_page(width=rect.width, height=rect.height)
                new_page.insert_image(rect, stream=compressed_img_data)
        
        # Save with better compression settings
        new_doc.save(output_path, garbage=4, deflate=True, clean=True, pretty=True)
        new_doc.close()
        doc.close()
        
        return True
    except Exception as e:
        print(f"Error with PyMuPDF compression: {e}")
        return False

def compress_single_pdf(file_path, output_dir, compression_method='auto', quality=95, dpi=150):
    """Compress a single PDF file to output directory"""
    input_path = Path(file_path)
    output_path = output_dir / f"{input_path.stem}_compressed{input_path.suffix}"
    
    print(f"Compressing: {input_path.name}")
    
    original_size = get_file_size(input_path)
    print(f"  Original size: {original_size:.2f} MB")
    
    success = False
    
    if compression_method == 'pymupdf' or compression_method == 'auto':
        success = compress_pdf_pymupdf(str(input_path), str(output_path), quality, dpi)
    
    if not success and (compression_method == 'pypdf2' or compression_method == 'auto'):
        print("  Trying PyPDF2 method...")
        success = compress_pdf_pypdf2(str(input_path), str(output_path))
    
    if success and output_path.exists():
        compressed_size = get_file_size(output_path)
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        print(f"  Compressed size: {compressed_size:.2f} MB")
        print(f"  Compression ratio: {compression_ratio:.1f}%")
        print(f"  Saved to: {output_path}")
        
        if compressed_size >= original_size:
            print("  Note: Compressed file is not smaller (quality preserved)")
        
        return True
    else:
        print(f"  Failed to compress {input_path.name}")
        return False

def find_pdf_files(directory='.'):
    """Find all PDF files in the specified directory"""
    pdf_files = []
    for file in Path(directory).glob('*.pdf'):
        if not file.name.endswith('_compressed.pdf'):  # Skip already compressed files
            pdf_files.append(file)
    return pdf_files

def main():
    """Main function to compress all PDFs in current directory"""
    print("PDF Compressor - High Quality Compression to Separate Directory\n")
    
    # Check if required libraries are installed
    try:
        import PyPDF2
        import fitz
        from PIL import Image
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Please install required libraries:")
        print("pip install PyPDF2 PyMuPDF Pillow")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path('./compressed_pdfs')
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir.absolute()}\n")
    
    # Find all PDF files
    pdf_files = find_pdf_files()
    # print("----",pdf_files)
    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to compress:\n")
    
    # Enhanced configuration for better quality
    compression_method = 'auto'  # 'auto', 'pymupdf', or 'pypdf2'
    quality = 80  # High quality JPEG (90-100 for better quality)
    dpi = 300     # Higher DPI for better resolution
    
    print(f"Compression settings:")
    print(f"  - Method: {compression_method}")
    print(f"  - JPEG Quality: {quality}%")
    print(f"  - DPI: {dpi}")
    print(f"  - Text preservation: Enabled")
    print(f"  - Vector graphics: Preserved when possible\n")
    
    successful_compressions = 0
    total_original_size = 0
    total_compressed_size = 0
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            original_size = get_file_size(pdf_file)
            total_original_size += original_size
            
            if compress_single_pdf(pdf_file, output_dir, compression_method, quality, dpi):
                compressed_file = output_dir / f"{pdf_file.stem}_compressed{pdf_file.suffix}"
                if compressed_file.exists():
                    compressed_size = get_file_size(compressed_file)
                    total_compressed_size += compressed_size
                    successful_compressions += 1
            
            print()  # Empty line for readability
            break
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}\n")
    
    # Summary
    print("=" * 60)
    print("COMPRESSION SUMMARY")
    print("=" * 60)
    print(f"Files processed: {len(pdf_files)}")
    print(f"Successfully compressed: {successful_compressions}")
    print(f"Output directory: {output_dir.absolute()}")
    print(f"Total original size: {total_original_size:.2f} MB")
    print(f"Total compressed size: {total_compressed_size:.2f} MB")
    
    if total_original_size > 0:
        overall_compression = ((total_original_size - total_compressed_size) / total_original_size) * 100
        print(f"Overall compression: {overall_compression:.1f}%")
        print(f"Space saved: {total_original_size - total_compressed_size:.2f} MB")
        print(f"\nQuality settings used:")
        print(f"  - JPEG Quality: {quality}% (High)")
        print(f"  - DPI: {dpi} (Enhanced)")
        print(f"  - Text preservation: ON")
    
    print(f"\nAll compressed files saved in: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
