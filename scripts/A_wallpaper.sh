CFGDIR='.'

location=$(cat "$CFGDIR/wp2.current.json" | jq '.["location"]')
location="${location//\"/}"
hyprctl hyprpaper preload "$location"
hyprctl hyprpaper wallpaper ",$location"
