# Basic Usage
---
On this page you will have the basic documentation to start using **WorkSpace Automation**. This page will focus just on bare commands and will not teach any optional arguments, instead you will be filling out forms made from prompts to give the required information to the application.
<br>
<br>

## General Flares
---
### `-v, --version`
This will display the current version of the program.
<br>

### `-h, --help`
This will display the full help message of the program.
<br>

### `--update`
This will update the program to the latest release.
```{note}
This command right now only works if installed as a Python package
```

### `--uninstall`
This will uninstall the program and delete all of the program data.
```{note}
This command will not errase your projects and repositories
```

### `-k, --key <KEY>`
This is an optional argument which takes the key you gave during the set-up in order to decrypt the API-KEY for its later usage. If not introduced a prompt will diplay asking for the key.
```{note}
The program wont work if the key is not provided for security reasons
```
<br>

## WorkSpace Commands
---
To run a command you will use the next command:
- `Workspace-auto -c/--command <COMMAND>`

The possible commands are:
- `create`: usage will be `Workspace-auto -c create`
- `import`: usage will be `Workspace-auto -c import`
- `delete`: usage will be `Workspace-auto -c delete`
- `open`: usage will be `Workspace-auto -c open`
- `publish`: usage will be `Workspace-auto -c publish`
- `edit`: usage will be `Workspace-auto -c edit`
- `move`: usage will be `Workspace-auto -c move`
- `config`: usage will be `Workspace-auto -c config`
```{note}
The config command will also need the `-sc, --subcommand <SUB_COMMAND>` flare, this is covered in the advanced usage page.
```
