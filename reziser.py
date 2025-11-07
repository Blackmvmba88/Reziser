#!/usr/bin/env python3
"""
Reziser - Image Resizing Tool
Resizes images to exactly 3000x3000 pixels while preserving aspect ratio.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library is required. Install it with: pip install Pillow")
    sys.exit(1)


TARGET_SIZE = 3000
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}


def resize_image(input_path: str, output_path: str = None) -> bool:
    """
    Resize an image to 3000x3000 pixels while preserving aspect ratio.
    Centers the image and pads with black or transparent background.
    
    Args:
        input_path: Path to the input image file
        output_path: Path to save the output image (optional)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Get original dimensions
        original_width, original_height = img.size
        
        # Calculate scaling factor to fit within 3000x3000 while preserving aspect ratio
        scale = min(TARGET_SIZE / original_width, TARGET_SIZE / original_height)
        
        # Calculate new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        # Resize the image using high-quality resampling
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Determine if we should use transparent or black background
        # Use transparent for images with alpha channel, black otherwise
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Create a new image with transparent background
            new_img = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
            # Convert resized image to RGBA if needed
            if resized_img.mode != 'RGBA':
                resized_img = resized_img.convert('RGBA')
        else:
            # Create a new image with black background
            new_img = Image.new('RGB', (TARGET_SIZE, TARGET_SIZE), (0, 0, 0))
            # Convert resized image to RGB if needed
            if resized_img.mode != 'RGB':
                resized_img = resized_img.convert('RGB')
        
        # Calculate position to center the resized image
        x_offset = (TARGET_SIZE - new_width) // 2
        y_offset = (TARGET_SIZE - new_height) // 2
        
        # Paste the resized image onto the centered position
        new_img.paste(resized_img, (x_offset, y_offset))
        
        # Determine output path
        if output_path is None:
            input_file = Path(input_path)
            output_dir = input_file.parent
            output_path = output_dir / f"{input_file.stem}_3000x3000.png"
        
        # Save the image
        new_img.save(output_path, 'PNG')
        print(f"✓ Resized: {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {str(e)}")
        return False


def is_supported_image(file_path: str) -> bool:
    """Check if the file is a supported image format."""
    return Path(file_path).suffix.lower() in SUPPORTED_FORMATS


def process_file(file_path: str) -> bool:
    """Process a single image file."""
    if not os.path.isfile(file_path):
        print(f"✗ File not found: {file_path}")
        return False
    
    if not is_supported_image(file_path):
        print(f"✗ Unsupported format: {file_path}")
        return False
    
    return resize_image(file_path)


def process_files(file_paths: List[str]) -> tuple:
    """
    Process multiple image files.
    
    Returns:
        Tuple of (success_count, failure_count)
    """
    success_count = 0
    failure_count = 0
    
    for file_path in file_paths:
        if process_file(file_path):
            success_count += 1
        else:
            failure_count += 1
    
    return success_count, failure_count


def process_folder(folder_path: str, recursive: bool = False) -> tuple:
    """
    Process all images in a folder.
    
    Args:
        folder_path: Path to the folder
        recursive: If True, process subfolders recursively
        
    Returns:
        Tuple of (success_count, failure_count)
    """
    if not os.path.isdir(folder_path):
        print(f"✗ Folder not found: {folder_path}")
        return 0, 0
    
    folder = Path(folder_path)
    
    # Find all image files
    if recursive:
        image_files = []
        for ext in SUPPORTED_FORMATS:
            image_files.extend(folder.rglob(f"*{ext}"))
    else:
        image_files = []
        for ext in SUPPORTED_FORMATS:
            image_files.extend(folder.glob(f"*{ext}"))
    
    if not image_files:
        print(f"✗ No supported images found in: {folder_path}")
        return 0, 0
    
    print(f"Found {len(image_files)} image(s) to process...")
    
    success_count = 0
    failure_count = 0
    
    for img_file in image_files:
        if resize_image(str(img_file)):
            success_count += 1
        else:
            failure_count += 1
    
    return success_count, failure_count


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Resize images to exactly 3000x3000 pixels while preserving aspect ratio.',
        epilog='Supported formats: JPEG, PNG, GIF, BMP, TIFF, WebP'
    )
    
    parser.add_argument(
        'paths',
        nargs='+',
        help='One or more image files or folders to process'
    )
    
    parser.add_argument(
        '-b', '--batch',
        action='store_true',
        help='Batch mode: treat paths as folders and process all images within'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='In batch mode, process subfolders recursively'
    )
    
    args = parser.parse_args()
    
    total_success = 0
    total_failure = 0
    
    if args.batch:
        # Batch mode: process folders
        for folder_path in args.paths:
            success, failure = process_folder(folder_path, args.recursive)
            total_success += success
            total_failure += failure
    else:
        # File mode: process individual files
        success, failure = process_files(args.paths)
        total_success += success
        total_failure += failure
    
    # Print summary
    print("\n" + "="*50)
    print(f"Summary: {total_success} succeeded, {total_failure} failed")
    print("="*50)
    
    # Exit with appropriate code
    sys.exit(0 if total_failure == 0 else 1)


if __name__ == '__main__':
    main()
