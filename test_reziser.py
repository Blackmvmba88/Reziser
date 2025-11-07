"""
Unit tests for Reziser image resizing tool.
"""

import os
import tempfile
import unittest
from pathlib import Path
from PIL import Image

# Import the module functions
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reziser


class TestRezizerCore(unittest.TestCase):
    """Test core functionality of the image resizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_image(self, width, height, mode='RGB', filename='test.png'):
        """Helper to create a test image."""
        img_path = os.path.join(self.temp_dir, filename)
        if mode == 'RGBA':
            img = Image.new(mode, (width, height), color=(255, 0, 0, 255))
        else:
            img = Image.new(mode, (width, height), color='red')
        img.save(img_path)
        return img_path
    
    def test_resize_wide_image(self):
        """Test resizing a wide landscape image."""
        # Create a wide image (4000x2000)
        input_path = self.create_test_image(4000, 2000)
        
        # Resize it
        result = reziser.resize_image(input_path)
        
        # Check the result
        self.assertTrue(result)
        
        # Verify output file exists
        output_path = os.path.join(self.temp_dir, 'test_3000x3000.png')
        self.assertTrue(os.path.exists(output_path))
        
        # Verify dimensions
        output_img = Image.open(output_path)
        self.assertEqual(output_img.size, (3000, 3000))
        
    def test_resize_tall_image(self):
        """Test resizing a tall portrait image."""
        # Create a tall image (1000x4000)
        input_path = self.create_test_image(1000, 4000)
        
        # Resize it
        result = reziser.resize_image(input_path)
        
        # Check the result
        self.assertTrue(result)
        
        # Verify output dimensions
        output_path = os.path.join(self.temp_dir, 'test_3000x3000.png')
        output_img = Image.open(output_path)
        self.assertEqual(output_img.size, (3000, 3000))
    
    def test_resize_square_image(self):
        """Test resizing a square image."""
        # Create a square image (2000x2000)
        input_path = self.create_test_image(2000, 2000)
        
        # Resize it
        result = reziser.resize_image(input_path)
        
        # Check the result
        self.assertTrue(result)
        
        # Verify output dimensions
        output_path = os.path.join(self.temp_dir, 'test_3000x3000.png')
        output_img = Image.open(output_path)
        self.assertEqual(output_img.size, (3000, 3000))
    
    def test_resize_small_image(self):
        """Test resizing a small image (upscaling)."""
        # Create a small image (500x300)
        input_path = self.create_test_image(500, 300)
        
        # Resize it
        result = reziser.resize_image(input_path)
        
        # Check the result
        self.assertTrue(result)
        
        # Verify output dimensions
        output_path = os.path.join(self.temp_dir, 'test_3000x3000.png')
        output_img = Image.open(output_path)
        self.assertEqual(output_img.size, (3000, 3000))
    
    def test_resize_with_transparency(self):
        """Test resizing an image with transparency."""
        # Create an image with transparency
        input_path = self.create_test_image(2000, 1500, mode='RGBA')
        
        # Resize it
        result = reziser.resize_image(input_path)
        
        # Check the result
        self.assertTrue(result)
        
        # Verify output has transparency
        output_path = os.path.join(self.temp_dir, 'test_3000x3000.png')
        output_img = Image.open(output_path)
        self.assertEqual(output_img.size, (3000, 3000))
        self.assertEqual(output_img.mode, 'RGBA')
    
    def test_is_supported_image(self):
        """Test image format validation."""
        self.assertTrue(reziser.is_supported_image('test.jpg'))
        self.assertTrue(reziser.is_supported_image('test.jpeg'))
        self.assertTrue(reziser.is_supported_image('test.png'))
        self.assertTrue(reziser.is_supported_image('test.gif'))
        self.assertTrue(reziser.is_supported_image('test.bmp'))
        self.assertTrue(reziser.is_supported_image('test.tiff'))
        self.assertTrue(reziser.is_supported_image('test.webp'))
        self.assertTrue(reziser.is_supported_image('TEST.PNG'))  # Case insensitive
        self.assertFalse(reziser.is_supported_image('test.txt'))
        self.assertFalse(reziser.is_supported_image('test.pdf'))
    
    def test_process_nonexistent_file(self):
        """Test processing a file that doesn't exist."""
        result = reziser.process_file('/nonexistent/file.jpg')
        self.assertFalse(result)
    
    def test_process_unsupported_format(self):
        """Test processing an unsupported file format."""
        # Create a text file
        txt_path = os.path.join(self.temp_dir, 'test.txt')
        with open(txt_path, 'w') as f:
            f.write('not an image')
        
        result = reziser.process_file(txt_path)
        self.assertFalse(result)
    
    def test_process_multiple_files(self):
        """Test processing multiple files."""
        # Create multiple test images
        img1 = self.create_test_image(2000, 1000, filename='img1.jpg')
        img2 = self.create_test_image(1000, 2000, filename='img2.png')
        
        # Process them
        success, failure = reziser.process_files([img1, img2])
        
        # Verify results
        self.assertEqual(success, 2)
        self.assertEqual(failure, 0)
        
        # Verify output files exist
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'img1_3000x3000.png')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'img2_3000x3000.png')))
    
    def test_output_naming(self):
        """Test that output files are named correctly."""
        input_path = self.create_test_image(1000, 1000, filename='myimage.jpg')
        
        reziser.resize_image(input_path)
        
        # Check output name
        expected_output = os.path.join(self.temp_dir, 'myimage_3000x3000.png')
        self.assertTrue(os.path.exists(expected_output))


class TestRezizerFolder(unittest.TestCase):
    """Test folder processing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_image(self, width, height, filename):
        """Helper to create a test image."""
        img_path = os.path.join(self.temp_dir, filename)
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        img = Image.new('RGB', (width, height), color='blue')
        img.save(img_path)
        return img_path
    
    def test_process_folder(self):
        """Test processing all images in a folder."""
        # Create test images
        self.create_test_image(1000, 1000, 'img1.jpg')
        self.create_test_image(1500, 1000, 'img2.png')
        
        # Process folder
        success, failure = reziser.process_folder(self.temp_dir)
        
        # Verify results
        self.assertEqual(success, 2)
        self.assertEqual(failure, 0)
    
    def test_process_folder_recursive(self):
        """Test recursive folder processing."""
        # Create test images in main folder and subfolder
        self.create_test_image(1000, 1000, 'img1.jpg')
        self.create_test_image(1000, 1000, 'subfolder/img2.png')
        
        # Process folder recursively
        success, failure = reziser.process_folder(self.temp_dir, recursive=True)
        
        # Verify results (should process both images)
        self.assertEqual(success, 2)
        self.assertEqual(failure, 0)
        
        # Verify subfolder image was processed
        subfolder_output = os.path.join(self.temp_dir, 'subfolder', 'img2_3000x3000.png')
        self.assertTrue(os.path.exists(subfolder_output))
    
    def test_process_nonexistent_folder(self):
        """Test processing a folder that doesn't exist."""
        success, failure = reziser.process_folder('/nonexistent/folder')
        self.assertEqual(success, 0)
        self.assertEqual(failure, 0)


if __name__ == '__main__':
    unittest.main()
