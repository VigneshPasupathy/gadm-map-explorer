import folium
from helpers.style import MAP_STYLES, BOUNDARY_STYLES, MARKER_STYLES
import helpers.constants as constants
import pandas as pd

class LayerManager:
    def __init__(self, map_obj, gadm_data, district_name, points_df, map_style):
        self.map_obj = map_obj
        self.district = gadm_data[gadm_data[constants.NAME_2] == district_name]
        self.points_df = points_df
        self.style = map_style

    def add_district_layer(self):
        bounds = self.district.total_bounds
        district_coords = self.district.geometry.centroid.iloc[0].coords[0][::-1]
        folium.GeoJson(self.district.__geo_interface__, name=f'{self.district.iloc[0][constants.NAME_2]} District', style_function=lambda feature: BOUNDARY_STYLES['Default']).add_to(self.map_obj)
        return bounds, district_coords

    def add_location_markers(self):
        for point in self.points_df.itertuples(index=False):
            name, lat, lon = point.Name, point.Latitude, point.Longitude
            if pd.notna(lat) and pd.notna(lon):
                try:
                    folium.CircleMarker(
                        location=[lat, lon],
                        **MARKER_STYLES['Default']
                    ).add_to(self.map_obj)
                    folium.Marker(
                        location=[lat, lon],
                        icon=folium.DivIcon(
                            icon_size=(150, 36),
                            icon_anchor=(0, 0),
                            html=f'<div style="font-size: 8pt; color: black; font-family: Arial; font-weight: bold;">{name}</div>'
                        )
                    ).add_to(self.map_obj)
                except ValueError as e:
                    st.warning(f"Error adding marker for {name}: {str(e)}")

    def add_outline_layer(self, bounds):
        map_style = MAP_STYLES[self.style]
        if map_style:
            folium.TileLayer(tiles=map_style['tiles'], attr=map_style['attr'], name='Custom Tile Layer').add_to(self.map_obj)
            for _, row in self.district.iterrows():
                taluk_name = row[constants.NAME_3]
                taluk_coords = row.geometry.centroid.coords[0][::-1]
                folium.Marker(location=taluk_coords, icon=folium.DivIcon(icon_size=(150, 36), icon_anchor=(0, 0), html=f'<div style="font-size: 8pt; color: black; font-family: Arial; font-weight: bold;">{taluk_name}</div>')).add_to(self.map_obj)