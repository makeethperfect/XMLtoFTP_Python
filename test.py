import xml.etree.ElementTree as ET
import re

# Parse the XML data
tree = ET.parse(r'C:\fielsxml\feedconverters.xml')
root = tree.getroot()

# Create a new root element for the filtered entries
filtered_root = ET.Element("rss")
filtered_feed = ET.SubElement(filtered_root, "feed")

# Iterate through each <entry> tag
for entry in root.findall('.//entry'):
    # Extract price and sale price
    pattern = r'\d+\.\d+'
    match = re.search(pattern, entry.find('price').text)
    sale_match = re.search(pattern, entry.find('sale_price').text)
    price = float(match.group())
    sale_price = float(sale_match.group()) if entry.find('sale_price') is not None else None
    
    # Check if sale_price is smaller than price
    if sale_price is not None and sale_price < price:
        # Append the entry to the filtered feed
        filtered_feed.append(entry)

# Create a new XML tree with the filtered entries
filtered_tree = ET.ElementTree(filtered_root)

# Write the filtered XML tree to a new file
filtered_tree.write("filtered_entries.xml", encoding="utf-8", xml_declaration=True)
