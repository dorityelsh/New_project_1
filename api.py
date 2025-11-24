import requests
import pandas as pd
import xml.etree.ElementTree as ET

url = "https://gisn.tel-aviv.gov.il/GisOpenData/service.asmx/GetLayer"

params = {
    "layerCode": 502,   # Waze Traffic lines
    "layerWhere": "",
    "xmin": 219000,     # bounding box for part of Tel Aviv (example)
    "ymin": 627000,
    "xmax": 223000,
    "ymax": 631000,
    "projection": 2039  # Israeli TM Grid
}

response = requests.get(url, params=params)
print(response.text[:500])  # see the first 500 chars

# Only parse XML if it looks correct
if response.text.strip().startswith("<"):
    root = ET.fromstring(response.text)
    features = []
    for feature in root.findall(".//Feature"):
        props = {attr.tag: attr.text for attr in feature}
        features.append(props)
    df = pd.DataFrame(features)
    print(df.head())
else:
    print("Response is not XML! Check parameters.")

