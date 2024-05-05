---
title: gadm-map-explorer
emoji: 🗺️
colorFrom: yellow
colorTo: blue
sdk: streamlit
sdk_version: 1.34.0
app_file: app.py
pinned: false
license: mit
---


# Motivation


The GADM (Database of Global Administrative Areas) dataset provides detailed administrative boundaries data for countries and their subdivisions globally. This comprehensive dataset is available in common GIS file formats like shapefiles, GeoPackage, and GeoJSON.

This repo aims to explore and work with the GADM dataset, utilizing its administrative boundaries information for various geospatial analyses and visualizations.


## Features

- Select districts
- Customize map style (Original, Outline)
- Add markers
- Adjust map size
- Export PNG

## Supported Countries
- India

## Installation

1. Clone repo
2. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Run: `streamlit run app.py`
2. Access at `http://localhost:8501`
3. Select district, style, and markers
4. Explore the interactive map

## Data

- GADM dataset: `gadm41_IND_3.json`

## For a new country
- Download the json from [GADM](https://gadm.org/download_country.html)
- Add to the data directory
- Replace the input source in app.py

## Libraries

- Streamlit
- Folium
- GeoPandas
- streamlit_folium

## Live Demo
[Hugging Face Space](https://huggingface.co/spaces/VigneshPasupathyHF/gadm-map-explorer)

## Contributing

Open an issue or PR for contributions.

## License

MIT License