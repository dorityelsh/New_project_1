import urllib.request
import json
import pandas as pd

# URL to the API (example)
url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=7725f888-0c51-44e7-8c5e-6771af01929a&limit=5&q=title:jones'  
# Fetch data
with urllib.request.urlopen(url) as response:
    data = response.read().decode('utf-8')  # bytes → string
    data_dict = json.loads(data)  # JSON string → Python dict

# The records are inside ['result']['records']
records = data_dict['result']['records']

# Convert to pandas DataFrame
df = pd.DataFrame(records)

# Show the DataFrame
print(df.head())

