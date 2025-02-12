import json
import requests
import base64
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load PAT from config.json
try:
    with open("config/config.json", "r") as f:
        config = json.load(f)
        logging.debug("Loaded config.json successfully.")
except FileNotFoundError:
    logging.error("config.json file not found! Make sure it exists in the config directory.")
    exit(1)
except json.JSONDecodeError as e:
    logging.error(f"Error parsing config.json: {e}")
    exit(1)

# Retrieve values
PAT = config.get("AZURE_DEVOPS_PAT")
ORGANIZATION = config.get("AZURE_ORGANIZATION", "colesgroup")  # Use default if missing

if not PAT:
    logging.error("AZURE_DEVOPS_PAT is missing from config.json!")
    exit(1)

logging.debug(f"Using Azure DevOps Organization: {ORGANIZATION}")

# Encode PAT for Basic Auth
auth_header = base64.b64encode(f":{PAT}".encode("ascii")).decode("ascii")
logging.debug("Encoded PAT into Base64 successfully.")

# Azure DevOps API URL
url = f"https://dev.azure.com/{ORGANIZATION}/_apis/git/repositories?api-version=6.0"
logging.debug(f"Azure API URL: {url}")

# Make request
headers = {"Authorization": f"Basic {auth_header}"}
try:
    response = requests.get(url, headers=headers)
    logging.debug(f"Received response: {response.status_code} {response.reason}")
except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {e}")
    exit(1)

# Print output
if response.status_code == 200:
    logging.info("✅ Authentication Successful!")
    print("Repositories:", response.json())
elif response.status_code == 203:
    logging.warning("⚠️ Authentication received status 203: Non-Authoritative Information. This might mean the request was redirected or unauthorized.")
    print("Response:", response.text)
else:
    logging.error(f"❌ Authentication Failed! Status Code: {response.status_code}")
    print("Response:", response.text)
