import os
import zipfile
import tempfile
import argparse
from PIL import Image
from ebooklib import epub
from tqdm import tqdm

# Set of valid image extensions to improve lookup speed
VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')

def compress_images(temp_dir, quality=80, max_height=1024):
    """
    Compresses and resizes images in the specified directory.
    
    Args:
        temp_dir (str): The directory containing images to compress.
        quality (int): The quality of the compressed images (1-100).
        max_height (int): The maximum height of the images.
    """
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(VALID_IMAGE_EXTENSIONS):
                img_path = os.path.join(root, file)
                with Image.open(img_path) as img:
                    if img.mode == 'P':
                        img = img.convert('RGB')
                    if img.height > max_height:
                        aspect_ratio = img.width / img.height
                        new_width = int(aspect_ratio * max_height)
                        img = img.resize((new_width, max_height), Image.LANCZOS)
                    img.save(img_path, "JPEG", quality=quality)

def create_epub(temp_dir, output_path):
    """
    Creates an EPUB file from images in the specified directory.
    
    Args:
        temp_dir (str): The directory containing images to include in the EPUB.
        output_path (str): The path where the EPUB file will be saved.
    """
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('Converted Images')
    book.set_language('en')
    book.add_author('Author')

    for root, _, files in os.walk(temp_dir):
        for file in sorted(files):
            if file.lower().endswith(VALID_IMAGE_EXTENSIONS):
                img_path = os.path.join(root, file)
                img_name = os.path.basename(img_path)
                with open(img_path, 'rb') as img_file:
                    img_content = img_file.read()
                img_item = epub.EpubItem(uid=img_name, file_name=img_name, media_type='image/jpeg', content=img_content)
                book.add_item(img_item)
                chapter = epub.EpubHtml(title=img_name, file_name=f'{img_name}.xhtml', lang='en')
                chapter.content = f'<html><body><img src="{img_name}" alt="{img_name}"/></body></html>'
                book.add_item(chapter)
                book.spine.append(chapter)

    book.toc = tuple(book.spine[1:])
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(output_path, book, {})

def process_cbz(cbz_file, output_folder, quality, max_height, relative_path=""):
    """
    Processes a CBZ file by extracting images, compressing them, and creating an EPUB file.
    
    Args:
        cbz_file (str): The path to the CBZ file.
        output_folder (str): The folder where the EPUB file will be saved.
        quality (int): The quality of the compressed images (1-100).
        max_height (int): The maximum height of the images.
        relative_path (str): The relative path to maintain folder structure.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        compress_images(temp_dir, quality=quality, max_height=max_height)
        epub_filename = os.path.splitext(os.path.basename(cbz_file))[0] + ".epub"
        epub_output_path = os.path.join(output_folder, relative_path)
        os.makedirs(epub_output_path, exist_ok=True)
        epub_path = os.path.join(epub_output_path, epub_filename)
        create_epub(temp_dir, epub_path)
        print(f"✅ Created {epub_path}")

def process_folder(input_folder, output_folder, quality, max_height):
    """
    Processes all CBZ files in a folder by converting them to EPUB files.
    
    Args:
        input_folder (str): The folder containing CBZ files.
        output_folder (str): The folder where EPUB files will be saved.
        quality (int): The quality of the compressed images (1-100).
        max_height (int): The maximum height of the images.
    """
    for root, _, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        cbz_files = [f for f in files if f.lower().endswith('.cbz')]
        if not cbz_files:
            continue

        for cbz_file in tqdm(cbz_files, desc=f"Processing CBZ files in {relative_path}"):
            process_cbz(os.path.join(root, cbz_file), output_folder, quality, max_height, relative_path)

def get_args():
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Convert all CBZ files in a folder to EPUB files.')
    parser.add_argument('input_folder', help='Path to the folder containing CBZ files')
    parser.add_argument('output_folder', help='Path to the folder where EPUB files will be saved')
    parser.add_argument('--quality', type=int, default=80, help='Image compression quality (1-100)')
    parser.add_argument('--max-height', type=int, default=1024, help='Maximum height for images')
    return parser.parse_args()

def main():
    """
    Main function to execute the script.
    """
    args = get_args()
    process_folder(args.input_folder, args.output_folder, args.quality, args.max_height)

if __name__ == "__main__":
    main()