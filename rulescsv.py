import http.client
import json
import csv
import os
import ssl

# Create an unverified SSL context
conn = http.client.HTTPSConnection("192.168.29.238", context=ssl._create_unverified_context())
payload = ''
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'X-PAN-Key': 'LUFRPT1obHVQZ045bWFzckxHVGl6MGl1b1NaSU5uVkk9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuUTZNd3UxVitXQmIrRHMzUGRPZmxWRzVpZHpWdG9qRnR4RFRLMUgzZHYrbQ=='
}

# Send the request to the firewall
conn.request("GET", "/restapi/v10.2/Policies/SecurityRules?location=vsys&vsys=vsys1", payload, headers)
res = conn.getresponse()

# Read the response
data = res.read()

# Decode and parse the response as JSON
json_data = json.loads(data.decode("utf-8"))

# Specify the directory and file path for the CSV file
directory_path = r'C:\Users\DELL\Desktop\output'
file_path = os.path.join(directory_path, 'firewall_security_rules.csv')

# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

# Extract the relevant data for CSV
rules = json_data.get('result', {}).get('entry', [])

# Write the JSON data to a CSV file
with open(file_path, 'w', newline='') as file:
    csv_writer = csv.writer(file)
    
    # Write the header
    if rules:
        header = rules[0].keys()
        csv_writer.writerow(header)
    
        # Write the data rows
        for rule in rules:
            csv_writer.writerow(rule.values())

print(f"CSV data saved to {file_path}")
