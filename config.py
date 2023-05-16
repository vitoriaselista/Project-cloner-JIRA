# This script is created by Ana Vitória Selista for Jira administrative use

from requests.auth import HTTPBasicAuth

# The base URL of your instance
base_url = "https://{YOUR_INSTANCE}atlassian.net"

# Pass the key of the source project you want to clone
source_project_key = 'FGL'

# Set the name and key of the new project
new_project_name = "YOUR_NEW_PROJECT"
new_project_key = 'NEW_PROJECT_KEY'

# Set the authentication credentials using HTTP Basic Authentication
credentials = HTTPBasicAuth("YOUR_USER", "YOUR_JIRA_API_TOKEN")
