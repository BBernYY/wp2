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
    parser.add_argument('-a', '--add', type=str)
    return parser

# Add file to config file

def to_hex(r, g, b):
    f = lambda x: '0'+hex(x)[:2] if x < 16 else hex(x)[2:]
    return f(r)+f(g)+f(b)

def add(fn):
    img = {}
    img['primary'] = to_hex(*fast_colorthief.get_dominant_color(fn, quality=10))
    img['colors'] = [to_hex(*i) for i in fast_colorthief.get_palette(fn)]
    img['location'] = path.abspath(fn)
    
    with open(CONF_DIR+'/wp2.json') as f:
        j = json.load(f)
    j[path.splitext(fn)[0]] = img
    with open(CONF_DIR+'/wp2.json', 'w') as f:
        json.dump(j, f, indent=2)
    return img
        
# Handle everything
def main():
    parser = argparse.ArgumentParser(prog='wp2', description='A wallpaper/colormanager for hyprpaper.')
    parser = argparser(parser)
    args = parser.parse_args()
    
    if args.add:
        add(args.add)




# Check if code isn't imported
if __name__ == '__main__':
    main()
