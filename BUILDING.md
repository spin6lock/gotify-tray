Get the source and install the requirements:

```shell
$ git clone https://github.com/seird/gotify-tray.git
$ cd gotify-tray
$ pip install -r requirements.txt
$ pip install pyinstaller
```

Currently it's only possible to create installer packages from the pyinstaller output. For any target platform, first create the executable with pyinstaller:

```shell
$ pyinstaller gotify-tray.spec
```


# Windows

## Create an installer with Inno Setup

Create an installer for windows with [inno setup](https://github.com/jrsoftware/issrc) from pyinstaller output:

```shell
$ iscc gotify-tray.iss
```

The installer is created at `inno-output/gotify-tray-installer.exe`.


# Linux

Packages can be created from the pyinstaller output with [fpm](https://fpm.readthedocs.io/). Run the `build_linux.sh` script with the desired package type:

## Create a deb package


```shell
$ ./build_linux.sh deb
```


## Create a pacman package


```shell
$ ./build_linux.sh pacman
```


# MacOS

## Create a macos .app

```shell
$ pip install pyinstaller Pillow
$ pyinstaller gotify-tray.spec
```

# Create and install a pip package

- Create the pip package:
    ```shell
    $ python -m build
    ```

- Install the pip package:
    ```shell
    $ pip install dist/gotify_tray-{{VERSION}}-py3-none-any.whl
    ```

- Launch from the command line:
    ```shell
    $ gotify-tray
    ```

# GitHub Releases (spin6lock fork)

The build workflow creates a Windows installer and a Python wheel. The wheel is
installed and checked with `gotify-tray --version` before it is uploaded.

Push a version tag to publish both files to this fork's GitHub Releases:

```shell
git tag v0.5.3
git push origin v0.5.3
```

For an existing tag, run the `release` workflow manually and provide that tag.
The tag must exist, and its GitHub Release must not already exist.
This fork's release workflow does not publish to the upstream PyPI project.
