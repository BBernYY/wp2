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
    parser.add_argument('-s', '--set')
    parser.add_argument('-r', '--refresh', action='store_true')
    parser.add_argument('-rm', '--remove', nargs='+')
    parser.add_argument('-nc', '--no_color', action='store_true')
    parser.add_argument('-n', '--name')
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

nn = lambda i: path.splitext(path.basename(i))[0]

# Add file to config file
def add(files, nm=None):

    with open(CONF_DIR+'/wp2.json') as f:
        j = json.load(f)
    if len(files) > 1 and nm is not None:
        print("Can't set name for multiple files.")
        return
    for fn in files:
        if not is_valid_image_pillow(fn):
            print(f'Skipping {fn}... (not an image)')
            continue
        
        name = path.splitext(path.basename(fn))[0] if nm == None else nm
        
        img = {}
        img['primary'] = to_hex(*fast_colorthief.get_dominant_color(fn, quality=10))
        img['colors'] = [to_hex(*i) for i in fast_colorthief.get_palette(fn)]
        img['location'] = path.abspath(fn)
    
        j[name] = img
        print(f"Added \"{name}\" to the list successfully.")
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
        fn = nn(fn)
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
    i = nn(i)
    chosen = j[i]
    print(f"\"{i}\": "+json.dumps(chosen, indent=4))

# Set all data
def set_data(s, no_color=False, no_img=False):
    s = nn(s)
    with open(CONF_DIR+'/wp2.json') as f:
        c = json.load(f)[s]
    with open(CONF_DIR+'/wp2.current.json') as f:
        j = json.load(f)

    if no_img:
        c['location'] = j['location']
    if no_color:
        c['primary'] = j['primary']
        c['colors'] = j['colors']
    with open(CONF_DIR+'/wp2.current.json', 'w') as f:
        json.dump(c, f, indent=2)
    print(f"Set {s} into {CONF_DIR}/wp2.current.json")
    


# Handle everything
def main():
    parser = argparse.ArgumentParser(prog='wp2', description='A wallpaper/colormanager for hyprpaper.')
    parser = argparser(parser)
    args = parser.parse_args()
    n = args.name

    if args.add:
        add(args.add, nm=n)
    if args.list:
        list_wps()
    if args.remove:
        rm(args.remove)
    if args.info:
        info(args.info)
    if args.set:
        set_data(args.set, no_color=args.no_color, no_img=args.no_img)



# Check if code isn't imported
if __name__ == '__main__':
    main()
