sublime-text-conda
==================
|travis|

sublime-text-conda is a Sublime Text plugin that allows users to work with Conda
directly within Sublime Text. Features include creating and removing Conda environments,
activating and deactivating Conda environments, and installing and removing Conda
packages.

Installation
============

sublime-text-conda can be found on the Package Control repository. To install the plugin
via Package Control, open the command palette, select `Package Control: Install Package`
and search for `Conda`. Package Control will then install the plugin and the plugin
settings will be located in the `Package Settings` submenu.

If you would rather install from source, simply run::

    $  git clone git@github.com:mandeep/sublime-text-conda.git

inside the Sublime Text packages folder.

Usage
=====

Once installed, Conda's commands will be located inside the command palette. These commands
include `Create Environment`, `Remove Environment`, `List Environments`, 
`Activate Environment`, `Deactivate Environment`,  `Install Package`, `Remove Package`,
and `List Packages`.

**Conda: Create Environment**

When selected from the command palette, `Conda: Create Environment` will provide an
input box for the name of the desired conda environment to create. Next, the command
palette will show the allowed Python versions to be used in the environment. Once the
Python version is selected, conda will create the specified environment.

**Conda: Remove Environment**

When selected from the command palette, `Conda: Remove Environment` will show all
available conda environments that are able to be removed. Once the environment
is selected, the build output will show the progress of the removal.

**Conda: List Environments**

When selected from the command palette, `Conda: List Environments` will display
inside the command palette all available conda environments.

**Conda: Activate Environment**

When selected from the command palette, `Conda: Activate Environment` will
display in the command pallete a list of available conda environments to be
activated. The selected conda environment will then be used in the build system.

**Conda: Deactivate Environment**

When selected from the command palette, `Conda: Dectivate Environment` will
display in the command palette the current active environment. When the environment
is selected, the build system will revert back to the Python that is located on PATH.

**Conda: Install Package**

When selected from the command palette, `Conda: Install Package` will provide an
input box for the name of the desired package to install. Once the package name
is typed, the build output will show the package installation progress.

**Conda: Remove Package**

When selected from the command palette, `Conda: Remove Package` will display in
the command palette, all available packages in the current conda environment. Once
the package is selected, the build output will show the package removal progress.

**Conda: List Packages**

When selected from the command palette, `Conda: List Packages` will display
inside the command palette all available packages inside the current conda
environment.

.. |travis| image:: https://img.shields.io/travis/mandeep/sublime-text-conda/master.svg
    :target: https://travis-ci.org/mandeep/sublime-text-conda