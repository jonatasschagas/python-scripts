"""
this script performs the following:
 - extracts the text from the image
 - translates the text
 - outputs the translation to a text file
 - opens the translated text file

Used libs/software:
 - reading the text from the image file with: tesseract (https://code.google.com/p/tesseract-ocr/)
 - converting the image to PNG using: imagemagick (http://www.imagemagick.org/script/index.php)
 - translating the text to english with: translate-shell (http://www.soimort.org/translate-shell/)

"""

import sys
import os
import argparse
import logging

def parse_args():
    """
    Parses the script's arguments from the command line. Returns all options in 'opts'.
    """

    parser = argparse.ArgumentParser(
        description='Utility command to translate the text from the images to english')
    parser.add_argument('-i',
                        '--image',
                        help='Source image file',
                        dest='image')

    return parser.parse_args()

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO, format='>>> %(process)d '
                                                       '%(filename)s %(levelname)s %(message)s', stream=sys.stdout)
    opts = parse_args()
    
    if opts.image is None or opts.image == '':
        raise ValueError('please provide the source image. Usage: python translate.py -i image.png')
    
    if opts.image.lower().endswith('.jpg') or opts.image.lower().endswith('.jpeg'):
        logging.info('converting the image to PNG')
        original = opts.image
        converted = opts.image.split('.')[0] + '.png'
        os.system('convert -rotate 90 {0} {1}'.format(original, converted))
        opts.image = converted
        logging.info('image converted')
    
    logging.info('reading the text from the image')
    os.system('tesseract {0} {1}'.format(opts.image, 'image_text_output'))
    
    logging.info('translating the text to english')
    os.system('trans -b -i {0} -o {1}'.format('image_text_output.txt', 'translated_output.txt'))
    
    logging.info('opening the file')
    os.system('open translated_output.txt')

    logging.info('cleaning up')
    os.system('rm image_text_output.txt')
    