# CBZ to EPUB Converter

This script converts all `.cbz` files in a specified folder to `.epub` format. It extracts images from the CBZ files, compresses them, and creates an EPUB file for each CBZ file.

## Prerequisites

Ensure you have Python 3 installed on your system. You will also need the following Python libraries:

- Pillow
- ebooklib
- tqdm

You can install these libraries using `pip`:

pip install pillow ebooklib tqdm

## Installation

1. Clone this repository or download the script `convert-cbz-to-epub.py` to your local machine.

2. Ensure the script is executable. You can set the execute permission using:

```sh
chmod +x convert-cbz-to-epub.py
```

## Usage

Run the script from the command line, providing the path to the folder containing your `.cbz` files and the output folder where the `.epub` files will be saved:

```sh
python convert-cbz-to-epub.py /path/to/your/input_folder /path/to/your/output_folder
```

### Optional Arguments

- --quality: Image compression quality (1-100). Default is 80.
- --max-height: Maximum height for images. Default is 1024.

Example with optional arguments:

```sh
python convert-cbz-to-epub.py /path/to/your/input_folder /path/to/your/output_folder --quality 90 --max-height 1200
```

## Example

Assume you have a folder `/home/user/comics` containing several `.cbz` files and you want to save the `.epub` files in `/home/user/epubs`. To convert all these files to `.epub` format with default settings, run:

```sh
python convert-cbz-to-epub.py /home/user/comics /home/user/epubs
```

## Output

The script will create an `.epub` file for each `.cbz` file in the specified output directory. The output files will have the same name as the input files but with an `.epub` extension.

## License

This project is licensed under the MIT License.
