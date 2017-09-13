import os
import subprocess
import sys

import json

import sublime
import sublime_plugin

import Default


class CondaCommand(sublime_plugin.WindowCommand):
    """Contains all of the attributes that will be inherited by other commands."""

    @property
    def settings(self):
        """Load the plugin settings for commands to use."""
        return sublime.load_settings('conda.sublime-settings')

    @property
    def executable(self):
        """Retrieve the python executable path from settings."""
        return os.path.expanduser(self.settings.get('executable'))

    @property
    def configuration(self):
        """Retrieve the conda configuration file from settings."""
        return os.path.expanduser(self.settings.get('configuration'))

    @property
    def root_directory(self):
        """Retrieve the directory of conda's root environment."""
        if sys.platform == 'win32':
            root_directory = os.path.dirname(self.executable)
        else:
            root_directory = os.path.dirname(self.executable).replace('bin', '')

        return root_directory

    @property
    def conda_environments(self):
        """Find all conda environments in the specified directory."""
        directory = os.path.expanduser(self.settings.get('environment_directory'))

        environments = [['root', self.root_directory]]

        for environment in os.listdir(directory):
            environment_path = os.path.join(directory, environment)
            # conda 4.4 added a _run environment so it needs to be excluded
            if os.path.isdir(environment_path) and environment != '_run':
                environments.append([environment, environment_path])

        return environments

    @property
    def project_data(self):
        """Retrieve the project data to be used in the current window."""
        if self.window.project_data() is None:
            return {}
        else:
            return self.window.project_data()

    @property
    def startupinfo(self):
        """Property used to hide command prompts when on Windows platforms."""
        startupinfo = None

        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()

            if sys.version_info.major == 3:
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            else:
                startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

        return startupinfo

    def retrieve_environment_name(self, path):
        """Retrieve the environment name from the active environment path.

        If the active environment is the root environment, 'root' must be
        returned instead of the basename from the environment path.
        """
        if path == self.root_directory:
            return 'root'
        else:
            return os.path.basename(path)


class CreateCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to create a conda environment."""

    def run(self):
        """Display 'Conda: Create' in Sublime Text's command palette.

        When 'Conda: Create' is clicked by the user, Sublime's text input
        box will show allowing the user to input the name of environment.
        This environment name is then passed to the create_environment
        method.
        """
        self.window.show_input_panel('Conda Environment Name:', '',
                                     self.retrieve_python_version, None, None)

    def retrieve_python_version(self, environment):
        """Display a list of available Python versions for the environment.

        Forcing the user to select the Python version allows conda to create
        a new Python executable inside the environment directory.
        """
        self.environment = environment

        python_versions = ['Python 2.7', 'Python 3.5', 'Python 3.6']

        self.window.show_quick_panel(python_versions, self.create_environment)

    def create_environment(self, index):
        """Create a conda environment in the envs directory."""
        if index != -1:
            if index == 0:
                python_version = 'python=2.7'
            elif index == 1:
                python_version = 'python=3.5'
            else:
                python_version = 'python=3.6'

            cmd = [self.executable, '-m', 'conda', 'create',
                   '--name', self.environment, python_version, '-y', '-q']

            self.window.run_command('exec', {'cmd': cmd})


class RemoveCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to remove a conda environment."""

    def run(self):
        """Display 'Conda: Remove' in Sublime Text's command palette.

        When 'Conda: Removed' is clicked by the user, the command
        palette whill show all conda environments available for removal.
        The index of the selected environment is then passed to the
        remove_environment method"
        """
        self.window.show_quick_panel(self.conda_environments,
                                     self.remove_environment)

    def remove_environment(self, index):
        """Remove a conda environment from the envs directory."""
        if index != -1:
            environment = self.conda_environments[index][0]

            cmd = [self.executable, '-m', 'conda', 'remove',
                   '--name', environment, '--all', '-y', '-q']

            self.window.run_command('exec', {'cmd': cmd})


class ListCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to list available conda environments."""

    def run(self):
        """Display 'Conda: List' in Sublime Text's command palette.

        When 'Conda: List' is clicked by the user, the command
        palette will show all available conda environments.
        """
        self.window.show_quick_panel(self.conda_environments,
                                     None)


class ActivateCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to activate a conda environment."""

    def run(self):
        """Display 'Conda: Activate' in Sublime Text's command palette.

        When 'Conda: Activate' is clicked by the user, the command
        palette will show all available conda environments. The
        clicked environment will be activated as the current environment.
        """
        self.window.show_quick_panel(self.conda_environments,
                                     self.activate_environment)

    def activate_environment(self, index):
        """Activate the environment selected from the command palette."""
        if index != -1:
            project_data = self.project_data

            project_data['conda_environment'] = self.conda_environments[index][1]

            self.window.set_project_data(project_data)

            sublime.status_message('Activated conda environment: {}'
                                   .format(self.conda_environments[index][0]))


class DeactivateCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to deactivate a conda environment."""

    def run(self):
        """Display 'Conda: Deactivate' in Sublime Text's command palette.

        When 'Conda: Deactivate' is clicked by the user, the command
        palette will show all available conda environments. The
        clicked environment will be deactivated.
        """
        self.window.show_quick_panel(self.active_environment,
                                     self.deactivate_environment)

    @property
    def active_environment(self):
        """Retrieve the active conda environment."""
        try:
            environment_path = self.project_data['conda_environment']
            environment_name = self.retrieve_environment_name(environment_path)

            return [[environment_name, os.path.dirname(environment_path)]]

        except KeyError:
            return ['No Active Conda Environment']

    def deactivate_environment(self, index):
        """Deactivate the environment selected in the command palette."""
        if index != -1:
            try:
                project_data = self.project_data

                del project_data['conda_environment']

                self.window.set_project_data(project_data)

                sublime.status_message('Deactivated conda environment: {}'
                                       .format(self.conda_environments[index][0]))
            except KeyError:
                sublime.status_message('No active conda environment')


class ListCondaPackageCommand(CondaCommand):
    """Contains all of the methods needed to list all installed packages."""

    def run(self):
        """Display 'Conda: List' in Sublime Text's command palette.

        When 'Conda: List' is clicked by the user, the build output
        displays all packages installed in the current environment.
        """
        self.window.show_quick_panel(self.environment_packages, None)

    @property
    def environment_packages(self):
        """List each package name and version installed in the environment."""
        try:
            environment_path = self.project_data['conda_environment']
            environment = self.retrieve_environment_name(environment_path)

            package_data = subprocess.check_output([self.executable, '-m', 'conda', 'list',
                                                    '--name', environment, '--json'],
                                                   startupinfo=self.startupinfo)

            packages_info = json.loads(package_data.decode())
            packages = [[package['name'], package['dist_name']]
                        for package in packages_info]

            return packages
        except KeyError:
            return ['No Active Conda Environment']


class InstallCondaPackageCommand(CondaCommand):
    """Contains all of the methods needed to install a conda package."""

    def run(self):
        """Display an input box allowing the user to input a package name."""
        self.window.show_input_panel('Package Name:', '', self.install_package,
                                     None, None)

    def install_package(self, package):
        """Install the given package name via conda."""
        try:
            environment_path = self.project_data['conda_environment']
            environment = self.retrieve_environment_name(environment_path)
            cmd = [self.executable, '-m', 'conda', 'install', package,
                   '--name', environment, '-y', '-q']
            self.window.run_command('exec', {'cmd': cmd})
        except KeyError:
            sublime.status_message('No active conda environment.')


class RemoveCondaPackageCommand(CondaCommand):
    """Contains all of the methods needed to remove a conda package."""

    def run(self):
        """Display an input box allowing the user to pick a package to remove."""
        self.window.show_quick_panel(self.environment_packages, self.remove_package)

    @property
    def environment_packages(self):
        """List each package name and version installed in the environment.

        This property had to be duplicated as the attribute from
        ListCondaPackageCommand could not be inherited properly.
        """
        try:
            environment_path = self.project_data['conda_environment']
            environment = self.retrieve_environment_name(environment_path)

            package_data = subprocess.check_output([self.executable, '-m', 'conda', 'list',
                                                    '--name', environment, '--json'],
                                                   startupinfo=self.startupinfo)

            packages_info = json.loads(package_data.decode())
            packages = [[package['name'], package['dist_name']]
                        for package in packages_info]

            return packages
        except KeyError:
            return ['No Active Conda Environment']

    def remove_package(self, index):
        """Remove the given package name via conda."""
        if index != -1:
            package_to_remove = self.environment_packages[index][0]

            environment_path = self.project_data['conda_environment']

            environment = self.retrieve_environment_name(environment_path)

            cmd = [self.executable, '-m', 'conda', 'remove', package_to_remove,
                   '--name', environment, '-y', '-q']

            self.window.run_command('exec', {'cmd': cmd})


class ListCondaChannelsCommand(CondaCommand):
    """Contains all of the methods needed to display conda's channel sources."""

    def run(self):
        """Display 'Conda: List Channel Sources' in Sublime Text's command palette.

        When 'Conda: List Channel Sources' is clicked by the user,
        the command palette displays all of the channel sources found
        in the condarc configuration file.
        """
        self.window.show_quick_panel(self.channel_sources, None)

    @property
    def channel_sources(self):
        """List each channel source found in the condarc configuration file."""
        sources = subprocess.check_output([self.executable, '-m', 'conda', 'config',
                                          '--show-sources', '--json'],
                                          startupinfo=self.startupinfo)
        sources = json.loads(sources.decode())

        try:
            return sources[self.configuration]['channels']
        except KeyError:
            return ['No Channel Sources Available']


