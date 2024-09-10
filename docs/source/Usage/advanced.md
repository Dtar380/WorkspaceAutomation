# Advanced Usage
---
On this page you will have the advanced documentation to use **WorkSpace Automation**. This page contains all the optional arguments and sub-commands and with which commands you can use them.
<br>
<br>

## Sub-command (`-sc, --subcommand <SUB_COMMAND>`)
This flare is required to use the `config` command, if not provided or wrongly tipped it will throw an error.

The aviable sub commands are:
- `vscode`: usage will be `Workspace-auto -c config -sc vscode`
- `languages`: usage will be `Workspace-auto -c config -sc languages`
- `directories`: usage will be `Workspace-auto -c config -sc directories`
- `github-user`: usage will be `Workspace-auto -c config -sc github-user`
- `api-key`: usage will be `Workspace-auto -c config -sc api-key`

The optional arguments that you can provide to this commands are the same than the ones for doing the [set-up](../GettingStarted/setup.md) of the program
<br>
<br>

## WorkSpace Arguments

### `--name <NAME>`
Where NAME is the name of the workspace.<br>
This can be used with all the commands except `config`
<br>

### `--directory <DIRECTORY>`
Where DIRECTORY is the directory with the Workspace will be located.<br>
This can be used with the next commands:
- `create`
- `import`
```{note}
The directory must be one of the directories included on the set-up of the program.
```

### `--language <LANGUAGE>`
Where LANGUAGE is the language of the project.<br>
This can be used with the next commands:
- `create`
- `import`
```{note}
The language must be one of the languages selected on the set-up of the program.
```
<br>

## GitHub Arguments

### `--github`
Include this argument if you want to create a GitHub repository.<br>
This can be used with the next commands:
- `create`
- `import`
<br>

### `--owner <OWNER>`
Where OWNER is the owner of the repository.<br>
This can be used with the next commands:
- `create`
- `import`
- `publish`
```{note}
The Owner must be either yourself or a organization in which you have permision to create repositories.
```

### `--private`
Include this argument if you want the repository to be private.<br>
This can be used with the next commands:
- `create`
- `import`
- `publish`
<br>

### `--license <LICENSE>`
Where LICENSE is the license to be used for the repository.<br>
This can be used with the next commands:
- `create`
- `import`
- `publish`

There are 3 licenses aviable on this moments:
- `Unlicense`: If you do not want to use a license
- `MIT`
- `GPL-3.0`
<br>
<br>

## WorkSpace Edition Arguments

### `--add-apps`
Include this argument if you want to show the prompt to add APPs to the workspaces.<br>
This can only be used with the `edit` command.
<br>

### `--del-apps`
Include this argument if you want to show the prompt to delete APPs from the workspaces.<br>
This can only be used with the `edit` command.
<br>

### `--add-urls`
Include this argument if you want to show the prompt to add URLs to the workspaces.<br>
This can only be used with the `edit` command.
<br>

### `--del-urls`
Include this argument if you want to show the prompt to delete URLs from the workspaces.<br>
This can only be used with the `edit` command.
<br>

### `--new-directory <NEW_DIRECTORY>`
Where NEW_DIRECTORY is the directory where you want to relocate the WorkSpace.<br>
This can only be used with the `move` command.
```{note}
The directory must be one of the directories included on the set-up of the program.
```
