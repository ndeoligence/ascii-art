#!/usr/bin/env python3
# code credit goes to:
#   https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie

import sys
import os
from PIL import Image
import click

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
SUPPORTED_IMAGE_TYPES = ['.png']


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image):
    return image.convert('L')


def map_pixels_to_ascii_chars(image, reverse, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    # We make a copy on reverse so we don't modify the global array.
    ascii_chars = ASCII_CHARS if not reverse else ASCII_CHARS[::-1]

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ascii_chars[int(pixel_value/range_width)] for pixel_value in pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, reverse=False, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, reverse)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)


def handle_image_conversion(image_filepath, reverse):
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return None

    return convert_image_to_ascii(image, reverse)


def write_file(ascii, filename):
    if not ascii or not filename:
        return False
    try:
        with open(filename, "w") as f:
            f.write(ascii)
            print(f"Image saved to -> {filename}")
            return True
    except:
        print("An error occured!")
        return False


def output_name(input):
    if not input:
        return 'output.txt'
    return f"{os.path.splitext(input)[0]}_output.txt"


def check_file(path):
    _, ext = os.path.splitext(path)
    if ext.lower() not in SUPPORTED_IMAGE_TYPES:
        print(f"{path} is not supported")
        print("Supported file types: ", end='')
        print(', '.join(SUPPORTED_IMAGE_TYPES))
        sys.exit(1)


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-r', '--reverse', is_flag=True, help='reverse the ASCII_CHARS')
@click.option('-s', '--save', is_flag=True,
              help='save the output to file (by default the output file is [input_file]_output.txt)')
@click.option('-o', '--output', default=None, type=click.Path(),
              help='Specify the name of the output file instead of using the default. -s is implied.')
def main(input_file, reverse, save, output):
    check_file(input_file)
    save = save or (output is not None)
    if save and not output:
        output = output_name(input_file)
    ascii_str = handle_image_conversion(input_file, reverse)

    if save:
        write_file(ascii_str, output)
    else:
        print(ascii_str)


if __name__ == '__main__':
    main()
