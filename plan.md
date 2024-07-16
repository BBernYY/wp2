# PLAN
> What do I want to do for `wp2`?

- One global config file (json) [ ]
    - separate entry from each wallpaper: [ ]
        ```json
            {
                "colors": str[8],
                "primary": str,
                "location": str
            }
        ```
    - separate for whatever `current` may be: [ ]
       ```json
            {
                "colors": str[8],
                "primary": str,
                "location": str
            }
        ```
        > note that these values don't have to correspond with exactly one of the wallpapers in the list.
- Handling for this config file: [ ]
    - auto-generate colors and primary based of location: `wp -a` [ ]
    - apply colors to multiple apps: `wp -s` [ ]
        - edit css with regex `($WP_COLOR1)` [ ]
        - maybe fullscreen transition effect? [ ]
    - apply wallpaper [ ]
    
    
