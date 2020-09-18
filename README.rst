.. image:: header.png

|travis| |release| |downloads| |license|

sublime-text-conda is a Sublime Text plugin that allows users to work with conda
directly within Sublime Text. Features include creating and removing conda environments,
activating and deactivating conda environments, and installing and removing conda
packages.

Installation
============

sublime-text-conda can be found on the Package Control repository. To install the plugin
via Package Control, open the command palette, select `Package Control: Install Package`
and search for `conda`. Package Control will then install the plugin and the plugin
settings will be located in the `Package Settings` submenu.

If you would rather install from source, simply run::

    $  git clone git@github.com:mandeep/sublime-text-conda.git

inside the Sublime Text packages folder. To find this folder, open Sublime Text and click
on `Preferences->Browse Packages`. Cloning in this directory will manually install the plugin.
Once you have cloned the repository inside the packages folder, be sure to rename the folder from
`sublime-text-conda` to `Conda`.
For more information please visit https://www.sublimetext.com/docs/3/packages.html

Settings
========

The settings file can be found in `Preferences->Package Settings->Conda->Settings - Default`. The
paths may need to be changed depending on where you've installed anaconda/miniconda. For Windows
users, the additional settings of `run_through_shell` and `use_pythonw` are available for when
working on projects that require a GUI to open (such as showing a matplotlib plot).

Usage
=====

Once installed, a ``Conda`` build system will appear in the build sytem menu and conda's commands will be located inside the command palette. The ``Conda`` build system must be selected in order to use the commands. These commands include ``Create Environment``, ``Remove Environment``, ``List Environments``, ``Activate Environment``, ``Deactivate Environment`` ``Open REPL``, ``Install Package``, ``Remove Package``, ``List Packages``, ``Add Channel Source``, ``Remove Channel Source``, and ``List Channel Sources``. Command names for key bindings can be found `here <Default.sublime-commands>`_.

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

**Conda: Open REPL**

When selected from the command palette, `Conda: Open REPL` will
open a REPL tab with the currently opened file within the activated Conda
environment.

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

**Conda: Add Channel Source**

When selected from the command palette, `Conda: Add Channel Source` will provide an
input box for the name of the desired channel to add. Once the channel
is typed, the build output will show the channel source progress.

**Conda: Remove Channel Source**

When selected from the command palette, `Conda: Remove Channel Source` will display
inside the command palette all available channel sources to remove. Once clicked,
the selected channel source remove from the conda configuration file.

**Conda: List Channel Sources**

When selected from the command palette, `Conda: List Channel Sources` will display
inside the command palette all channel sources listed inside the conda configuration
file.

.. |travis| image:: https://img.shields.io/travis/mandeep/sublime-text-conda/master.svg?style=flat-square
    :target: https://travis-ci.org/mandeep/sublime-text-conda

.. |release| image:: https://img.shields.io/github/release/mandeep/sublime-text-conda.svg?style=flat-square
    :target: https://github.com/mandeep/sublime-text-conda/releases

.. |license| image:: https://img.shields.io/github/license/mandeep/sublime-text-conda.svg?style=flat-square
    :target: https://github.com/mandeep/sublime-text-conda/blob/master/LICENSE

.. |downloads| image:: https://img.shields.io/packagecontrol/dt/Conda.svg?style=flat-square
    :alt: Package Control
    :target: https://packagecontrol.io/packages/Conda
