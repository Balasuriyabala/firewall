import http.client
import json
import ssl

# Create an unverified SSL context
conn = http.client.HTTPSConnection("192.168.1.50", context=ssl._create_unverified_context())
payload = ''
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'X-PAN-Key': 'LUFRPT1MbUtJL2hSWFg4ZCtBMTAvUHFYUkorSGwvREU9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuYlA3bjVZVDExZWxVM0VaOGdqWWVLcDBYcWNqQUpqcXJ0L1lmNHhRVEZMNQ=='
}

# Send the request to the firewall
conn.request("GET", "/restapi/v11.1/Policies/SecurityRules?location=vsys&vsys=vsys1", payload, headers)
res = conn.getresponse()

# Read the response
data = res.read()

# Decode and parse the response as JSON
json_data = json.loads(data.decode("utf-8"))

# Specify the file path where you want to save the JSON data
file_path = r'C:\Users\DELL\Desktop\output\firewall_security_rules.json'

# Write the JSON data to a local file
with open(file_path, 'w') as file:
    json.dump(json_data, file, indent=4)

print(f"JSON data saved to {file_path}")
