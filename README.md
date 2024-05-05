# GADM India District Map

Interactively explore GADM data using Streamlit, and Folium.

## Features

- Select districts
- Customize map style
- Add markers
- Adjust map size

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
- Download the json from https://gadm.org/download_country.html
- Add to the data directory
- Replace the input source in app.py

## Libraries

- Streamlit
- Folium
- GeoPandas
- streamlit_folium

## Contributing

Open an issue or PR for contributions.

## License

MIT License