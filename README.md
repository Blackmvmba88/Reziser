# Reziser

An image resizing tool that resizes images to exactly 3000x3000 pixels while preserving aspect ratio.

## Features

- Resize images to exactly 3000x3000 pixels
- Automatically preserves aspect ratio
- Centers images with black or transparent padding
- Supports multiple image formats: JPEG, PNG, GIF, BMP, TIFF, WebP
- Process single files, multiple files, or entire folders
- Batch mode for processing folders
- Recursive folder processing option

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Blackmvmba88/Reziser.git
cd Reziser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Process a single image file
```bash
python reziser.py image.jpg
```

### Process multiple image files
```bash
python reziser.py image1.jpg image2.png image3.gif
```

### Process all images in a folder (batch mode)
```bash
python reziser.py -b /path/to/folder
```

### Process all images in a folder recursively
```bash
python reziser.py -b -r /path/to/folder
```

### Options

- `-b, --batch`: Batch mode - treat paths as folders and process all images within
- `-r, --recursive`: In batch mode, process subfolders recursively

## Output

- Resized images are saved as `[original_name]_3000x3000.png` in the same directory as the original
- Images with transparency (PNG with alpha channel) use transparent padding
- Other images use black padding
- Original images are not modified

## Examples

```bash
# Resize a single photo
python reziser.py photo.jpg
# Output: photo_3000x3000.png

# Resize multiple photos
python reziser.py photo1.jpg photo2.png photo3.gif

# Process all images in a folder
python reziser.py -b ./my_images/

# Process all images in a folder and subfolders
python reziser.py -b -r ./my_images/
```

## Requirements

- Python 3.6+
- Pillow (PIL) 10.0.0+

## License

This project is open source and available under the MIT License.
