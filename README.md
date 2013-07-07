# Gallery generator

This is a simply python script that extracts EXIF-Data from images
and generates an HTML-File for
[gallerific](http://www.twospy.com/galleriffic/).

## Installation

Debian/Ubuntu:

    sudo apt-get install libexiv2-dev python-gobject python-pip

Arch-Linux:

    pacman -S libexiv2 python-gobject python-pip

Install Pystache and Pillow:

    sudo pip install pystache Pillow

## Usage

Place your JPEG images into the `images` folder and run

    python generate.py

This generates `gallery.html` that contains an `ul` tag
with all the list elements.

Please note:
The filename should contain an number (e.g. `img_003.jpg`).

## Licence

This project is licensed under the MIT license.
