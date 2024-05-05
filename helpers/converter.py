import io
import os
import tempfile
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def convert_map_to_png(progress_bar, map_obj, width, height):
    progress_bar.progress(0.5)

    # Create a headless Chrome browser instance
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Capture the map as a PNG image using the _to_png() method
    png_data = map_obj._to_png()

    progress_bar.progress(0.8)

    # Resize the image
    bytes_io = io.BytesIO(png_data)
    img = Image.open(bytes_io)

    # Save the resized image to a BytesIO object
    bytes_io = io.BytesIO()
    img.save(bytes_io, format='PNG')

    progress_bar.progress(0.9)

    # Clean up
    driver.quit()

    return bytes_io.getvalue()