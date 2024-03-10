import schedule
import time
import requests
import os
import xml.etree.ElementTree as ET
import re
from ftplib import FTP

def send_xml_file_to_ftp(xml_file_path, ftp_server, ftp_username, ftp_password, ftp_directory):
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_server)
        ftp.login(user=ftp_username, passwd=ftp_password)
        
        # Change to the specified directory
        ftp.cwd(ftp_directory)
        
        # Open the local XML file in binary mode for reading
        with open(xml_file_path, 'rb') as file:
            # Upload the file to the FTP server
            ftp.storbinary(f'STOR {xml_file_path}', file)
        
        print(f"File '{xml_file_path}' uploaded successfully to '{ftp_directory}' on {ftp_server}.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Close the FTP connection
        if ftp:
            ftp.quit()


def my_task():
    # URL of the XML file
    url = "https://agatameble.pl/xml/feedconverters.xml"

    # Folder to store the XML file
    folder_path = os.getcwd()

    # Ensure the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # File path for storing the downloaded XML file
    file_path = os.path.join(folder_path, "feedconverters.xml")

    # Send a GET request to the URL to download the XML content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the file in binary write mode and write the content of the response to it
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("XML file downloaded successfully and stored at:", file_path)
    else:
        print("Failed to download XML file")


    # Parse the XML data
    tree = ET.parse(r'C:\fielsxml\feedconverters.xml')
    root = tree.getroot()

    # Create a new root element for the filtered entries
    filtered_root = ET.Element("rss")
    filtered_feed = ET.SubElement(filtered_root, "feed")

    prefix = "https://go.trackitlikeitshot.pl/click?o=3654&a=1&deep_link="

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
            link_element = entry.find('link')
            link_element.text = prefix + link_element.text
            filtered_feed.append(entry)

    # Create a new XML tree with the filtered entries
    filtered_tree = ET.ElementTree(filtered_root)

    # Write the filtered XML tree to a new file
    filtered_tree.write("filtered_entries.xml", encoding="utf-8", xml_declaration=True)


    xml_file_path = 'filtered_entries.xml'
    ftp_server = 'converters.ftp.dhosting.pl'
    ftp_username = 'eim9du_feed'
    ftp_password = 'yU#Zz@y2ukJ5$J'
    ftp_directory = '/'
    send_xml_file_to_ftp(xml_file_path, ftp_server, ftp_username, ftp_password, ftp_directory)

# Schedule the task to run at 8:00 am every day
schedule.every().day.at("08:00").do(my_task)

while True:
    schedule.run_pending()
    time.sleep(60)  # Sleep for 1 minute to avoid consuming too much CPU
