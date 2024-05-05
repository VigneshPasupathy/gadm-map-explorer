import streamlit as st
from helpers.converter import convert_map_to_png
import helpers.constants as constants

def download_png(map_obj, district_name, map_width, map_height):
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

def on_district_change():
    st.session_state.state['district_name'] = st.session_state.district_name

def on_map_style_change():
    st.session_state.state['map_style'] = st.session_state.map_style

def on_map_width_change():
    st.session_state.state['map_width'] = st.session_state.map_width

def on_map_height_change():
    st.session_state.state['map_height'] = st.session_state.map_height