import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import pandas as pd

from helpers.layers import add_district_layer, add_location_markers, add_outline_layer, create_map
from helpers.callbacks import download_png, on_district_change, on_map_style_change, on_map_width_change, on_map_height_change
from helpers.layout import reduce_spacing, display_header
from helpers.style import MAP_STYLES, BOUNDARY_STYLES, MARKER_STYLES
from helpers.converter import convert_map_to_png
import helpers.constants as constants

def update_map(gadm_data):
    district_name = st.session_state.state['district_name']
    map_style = st.session_state.state['map_style']
    points_df = st.session_state.state['points_df']
    return create_map(gadm_data, district_name, points_df, map_style)

def main():
    reduce_spacing()
    display_header()

    # Load the GeoPackage file
    gadm_data = gpd.read_file(constants.GADM_FILE)
    district_names = gadm_data[constants.NAME_2].unique()

    # Initialize session state
    if 'state' not in st.session_state:
        st.session_state.state = {
            'district_name': district_names[0],
            'map_style': constants.MAP_STYLE_OPTIONS[0],
            'map_width': 450,
            'map_height': 450,
            'points_df': pd.DataFrame(constants.DEFAULT_POINTS)
        }

    # Create tabs
    tabs = st.tabs(["Preview", "Data"])

    with tabs[0]:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.selectbox(
                constants.SELECT_DISTRICT,
                district_names,
                index=district_names.tolist().index(st.session_state.state['district_name']),
                key='district_name',
                on_change=on_district_change
            )
            st.selectbox(
                constants.MAP_STYLE_LABEL,
                constants.MAP_STYLE_OPTIONS,
                index=constants.MAP_STYLE_OPTIONS.index(st.session_state.state['map_style']),
                key='map_style',
                on_change=on_map_style_change
            )
            st.slider(
                constants.WIDTH_LABEL,
                value=st.session_state.state['map_width'],
                min_value=100,
                max_value=1000,
                step=50,
                key='map_width',
                on_change=on_map_width_change
            )
            st.slider(
                constants.HEIGHT_LABEL,
                value=st.session_state.state['map_height'],
                min_value=100,
                max_value=1000,
                step=50,
                key='map_height',
                on_change=on_map_height_change
            )

            if st.button(constants.EXPORT_AS_PNG):
                download_png(st.session_state.map_obj, st.session_state.state['district_name'], st.session_state.state['map_width'], st.session_state.state['map_height'])

        with col2:
            st.session_state.map_obj = update_map(gadm_data)
            folium_static(st.session_state.map_obj, width=st.session_state.state['map_width'], height=st.session_state.state['map_height'])

    with tabs[1]:
        st.header("")
        form = st.form("data_editor")
        points_df = form.data_editor(st.session_state.state['points_df'], num_rows="dynamic")
        submitted = form.form_submit_button("Save Data")
        if submitted:
            with st.spinner("Saving data..."):
                st.session_state.state['points_df'] = points_df
                st.session_state.map_obj = update_map(gadm_data)
            st.rerun()


if __name__ == '__main__':
    main()