from collections import OrderedDict

NO_TITLE = 'Ohne Titel'

def name(img):
  m = img['metadata']
  tags = [
    "Iptc.Application2.Caption",
    "Iptc.Application2.ObjectName",
    "Iptc.Application2.Headline",
    "Iptc.Application2.SubLocation",
    "Iptc.Application2.City",
    "Iptc.Application2.ProvinceState",
    "Iptc.Application2.CountryName"
  ]
  for t in tags:
    if (t in m) and (m.get(t) is not ''):
      return m[t]
  return NO_TITLE

def subtitle(img):
  m = img['metadata']
  tags = [
    "Iptc.Application2.Caption",
    "Iptc.Application2.SubLocation",
    "Iptc.Application2.City",
    "Iptc.Application2.ProvinceState",
    "Iptc.Application2.CountryName"
  ]

  n = name(img)

  # get list of tag values
  entries = [ m[tag] for tag in tags
    if  (tag in m)
    and (m.get(tag) is not '')
    and (m.get(tag) is not n )
  ]

  # remove duplicates
  entries = list(OrderedDict.fromkeys(entries))

  if len(entries) > 4:
    entries = entries[-4:]
  return entries

def alignment(img):

  w = img['width']

  if w <= 210: return "cahp"
  if w <= 253: return "cahl"
  if w <= 310: return "cahm"
  if w <= 353: return "cahs"
  if w <= 460: return "caq"
  if w <= 610: return "cas"
  if w <= 685: return "cam"
  if w <= 986: return "cal"
  return "cahp"

keyMap = {
  'name':           name,
  'srcFileName':    lambda img: img['srcDir'] + img['filename'],
  'title':          lambda img: ' '.join(subtitle(img)),
  'thumbFileName':  lambda img: img['thumbDir'] + img['filename'],
  'alt':            name,
  'alignment':      alignment,
  'subtitle':       lambda img: ', '.join(subtitle(img))
}
