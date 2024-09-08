
<div>
  <a href="https://github.com/Dtar380/WorkspaceAutomation/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/github/downloads/Dtar380/WorkspaceAutomation/total?style=for-the-badge&logoColor=white&logo=download&color=0ae63d" height="20">
  </a>
  <a href="https://github.com/Dtar380/WorkspaceAutomation/issues">
    <img src="https://custom-icon-badges.demolab.com/github/issues-raw/Dtar380/WorkspaceAutomation?style=for-the-badge&color=0ae63d&logo=issue" height="20">
  </a>
  <a href="https://github.com/Dtar380/WorkspaceAutomation/blob/main/LICENSE">
    <img src="https://custom-icon-badges.demolab.com/github/license/Dtar380/WorkspaceAutomation?style=for-the-badge&color=0ae63d&logo=law" height="20">
  </a>
  <a href="https://github.com/Dtar380/WorkspaceAutomation">
    <img src="https://custom-icon-badges.demolab.com/github/stars/Dtar380/WorkspaceAutomation?style=for-the-badge&logo=star&logoColor=white&color=0ae63d" height="20">
  </a>
</div>

# :computer: WorkspaceAutomation :computer:

**WorkspaceAutomation** is a CLI tool designed to simplify and automate the process of setting up development workspaces. With this program, you can create, edit, delete, and manage customized workspaces, streamlining your daily workflow and boosting your productivity.

## Features

- **Automated Workspace Creation**: Automates the creation of a complete development environment with a single command.
- **GitHub Integration**: Publish any workspace as a GitHub repository on creation or later on.
- **Application and URL Management**: Save APPs and URLs associated with a workspace so they automatically open when reopening the workspace.
- **Workspace Editing and Relocating**: Easily modify workspace settings ot move it to another directory on your PC
- **Project Importation**: Import an existing project on your machine and transform it into a workspace.
- **Pleasing CLI**: If typing parameters for a command is not for you, you can always enter the parameters through our beautiful prompts.

## :arrow_down: App Installation

### Using built application (Not aviable now)
You can download the installer for your Operating System in the releases tab.<br>
It's preferable to download the latest version always for many reasons. Download it [here](https://github.com/Dtar380/WorkspaceAutomation/releases/latest).

### Using it as a Python Package
If you're a python enjoyer 🗿 you can install it with pip from [pypi.org](https://pypi.org/project/WorkspaceAutomation) to your main python installation so you can use it automatically from the terminal.

For doing this, just open a terminal and run:
`pip install WorkspaceAutomation`

### Building the python package yourself
You can always download the source version either from latest release and build it yourself.
To do so follow the next steps:

<details>
<summary>Download the Repo</summary>

- First go to the latest release on the releases page
- Scroll to the bottom and download the source.zip file
- Unzip the file where you desire

</details>

<details>
<summary>Install the dependencies</summary>

- Now make sure you're running on python 3.12.4 (run `python --version`)
- Now run `python -m pip install -r requirements_dev.txt`

</details>

<details>
<summary>Install app via pip</summary>

- Now run `python -m pip install -e .`
- Your CLI app is now working and you can call it via command line whenever you want

</details>

## Usage

