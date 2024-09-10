# Installation
---
In this part of the tutorial you will learn all the different ways to install WorkSpace Automation and how to do it. There are three ways to install the application:
- [Python Package](#python-package)
- [Built application](#built-application)
- [Build from source](#build-from-source)

```{note}
Both python package and building the app your self are not recommended for unexperienced developers, unless you're willing to search for further guidance your self.
```
<br>

## Python package
---
For installing the application as a python package you need to do the next steeps:
- First install `python 3.12.4`.
- Then set `python 3.12.4` as the main python version in your PATH environment variables.
- At last install the package using `pip install WorkSpaceAutomation`.
<br>
<br>

## Built application
---
```{warning}
This method is not aviable on this moments.
```
For installing the application already built you need to do the next steps:
- First go to the latest release page. [Here](https://github.com/Dtar380/WorkspaceAutomation/releases/latest)
- Then download the installer for your operating system. (e.j `.exe` if you are in Windows)
- At last run the installer.
<br>
<br>

## Build from source
---
For building the app from the source code your self you need to do the next steps:
- First go to the latest release page. [Here](https://github.com/Dtar380/WorkspaceAutomation/releases/latest)
- Then download the `source.zip` file and unzip the file on a custom directory.
- Now make sure you're running on python 3.12.4 (run `python --version`)
- After that install the required packages running `python -m pip install -r requirements_dev.txt`.
- At last run `python -m pip install -e .` inside the directory of the source.

```{warning}
Do not errase or modify the code form the source folder as the python package has been installed locally and it is running from that source code.
```
