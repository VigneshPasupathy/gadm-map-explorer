import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import io
from helpers.style import MAP_STYLES, BOUNDARY_STYLES, MARKER_STYLES
from helpers.converter import convert_map_to_png
import helpers.constants as constants

def add_district_layer(map_obj, style, district, district_name):
    bounds = district.total_bounds
    district_coords = district.geometry.centroid.iloc[0].coords[0][::-1]
    folium.GeoJson(district.__geo_interface__, name=f'{district_name} District', style_function=lambda feature: BOUNDARY_STYLES[style]).add_to(map_obj)
    return map_obj, bounds, district_coords

def add_location_markers(map_obj, style, points):
    for point in points:
        name, lat, lon = point
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
    map_obj = folium.Map(location=district.geometry.centroid.iloc[0].coords[0][::-1])
    map_obj, bounds, district_coords = add_district_layer(map_obj, 'Default', district, district_name)
    map_obj.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    map_obj = add_location_markers(map_obj, 'Default', points)
    map_obj = add_outline_layer(map_obj, map_style, district, bounds)
    return map_obj


def reduce_spacing():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_header():
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 1rem;'>{constants.TITLE}</h1>", unsafe_allow_html=True)


def download_png(map_obj,district_name, map_width, map_height):
    progress_bar = st.progress(0.2)
    png_bytes = convert_map_to_png(progress_bar, map_obj, map_width, map_height)
    progress_bar.empty()

    # Initiate download automatically
    st.download_button(
            label=constants.DOWNLOAD_READY,
            data=png_bytes,
            file_name=f'{district_name}.png',
            mime='image/png',
            key='download_button')

def main():
    reduce_spacing()
    display_header() 
    map_obj = None

    # Load the GeoPackage file
    gadm_data = gpd.read_file(constants.GADM_FILE)
    district_names = gadm_data[constants.NAME_2].unique()

    col1, col2 = st.columns([1, 3])

    with col1:
        district_name = st.selectbox(constants.SELECT_DISTRICT, district_names)
        map_style = st.selectbox(constants.MAP_STYLE_LABEL, constants.MAP_STYLE_OPTIONS)
        map_width = st.slider(constants.WIDTH_LABEL, value=450, min_value=100, max_value=1000, step=50)
        map_height = st.slider(constants.HEIGHT_LABEL, value=450, min_value=100, max_value=1000, step=50)
        points_input = st.text_area(constants.POINTS_LABEL, constants.DEFAULT_POINTS)
        try:
            points = [tuple(point.strip().split(',')) for point in points_input.split(';')]
            points = [(name.strip(), float(lat), float(lon)) for name, lat, lon in points]
        except ValueError:
            points = []
        if st.button(constants.EXPORT_AS_PNG):
                print(st.session_state.map_obj)
                download_png(st.session_state.map_obj,district_name, map_width, map_height)
        
    with col2:
            st.session_state.map_obj = create_map(gadm_data, district_name, points, map_style)
            print("Map Obj Assigned")
            folium_static(st.session_state.map_obj, width=map_width, height=map_height)

if __name__ == '__main__':
    main()