# **Jira Project Cloner**

The Jira Project Cloner is a Python script designed to facilitate the cloning of projects, along with their associated schemes, using the Jira Software API's.

<span style="color:gray ;font-weight:700;font-size:20px">
    Features
</span>

### Clone entire projects: 
The script allows you to clone projects from one Jira Software instance to another, preserving all project configurations, issue types, workflows, and other associated settings.

### Scheme cloning: 
In addition to project cloning, the script also ensures that associated schemes, such as issue type schemes, workflow schemes, and screen schemes, are accurately replicated in the cloned project.

### Automated process: 
With a simple configuration and execution process, the script automates the otherwise manual and time-consuming task of cloning projects and their schemes.

<span style="color:gray ;font-weight:700;font-size:20px">
    Prerequisites
</span>


    Python 3.x installed on your system
    Access to a Jira Software instance with administrative privileges
    Jira Software API credentials (API token & username/password)

<span style="color:gray ;font-weight:700;font-size:20px">
    Installation
</span>

    Clone the repository or download the script directly to your local machine.

    Install the required Python packages by running the following command:

    pip install -r requirements.txt

<span style="color:gray ;font-weight:700;font-size:20px">
    Configuration
</span>

Before running the script, you need to configure the following settings:

1. Open the config.py file.


2. Update the following variables with your Jira Software instance details and credentials:

         YOUR_PROJECT_KEY: The key of the source project you want to clone

         NEW_PROJECT_KEY: Set the key of the new project

         YOUR_USER/EMAIL: Your Atlassian account user

         API_TOKEN: Your Jira Software API token or password

<span style="color:gray ;font-weight:700;font-size:20px">
    Usage
</span>

    Open a terminal or command prompt and navigate to the directory containing the script.

    Run the following command to start the project cloning process:

    python clone_projects.py

    The script will initiate the cloning process and provide progress updates in the terminal.

    Once the script completes, the cloned project, including its associated schemes, will be available in your Jira Software instance.

<span style="color:gray ;font-weight:700;font-size:20px">
    Notes
</span>

This script is intended for **administrative** use and requires appropriate permissions to clone projects and modify schemes.

Ensure that you have valid backup mechanisms in place before executing this script, as it performs irreversible changes to your Jira Software instance.

<span style="color:gray ;font-weight:700;font-size:20px">
    License
</span>

This script is created by [Ana Vitória Selista](https://github.com/vitoriaselista) and is licensed under the [MIT License](LICENSE).

*Please exercise caution while using this script and always double-check your configuration settings before executing it. If you encounter any issues or need further assistance, feel free to reach out to the script's author or refer to the Jira Software API documentation for more information.*