MAP_STYLES = {
    'Original': None,
    'Outline': {
        'attr': ("&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> "
                 "contributors, &copy; <a href='https://cartodb.com/attributions'>CartoDB</a>"),
        'tiles': "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
    }
}

BOUNDARY_STYLES = {
    'Default': {
        'fillOpacity': 0,
        'weight': 2,
        'color': 'black'
    },
    'Bold': {
        'fillOpacity': 0.8,
        'weight': 3,
        'color': 'green'
    }
}

MARKER_STYLES = {
    'Default': {
        'radius': 2,
        'color': 'black',
        'fill': True,
        'fill_color': 'transparent',
        'fill_opacity': 1
    },
    'Style1': {
        'radius': 2,
        'color': 'blue',
        'fill': True,
        'fill_color': 'white',
        'fill_opacity': 1
    },
}