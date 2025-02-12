import json
import requests
import base64

# Load PAT from config.json
with open("config/config.json", "r") as f:
    config = json.load(f)

PAT = config["AZURE_DEVOPS_PAT"]
ORGANIZATION = "colesgroup"  # Change if needed

# Encode PAT for Basic Auth
auth_header = base64.b64encode(f":{PAT}".encode("ascii")).decode("ascii")

# Azure DevOps API URL
url = f"https://dev.azure.com/{ORGANIZATION}/_apis/git/repositories?api-version=6.0"

# Make request
headers = {"Authorization": f"Basic {auth_header}"}
response = requests.get(url, headers=headers)

# Print output
if response.status_code == 200:
    print("✅ Authentication Successful!")
    print("Repositories:", response.json())
else:
    print(f"❌ Authentication Failed! Status Code: {response.status_code}")
    print("Response:", response.text)
