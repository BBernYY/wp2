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
    parser.add_argument('-a', '--add', nargs='+')
    parser.add_argument('-i', '--info')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-rm', '--remove', nargs='+')
    parser.add_argument('-nc', '--no-color', action='store_true')
    parser.add_argument('-ni', '--no-img', action='store_true')
    return parser

# Util functions
def to_hex(r, g, b):
    f = lambda x: '0'+hex(x)[:2] if x < 16 else hex(x)[2:]
    return f(r)+f(g)+f(b)

def is_valid_image_pillow(file_name):
    try:
        with Image.open(file_name) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

# Add file to config file
def add(files):
    with open(CONF_DIR+'/wp2.json') as f:
        j = json.load(f)
    
    for fn in files:
        if not is_valid_image_pillow(fn):
            print(f'Skipping {fn}... (not an image)')
            continue

        img = {}
        img['primary'] = to_hex(*fast_colorthief.get_dominant_color(fn, quality=10))
        img['colors'] = [to_hex(*i) for i in fast_colorthief.get_palette(fn)]
        img['location'] = path.abspath(fn)
    
        j[path.splitext(path.basename(fn))[0]] = img
    
    with open(CONF_DIR+'/wp2.json', 'w') as f:
        json.dump(j, f, indent=2)
        print('Successfully saved to '+CONF_DIR+'/wp2.json.')
    return img

# List all files in table form
def list_wps():
    with open(CONF_DIR+'/wp2.json') as f:
        df = json.load(f)
    for k in df.keys():
        print(k)

# Remove
def rm(wps):
    with open(CONF_DIR+'/wp2.json') as f:
        j = json.load(f)
    for fn in wps:
        if fn in j:
            del j[fn]
            print(f"Removed {fn}.")
        else:
            print(f"{fn} could not be found.")
    with open(CONF_DIR+'/wp2.json', 'w') as f:
        json.dump(j, f, indent=2)

# Show info
def info(i):
    with open(CONF_DIR+'/wp2.json') as f:
        j = json.load(f)
    chosen = j[i]
    print(f"\"{i}\": "+json.dumps(chosen, indent=4))

# Handle everything
def main():
    parser = argparse.ArgumentParser(prog='wp2', description='A wallpaper/colormanager for hyprpaper.')
    parser = argparser(parser)
    args = parser.parse_args()

    if args.add:
        add(args.add)
    if args.list:
        list_wps()
    if args.remove:
        rm(args.remove)
    if args.info:
        info(args.info)




# Check if code isn't imported
if __name__ == '__main__':
    main()
