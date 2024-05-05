import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import pandas as pd

from helpers.layers import LayerManager
from helpers.callbacks import download_png, on_district_change, on_map_style_change, on_map_width_change, on_map_height_change
from helpers.layout import reduce_spacing, display_header
from helpers.style import MAP_STYLES, BOUNDARY_STYLES, MARKER_STYLES
from helpers.converter import MapConverter
import helpers.constants as constants

class MapApp:
    def __init__(self):
        self.gadm_data = gpd.read_file(constants.GADM_FILE)
        self.district_names = self.gadm_data[constants.NAME_2].unique()
        self.state = {
            'district_name': self.district_names[0],
            'map_style': constants.MAP_STYLE_OPTIONS[0],
            'map_width': 450,
            'map_height': 450,
            'points_df': pd.DataFrame(constants.DEFAULT_POINTS)
        }
        self.map_obj = self.create_map()
        self.map_converter = MapConverter()

    def create_map(self):
        print(f"{self.state}")
        district = self.gadm_data[self.gadm_data[constants.NAME_2] == self.state['district_name']]
        map_obj = folium.Map(location=district.geometry.centroid.iloc[0].coords[0][::-1], zoom_start=8.5)
        layer_manager = LayerManager(map_obj, self.gadm_data, self.state['district_name'], self.state['points_df'], self.state['map_style'])
        bounds, district_coords = layer_manager.add_district_layer()
        layer_manager.add_location_markers()
        layer_manager.add_outline_layer(bounds)
        return map_obj

    def update_map(self):
        self.map_obj = self.create_map()

    def main(self):
        reduce_spacing()
        display_header()

        # Create tabs
        tabs = st.tabs(["Preview", "Data"])

        with tabs[0]:
            col1, col2 = st.columns([1, 3])

            with col1:
                st.selectbox(
                    constants.SELECT_DISTRICT,
                    self.district_names,
                    index=self.district_names.tolist().index(self.state['district_name']),
                    key='district_name',
                    on_change=on_district_change,
                    args=(self,)
                )
                st.selectbox(
                    constants.MAP_STYLE_LABEL,
                    constants.MAP_STYLE_OPTIONS,
                    index=constants.MAP_STYLE_OPTIONS.index(self.state['map_style']),
                    key='map_style',
                    on_change=on_map_style_change,
                    args=(self,)
                )
                st.slider(
                    constants.WIDTH_LABEL,
                    value=self.state['map_width'],
                    min_value=100,
                    max_value=1000,
                    step=50,
                    key='map_width',
                    on_change=on_map_width_change,
                    args=(self,)
                )
                st.slider(
                    constants.HEIGHT_LABEL,
                    value=self.state['map_height'],
                    min_value=100,
                    max_value=1000,
                    step=50,
                    key='map_height',
                    on_change=on_map_height_change,
                    args=(self,)
                )

                if st.button(constants.EXPORT_AS_PNG):
                    download_png(self.map_obj, self.state['district_name'], self.state['map_width'], self.state['map_height'], self.map_converter)

            with col2:
                print(f"in Col2 {self.state}")
                self.update_map()
                folium_static(self.map_obj, width=self.state['map_width'], height=self.state['map_height'])

        with tabs[1]:
            st.header("")
            form = st.form("data_editor")
            points_df = form.data_editor(self.state['points_df'], num_rows="dynamic")
            submitted = form.form_submit_button("Save Data")
            if submitted:
                with st.spinner("Saving data..."):
                    self.state['points_df'] = points_df
                    self.update_map()
                st.rerun()

if __name__ == '__main__':
    if 'app' not in st.session_state:
        st.session_state['app'] = MapApp()

    app = st.session_state['app']
    app.main()