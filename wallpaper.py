import xml.etree.ElementTree as et
import requests
import sys
import os

def remove_old_wallpapers(folder):
	jpg_file_list = filter(lambda x : x.find('pwm') == 0 and x.endswith('1920x1080.jpg'), os.listdir(folder))
	jpg_file_list.sort(key=lambda x : os.path.getmtime(), reverse = True)
	while len(jpg_file_list) > max_wallpapers:
		os.remove(jpg_file_list.pop())
		
# Maximum number of wallpapers to keep
max_wallpapers = 10
home_folder = os.path.expanduser('~')
folder = os.path.join(home_folder, 'Pictures/Wallpapers/')
if os.path.exists(folder):
	remove_old_wallpapers(folder)
else:
	os.mkdir(folder)
url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-US'
r = requests.get(url)
root = et.fromstring(r.content)

image_url = root.iter('url').next()
if image_url is None:
	sys.exit(1)
image_url = image_url.text.replace('1366x768', '1920x1080')

fname = 'pwm_' + image_url[image_url.rfind('/') + 1:]
fname = os.path.join(folder, fname)
r = requests.get('http://www.bing.com' + image_url)
f = open(fname, 'wb')
f.write(r.content)
f.close()

os.system('gsettings set org.gnome.desktop.background picture-uri file://' + fname)