class SearchCondaPackageCommand(CondaCommand):
    """Contains all of the methods needed to search for a conda package."""

    def run(self):
        """Display an input box allowing the user to input a package name."""
        self.window.show_input_panel('Package Name:', '', self.search_package,
                                     None, None)

    def search_package(self, package):
        """Search for a package included in the defaults channel."""
        cmd = [self.executable, '-m', 'conda', 'search', package]
        self.window.run_command('exec', {'cmd': cmd})


class AddCondaChannelCommand(CondaCommand):
    """Contains all of the methods needed to add a conda channel source."""

    def run(self):
        """Display 'Conda: Add Channel Source' in Sublime Text's command palette.

        When 'Conda: Add Channel Source' is clicked by the user,
        an input box will show allowing the user to type the name
        of the channel to add.
        """
        self.window.show_input_panel('Conda Channel Name:', '',
                                     self.add_channel, None, None)

    def add_channel(self, channel):
        """Add the given channel to the condarc configuration file."""
        cmd = [self.executable, '-m', 'conda', 'config', '--add',
               'channels', channel]

        self.window.run_command('exec', {'cmd': cmd})


class RemoveCondaChannelCommand(CondaCommand):
    """Contains all of the methods needed to remove a conda channel source."""

    def run(self):
        """Display 'Conda: Remove Channel Source' in Sublime Text's command palette.

        When 'Conda: Remove Channel Source' is clicked by the user,
        the command palette will show a list of channel sources
        available to be removed by the user.
        """
        self.window.show_quick_panel(self.channel_sources, self.remove_channel)

    @property
    def channel_sources(self):
        """List each channel source found in the condarc configuration file.

        This property had to be duplicated as the attribute from
        ListCondaChannelCommand could not be inherited properly.
        """
        sources = subprocess.check_output([self.executable, '-m', 'conda', 'config',
                                          '--show-sources', '--json'],
                                          startupinfo=self.startupinfo)
        sources = json.loads(sources.decode())

        try:
            return sources[self.configuration]['channels']
        except KeyError:
            return ['No Channel Sources Available']

    def remove_channel(self, index):
        """Remove a channel from the condarc configuration file."""
        if index != -1:
            channel = self.channel_sources[index]

            cmd = [self.executable, '-m', 'conda', 'config', '--remove',
                   'channels', channel]

            self.window.run_command('exec', {'cmd': cmd})


class ExecuteCondaEnvironmentCommand(CondaCommand):
    """Override Sublime Text's default ExecCommand with a targeted build."""

    def run(self, **kwargs):
        """Run the current Python file with the conda environment's Python executable.

        The activated conda environment is retrieved from the Sublime Text
        window project data. The Python executable found in the conda
        environment's bin directory is used to build the file.
        """
        try:
            environment = self.project_data['conda_environment']
            
            if sys.platform == 'win32':
                executable_path = '{}\\python' .format(environment)
            else:
                executable_path = '{}/bin/python' .format(environment)

            kwargs['cmd'][0] = os.path.normpath(executable_path)
        except KeyError:
            pass

        self.window.run_command('exec', kwargs)
