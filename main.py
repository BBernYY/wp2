# Imports
import argparse
from os import path, listdir
import json
import fast_colorthief
from PIL import Image

# Constants
CONF_DIR = '.'

# Parse cmd flags
def argparser(parser):
    parser.add_Argument('-a', '--add', type=str)

# Add file to config file
def add(fn):
    img = {}
    img['primary'] = fast_colorthief.get_dominant_color(fn)
    img['colors'] = fast_colorthief.get_palette(fn)
    img['location'] = path.expanduser(fn)
    with json.load(CONF_DIR+'/wp2.json') as j:
        j['wallpapers'].append(img)
        json.dump(CONF_DIR+'/wp2.json', j)
    return img
        
# Handle everything
def main():
    parser = argparse.ArgumentParser(prog='wp2', description='A wallpaper/colormanager for hyprpaper.')
    parser = argparser(parser)
    
    if parser.add:
        add(parser.add)




# Check if code isn't imported
if __name__ = '__main__':
    main()
