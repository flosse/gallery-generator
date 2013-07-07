# Copyright (c) 2013 Markus Kohlhase

import os
import re
from gi.repository import GExiv2
import pystache
import json
from keyMap import keyMap
from PIL import Image

REGEX_FILENAME    = '\\d+\.jpg'
REGEX_NUMBER      = '(?<![-.])([1-9])(\\d+)*'
SRC_IMG_FOLDER    = 'images/'
THUMB_IMG_FOLDER  = 'thumbs/'
TEMPLATE          = 'template.mustache'
OUT_FILE_NAME     = 'gallery.html'
GENERATE_JSON     = False

fileRegex   = re.compile(REGEX_FILENAME, re.IGNORECASE)
numberRegex = re.compile(REGEX_NUMBER,   re.IGNORECASE)

files    = os.listdir(SRC_IMG_FOLDER)
imgFiles = filter(fileRegex.search, files)
images   = []

for f in imgFiles:
  nr = numberRegex.search(f).group()
  if nr in images:
    print("WARN: image number " + nr + " already exists")
    continue
  meta = GExiv2.Metadata()
  try:
    meta.open_path(SRC_IMG_FOLDER + f)
  except:
    print("ERROR: could not process '" + f + "'")
    continue
  obj = {}
  for tag in meta.get_exif_tags():
    obj[tag] = meta.get_tag_string(tag)
  for tag in meta.get_iptc_tags():
    obj[tag] = meta.get_tag_string(tag)
  w, h = Image.open(SRC_IMG_FOLDER + f).size
  images.append({
    'metadata' : obj,
    'filename' : f,
    'number'   : nr,
    'srcDir'   : SRC_IMG_FOLDER,
    'thumbDir' : THUMB_IMG_FOLDER,
    'width'    : w,
    'height'   : h
  })
  if GENERATE_JSON is True:
    f = open(nr+".json", 'w')
    json.dump(obj,f,indent=2)

images.sort(key = lambda x: int(x['number']))

renderer = pystache.Renderer()
template = open(TEMPLATE,"r").read()

def get_data(img):
  data = { }
  for k,f in keyMap.items():
    data[k] = f(img)
  return data

data = {
  'ulClass': "thumbs noscript",
  'images': list((get_data(img) for img in images))
}

file = open(OUT_FILE_NAME, 'w')
file.write(renderer.render(template, data))
file.close()
print('done!')
