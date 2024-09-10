# Set-Up
---
In this part of the tutorial you will learn how to set-up the application. There are two ways to set-up the application:
- Using inline command
- Using the prompted form

```{warning}
Do not stop the program while setting it up, this may cause issues. It it stops without giving an error you might need to reinstall the program.
```
<br>

To set-up the app by using just one command you will need to do the next steps:
- First run `Workspace-auto --update` (only if it was installed as a python package)
- Then run `Workspace-auto --init`.
Here is where you have the two paths where you can either just run the --init argument and complete the prompted form, or use optional arguments to skip the propmts.
<br>

For this you will need to know the next arguments:
- `--vscode VSCODE`: VSCODE being the VSCODE type
- `--set-up-languages SET_UP_LANGUAGES`: SET_UP_LANGUAGES being the languages you will use.
  - `--custom-dir CUSTOM_DIR`: The main directory where the rest will be stored
  - `--create-directories`: A flare that determines if the directories will be created or selected.
- `--github-user GITHUB_USER`: Your GitHub username.
- `--api-key API_KEY`: Your GitHub API-KEY.
