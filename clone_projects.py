# This script is created by Ana Vitória Selista for Jira administrative use

import requests
import json
from config import source_project_key, new_project_key, credentials, base_url, new_project_name


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
        auth=credentials,
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
        data=json.dumps(data),  # Convert data to JSON format
        auth=credentials,
        params=params
    )


def get_workflow_scheme_id(source_project_data):
    workflow_scheme_association_url = base_url + '/rest/api/2/workflowscheme/project'

    # Send a GET request to retrieve the workflow scheme association for the source project
    workflow_scheme_association = get(workflow_scheme_association_url,
                                      params={'projectId': source_project_data['id']}).json()

    # Extract the workflow scheme ID associated with the source project
    return [int(wfscheme['workflowScheme']['id']) for wfscheme in workflow_scheme_association['values'] if
            str(source_project_data['id']) in wfscheme['projectIds']][0]  # Take the first workflow scheme ID


def get_notification_scheme_id(source_project_data):
    url = base_url + "/rest/api/2/notificationscheme/project"
    results = get(url, params={'maxResults': 100, 'projectId': source_project_data['id']})
    return int(results.json()['values'][0]['notificationSchemeId']) if len(results.json()['values']) == 1 else False


def get_issuetype_scheme_id(source_project_data):
    url = base_url + f'/rest/api/2/issuetypescheme/project?projectId={source_project_data["id"]}'
    return int(get(url).json()['values'][0]['issueTypeScheme']['id'])


def get_issuetype_screen_scheme_id(source_project_data):
    url = base_url + f'/rest/api/2/issuetypescreenscheme/project?projectId={source_project_data["id"]}'
    return int(get(url).json()['values'][0]['issueTypeScreenScheme']['id'])


def get_permission_scheme_id(source_project_data):
    url = base_url + f'/rest/api/3/project/{source_project_data["id"]}/permissionscheme'
    return int(get(url).json()['id'])



def clone_project():
    print(f'Cloning Jira Project: {source_project_key}')

    # Construct the URL for retrieving information about the source project
    project_url = f'{base_url}/rest/api/2/project/{source_project_key}'

    # Send a GET request to retrieve information about the source project
    source_project = get(project_url, params={
        'expand': 'description,lead,issueTypes,url,projectKeys,permissions,insight'
    }).json()  # Include the desired query parameters to expand specific fields

    # ---------------------------------------------------------------------------------
    # Using functions defined above.
    # ---------------------------------------------------------------------------------

    # Create the initial payload dictionary with common fields
    payload = {
        "key": new_project_key,
        "name": 'Clone of ' + source_project['name'] if new_project_name == '' else new_project_name,
        "projectTypeKey": source_project['projectTypeKey'],
        "leadAccountId": source_project['lead']['accountId'],
        "description": f"This project is a clone of {source_project['name']}\n\n{source_project['description']}",

        # Add the workflow scheme to the payload
        "workflowScheme": get_workflow_scheme_id(source_project),
        'issueTypeScheme': get_issuetype_scheme_id(source_project),
        'issueTypeScreenScheme': get_issuetype_screen_scheme_id(source_project),

        'permissionScheme': get_permission_scheme_id(source_project), # ! Permission schemes are not available in free plans
        'notificationScheme': get_notification_scheme_id(source_project),
    }

    # Send a POST request to create a new project with the provided payload
    response = post(
        base_url + "/rest/api/2/project",
        data=payload)

    # Print the status code and response JSON
    print(response.status_code,
          response.json())

    print(f"You're new project is available! Access your Jira instance and search in projects for {new_project_key}")

clone_project()
