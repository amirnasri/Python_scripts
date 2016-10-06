import xml.etree.ElementTree as et
import requests
import sys
import os

url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-US'
r = requests.get(url)
root = et.fromstring(r.content)

image_url = root.iter('url').next()
if image_url is None:
	sys.exit(1)
image_url = image_url.text.replace('1366x768', '1920x1080')

fname = image_url[image_url.rfind('/') + 1:]
fname = os.path.join('/home/amir/Pictures/Wallpapers/', fname)
r = requests.get('http://www.bing.com' + image_url)
f = open(fname, 'wb')
f.write(r.content)
f.close()

os.system('gsettings set org.gnome.desktop.background picture-uri file://' + fname)