### :bookmark_tabs: **INDEX**
- [**Create a new Workspace**](#create-a-new-workspace)
- [**Open a Workspace**](#open-a-workspace)
- [**Edit a Workspace**](#edit-a-workspace)
- [**Move a Workspace**](#move-a-workspace)
- [**Import a project as a Workspace**](#import-a-project-as-a-workspace)
- [**Publish a Workspace to GitHub**](#publish-a-workspace-to-github)
- [**Delete an exiting Workspace**](#delete-an-existing-workspace)

### Other Flares and Commands
There are additional commands, which are:
- `-v, --version`: Will display the current version of your WorkSpaceAutomation App.
- `-h, --help`: Will display the help message of the App.
- `--update`: Will update your program to the latest released version. (Only works if the app is installed as a python module)
- `--uninstall`: Will uninstall the program, but this will not errase your WorkSpaces.

There is an additional flare which is:
- `-y, --yes`: Will stop confirmation prompts.

### SetUp the application
This will only be run only one time, and the command will be:
`Workspace-auto` + `-i` or `--init`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To select by the name of the WorkSpace
- `--add-apps`: Flare to activate the app adding prompt form
- `--del-apps`: Flare to activate the app deleting prompt form
- `--add-urls`: Flare to activate the url adding prompt form
- `--del-urls`: Flare to activate the url deleting prompt form

### Required flares
There are two required flares at all times, and these are:
`-c, --command COMMAND`: Contains the command to run
`-k, --key KEY`: Contains the password to encrypt/decrypt the API-KEY

### Create a New Workspace
In order to create a new Workspace you will use the next command:
`Workspace-auto -c create`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To set the name of the WorkSpace
- `--directory DIRECTORY`: To set where the WorkSpace will be located
- `--language LANGUAGE`: To set the main language of the project
- `--github`: Flare to use if you want to create a GitHub repo
- If `--github` was used:
  - `--owner`: To set the owner of the repo
  - `--private`: Flare to use if want to create a private repo
  - `--license`: To set the license for the repo

### Import a project as a Workspace
In order to import a Workspace you will use the next command:
`Workspace-auto -c import`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To set the name of the WorkSpace
- `--directory DIRECTORY`: Directory where the WorkSpace is located
- `--github`: Flare to use if you want to create a GitHub repo
- If `--github` was used:
  - `--owner`: To set the owner of the repo
  - `--private`: Flare to use if want to create a private repo
  - `--license`: To set the license for the repo

### Delete an existing Workspace
In order to import a Workspace you will use the next command:
`Workspace-auto -c delete`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To select by the name of the WorkSpace

### Open a Workspace
In order to open a Workspace you will use the next command:
`Workspace-auto -c open`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To select by the name of the WorkSpace

### Publish a Workspace to GitHub
In order to import a Workspace you will use the next command:
`Workspace-auto -c publish`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To select by the name of the WorkSpace
- `--owner`: To set the owner of the repo
- `--private`: Flare to use if want to create a private repo
- `--license`: To set the license for the repo

### Edit a Workspace
In order to import a Workspace you will use the next command:
`Workspace-auto -c import`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To select by the name of the WorkSpace
- `--add-apps`: Flare to activate the app adding prompt form
- `--del-apps`: Flare to activate the app deleting prompt form
- `--add-urls`: Flare to activate the url adding prompt form
- `--del-urls`: Flare to activate the url deleting prompt form

### Move a Workspace
In order to import a Workspace you will use the next command:
`Workspace-auto -c import`

You can also specify optional parameters instead of using the CLI prompted form.
The command will be able to use all of the next optional arguments:
- `--name NAME`: To select by the name of the WorkSpace
- `--new-directory`: To set the new directory to move the WorkSpace to.

### Re-Config the APP
In order to reconfigure the app you will use the next command:
`Workspace-auto -c config -sc SUBCOMMAND`

Aviable SUBCOMMANDS are with they're respective optional arguments are:
- `-sc vscode --vscode VSCODE`: VSCODE being the VSCODE type
- `-sc languages --set-up-languages SET_UP_LANGUAGES`: SET_UP_LANGUAGES being the languages you will use.
- `-sc directories` which has two flares:
  - `--custom-dir CUSTOM_DIR`: The main directory where the rest will be stored
  - `--create-directories`: A flare that determines if the directories will be created or selected.
- `-sc github-user --github-user GITHUB_USER`: Your GitHub username.
- `-sc api-key --api-key API_KEY`: Your GitHub API-KEY.

## :memo: Working on
Currently working on the first release for the application (0.1.0 following the convention of Mayor.Minor.Patch)

### Already planned releases

| VERSION | INCLUDES                          |
|---------|-----------------------------------|
|  0.1.0  | First Version                     |
|  0.2.0  | Multilingual support              |
|  0.3.0  | Up/Un for every installation type |
|  0.4.0  | Reestructure help message         |
|  0.5.0  | Code Review and Refactoring       |
|  1.0.0  | First Release Version             |

### On consideration
Right now we have three main things in consideration for future updates for this Application, which are:

- **URL/APP** saving on the go, making it easier to manage your workspaces
- **GitLab** support
- **More editors** support (like JetBrains IDE's and VisualStudio)
- **Custom .gitignore** adding all folders and files that are not usually wanted in your Repo's like tests or editor configurations.
- **Notion** support
- **Multilingual** support (May make the project collaborative)

Feel free to open Feature Requests [issues](https://github.com/Dtar380/WorkspaceAutomation/issues/new/choose) to request things related to this concepts such popular IDE's, popular Git services with REST API's (API needed for being able to give support), unwanted types of files and folders generated by WorkSpace creations, etc.

## :open_file_folder: Known Issues
The `-y, --yes` flag is not working, I know that and I am going to bring a fix soon this week.
We are knowledgeable that theres no way to update and uninstall the program via CLI itself if its not installed as a python module, this is not an error, it's jut not implemented yet.

## :scroll: License
WorkspaceAutomation is distributed under the GPL v3.0+ license.<br>
See the [LICENSE](LICENSE) file for more information.

## :money_with_wings: Sponsor this project
You can support me and the project with a donation to my Ko-Fi<br>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/H2H4TBMEZ)
