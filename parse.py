import os
import json
import xml.etree.ElementTree as ET
import pandas as pd  # Import pandas for CSV writing

# Set the correct folder path
folder_path = r"C:\5th sem\Thesis\Main\all"

# List files in the directory
files = os.listdir(folder_path)

# Separate files by extension
json_files = [f for f in files if f.endswith('.json')]
xml_files = [f for f in files if f.endswith('.xml')]

# Initialize a list to store the extracted data
data_list = []

# Function to extract all keys from a JSON object
def extract_json_keys(data, prefix=""):
    extracted = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            # Recursively process nested dictionaries
            extracted.update(extract_json_keys(value, prefix=full_key))
        elif isinstance(value, list):
            # Handle lists by extracting info from the first item if it's a dictionary
            if len(value) > 0 and isinstance(value[0], dict):
                extracted.update(extract_json_keys(value[0], prefix=full_key))
            else:
                extracted[full_key] = value
        else:
            extracted[full_key] = value
    return extracted

# Process JSON files
for file in json_files:
    with open(os.path.join(folder_path, file), 'r') as f:
        data = json.load(f)
        # Extract all keys and their values from the JSON object
        extracted_data = {"File Name": file, "Data Type": "JSON"}
        extracted_data.update(extract_json_keys(data))
        data_list.append(extracted_data)

# Process XML files
for file in xml_files:
    tree = ET.parse(os.path.join(folder_path, file))
    root = tree.getroot()
    for child in root:  # Iterate over child elements
        extracted_data = {
            "File Name": file,
            "Data Type": "XML",
            "Tag": child.tag,  # Extract the tag name
            "Text": child.text.strip() if child.text else "N/A",  # Extract the text content
            "Attributes": child.attrib,  # Extract attributes of the tag
        }
        data_list.append(extracted_data)

# Convert the data list to a pandas DataFrame
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
output_file = "extracted_data.csv"
df.to_csv(output_file, index=False)
print(f"Data successfully saved to {output_file}")

# Display a preview of the saved data
print("Data Preview:")
print(df.head())
