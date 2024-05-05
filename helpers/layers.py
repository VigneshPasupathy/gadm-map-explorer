import folium
from helpers.style import MAP_STYLES,BOUNDARY_STYLES, MARKER_STYLES
import helpers.constants as constants
import pandas as pd

def add_district_layer(map_obj, style, district, district_name):
    bounds = district.total_bounds
    district_coords = district.geometry.centroid.iloc[0].coords[0][::-1]
    folium.GeoJson(district.__geo_interface__, name=f'{district_name} District', style_function=lambda feature: BOUNDARY_STYLES[style]).add_to(map_obj)
    return map_obj, bounds, district_coords

def add_location_markers(map_obj, style, points_df):
    for point in points_df.itertuples(index=False):
        name, lat, lon = point.Name, point.Latitude, point.Longitude
        if pd.notna(lat) and pd.notna(lon):
            try:
                folium.CircleMarker(
                    location=[lat, lon],
                    **MARKER_STYLES[style]
                ).add_to(map_obj)
                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(
                        icon_size=(150, 36),
                        icon_anchor=(0, 0),
                        html=f'<div style="font-size: 8pt; color: black; font-family: Arial; font-weight: bold;">{name}</div>'
                    )
                ).add_to(map_obj)
            except ValueError as e:
                st.warning(f"Error adding marker for {name}: {str(e)}")
    return map_obj

def add_outline_layer(map_obj, style, district, bounds):
    map_style = MAP_STYLES[style]
    if map_style:
        folium.TileLayer(tiles=map_style['tiles'], attr=map_style['attr'], name='Custom Tile Layer').add_to(map_obj)
        for _, row in district.iterrows():
            taluk_name = row[constants.NAME_3]
            taluk_coords = row.geometry.centroid.coords[0][::-1]
            folium.Marker(location=taluk_coords, icon=folium.DivIcon(icon_size=(150, 36), icon_anchor=(0, 0), html=f'<div style="font-size: 8pt; color: black; font-family: Arial; font-weight: bold;">{taluk_name}</div>')).add_to(map_obj)
    return map_obj

def create_map(gadm_data, district_name, points, map_style):
    district = gadm_data[gadm_data[constants.NAME_2] == district_name]
    map_obj = folium.Map(location=district.geometry.centroid.iloc[0].coords[0][::-1], zoom_start=8.5)
    map_obj, bounds, district_coords = add_district_layer(map_obj, 'Default', district, district_name)
    print(f"Bounds is {bounds}")
    #map_obj.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    map_obj = add_location_markers(map_obj, 'Default', points)
    map_obj = add_outline_layer(map_obj, map_style, district, bounds)
    return map_obj