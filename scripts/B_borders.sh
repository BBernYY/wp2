CFGDIR='.'

color1=$(cat "$CFGDIR/wp2.current.json" | jq '.["colors"][0]')
color1="${color1//\"/}"
color2=$(cat "$CFGDIR/wp2.current.json" | jq '.["colors"][1]')
color2="${color2//\"/}"
color3=$(cat "$CFGDIR/wp2.current.json" | jq '.["colors"][-1]')
color3="${color3//\"/}"





hyprctl keyword general:col.active_border "rgba(${color1}ee) rgba(${color2}ee) 45deg"
hyprctl keyword general:col.inactive_border "rgba(${color3}ee) rgba(${color3}ee) 45deg"
