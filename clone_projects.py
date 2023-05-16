# This script is created by Ana Vitória Selista for Jira administrative use

import requests
import json
from config import source_project_key, new_project_key, auth

def get(url, header=None, params=None):

    # Set default empty params if not provided
    if params is None:
        params = {'': ''}

    # Set default Content-Type header if not provided
    if header is None:
        header = {'Content-Type': 'application/json'}

    # Send a GET request with the specified URL, headers, authentication, and parameters
    return requests.get(
        url,
        headers=header,
        auth=auth,
        params=params
    )


def post(url, data, header=None, params=None):
    if params is None:
        params = {'': ''}

    if header is None:
        header = {'Content-Type': 'application/json'}

    return requests.post(
        url,
        headers=header,
        data=json.dumps(data), # Convert data to JSON format
        auth=auth,
        params=params
    )

def create_new_project():

    print(f'Cloning Jira Project: {source_project_key}')

    # Base URL of the Jira instance
    base_url = 'https://{YOUR_INSTANCE}.atlassian.net'

    # Construct the URL for retrieving information about the source project
    project_url = f'{base_url}/rest/api/2/project/{source_project_key}'

    # Send a GET request to retrieve information about the source project
    source_project = get(project_url, params={
        'expand': 'description,lead,issueTypes,url,projectKeys,permissions,insight'
    }).json() # Include the desired query parameters to expand specific fields

    #------------------------------------------------------------------------------

    workflow_scheme_association_url = base_url + '/rest/api/2/workflowscheme/project'

    # Send a GET request to retrieve the workflow scheme association for the source project
    workflow_scheme_association = get(workflow_scheme_association_url,
                                      params={'projectId': source_project['id']}).json()

    # Extract the workflow scheme ID associated with the source project
    workflow_scheme_id = [wfscheme['workflowScheme']['id'] for wfscheme in workflow_scheme_association['values'] if
                          str(source_project['id']) in wfscheme['projectIds']][0] # Take the first workflow scheme ID

    #---------------------------------------------------------------------------------

    issuesecuritylevel_scheme_url = base_url + '/rest/api/2/issuesecuritylevel/project'

    # Get issue security level association
    response = requests.get(issuesecuritylevel_scheme_url, params={'projectId': source_project['id']})
    issuesecuritylevel_scheme_association = response.json() if response.status_code == 200 else {}

    # Get issue security level scheme ID
    values = issuesecuritylevel_scheme_association.get('values', [])
    issuesecuritylevel_scheme_id = next((islscheme['issuesecuritylevelscheme']['id'] for islscheme in values if
                                         str(source_project['id']) in islscheme['projectIds']), None)

    #--------------------------------------------------------------------------

    permissions_scheme_url = base_url + '/rest/api/2/permissionscheme/project'

    # Get permissions scheme association
    response = requests.get(permissions_scheme_url, params={'projectId': source_project['id']})
    permissions_scheme_association = response.json() if response.status_code == 200 else {}

    # Get permissions scheme ID
    values = permissions_scheme_association.get('values', [])
    permissions_scheme_id = next((pmscheme['permissionscheme']['id'] for pmscheme in values if
                                         str(source_project['id']) in pmscheme['projectIds']), None)

    #--------------------------------------------------------------------------

    fieldconfiguration_scheme_url = base_url + '/rest/api/2/fieldconfigurationscheme/project'

    # Get permissions scheme association
    response = requests.get(fieldconfiguration_scheme_url, params={'projectId': source_project['id']})
    fieldconfiguration_scheme_association = response.json() if response.status_code == 200 else {}

    # Get permissions scheme ID
    values = fieldconfiguration_scheme_association.get('values', [])
    fieldconfiguration_scheme_id = next((fcscheme['fieldconfigurationscheme']['id'] for fcscheme in values if
                                         str(source_project['id']) in fcscheme['projectIds']), None)

    #-----------------------------------------------------------------------

    securitylevel_scheme_url = base_url + '/rest/api/2/securitylevel/project'

    # Get security level association
    response = requests.get(securitylevel_scheme_url, params={'projectId': source_project['id']})
    securitylevel_scheme_association = response.json() if response.status_code == 200 else {}

    # Get security level scheme ID
    values = securitylevel_scheme_association.get('values', [])
    securitylevel_scheme_id = next((slscheme['securitylevel']['id'] for slscheme in values if
                                  str(source_project['id']) in slscheme['projectIds']), None)

    # Create the initial payload dictionary with common fields
    payload = {
        "key": new_project_key,
        "name": 'Clone of ' + source_project['name'],
        "projectTypeKey": source_project['projectTypeKey'],
        "leadAccountId": source_project['lead']['accountId'],

        # Add the workflow scheme to the payload
        "workflowScheme": workflow_scheme_id,

    }
    # Conditionally add schemes if the ID is not None
    if issuesecuritylevel_scheme_id is not None:
        payload["issuesecuritylevelscheme"] = issuesecuritylevel_scheme_id

    if permissions_scheme_id is not None:
        payload["permissionScheme"] = permissions_scheme_id

    if securitylevel_scheme_id is not None:
        payload["securitylevel"] = securitylevel_scheme_id

    if fieldconfiguration_scheme_id is not None:
        payload["fieldConfigurationScheme"] = fieldconfiguration_scheme_id

    # Send a POST request to create a new project with the provided payload
    response = post(
        base_url + "/rest/api/2/project",
        data=payload)

    # Print the status code and response JSON
    print(response.status_code,
          response.json())

    print(f"You're new project is available! Access your Jira instance and search in projects for {new_project_key}")

create_new_project()
