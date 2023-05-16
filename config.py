from requests.auth import HTTPBasicAuth

# Pass the key of the source project you want to clone
source_project_key = 'YOUR_PROJECT_KEY'

# Set the key of the new project
new_project_key = 'NEW_PROJECT_KEY'

# Set the authentication credentials using HTTP Basic Authentication
auth = HTTPBasicAuth("YOUR_USER/EMAIL", "YOUR_API_TOKEN")