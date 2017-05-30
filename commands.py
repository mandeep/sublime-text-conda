import os
import sys

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
    def conda_environments(self):
        """Find all conda environments in the specified directory."""
        directory = os.path.expanduser(self.settings.get('environment_directory'))

        environments = [[environment, os.path.join(directory, environment)]
                        for environment in os.listdir(directory)]

        if len(environments) > 0:
            return environments
        else:
            return ['No Conda Environments Found']


class ListCondaEnvironmentCommand(CondaCommand):
    """Contains all of the methods needed to list all installed packages."""

    def run(self):
        """Display 'Conda: List' in Sublime Text's command palette.

        When 'Conda: List' is clicked by the user, the build output
        displays all packages installed in the current environment.
        """
        self.window.show_quick_panel(self.environment_packages, None)

    @property
    def environment_packages(self):
        """"""
        cmd = [self.executable, '-m', 'conda', 'list']

        try:
            environment_path = self.window.project_data()['conda_environment']
            environment = os.path.basename(environment_path)
            cmd.extend(['--name', environment])
        except KeyError:
            pass

        self.window.run_command('exec', {'cmd': cmd})


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
            project_data = self.window.project_data()

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
        try:
            environment = self.window.project_data()['conda_environment']
            return [[os.path.basename(environment), os.path.dirname(environment)]]
        except KeyError:
            return ['No Active Conda Environment']

    def deactivate_environment(self, index):
        """Deactivate the environment selected in the command palette."""
        sublime.status_message('Deactivated conda environment: {}'
                               .format(self.conda_environments[index][0]))

        project_data = self.window.project_data()

        try:
            del project_data['conda_environment']
        except KeyError:
            sublime.status_message('No active conda environment')

        self.window.set_project_data(project_data)


class InstallCondaPackageCommand(CondaCommand):
    """Install a Python package via conda."""

    def run(self):
        """Display an input box allowing the user to input a package name."""
        self.window.show_input_panel('Package Name:', '', self.install_package,
                                     None, None)

    def install_package(self, package):
        """Install the given package name via conda."""
        try:
            environment_path = self.window.project_data()['conda_environment']
            environment = os.path.basename(environment_path)
            cmd = [self.executable, '-m', 'conda', 'install', package,
                   '--name', environment, '-y', '-q']
        except KeyError:
            pass

        self.window.run_command('exec', {'cmd': cmd})


class RemoveCondaPackageCommand(CondaCommand):
    """Remove a Python package via conda."""

    def run(self):
        """Display an input box allowing the user to input a package name."""
        self.window.show_input_panel('Package Name:', '', self.remove_package,
                                     None, None)

    def remove_package(self, package):
        """Remove the given package name via conda."""
        try:
            environment_path = self.window.project_data()['conda_environment']
            environment = os.path.basename(environment_path)
            cmd = [self.executable, '-m', 'conda', 'remove', package,
                   '--name', environment, '-y', '-q']
        except KeyError:
            pass

        self.window.run_command('exec', {'cmd': cmd})


class ExecuteCondaEnvironmentCommand(Default.exec.ExecCommand):
    """Override Sublime Text's default ExecCommand with a targeted build."""

    def run(self, **kwargs):
        """Run the current Python file with the conda environment's Python executable.

        The activated conda environment is retrieved from the Sublime Text
        window project data. The Python executable found in the conda
        environment's bin directory is used to build the file.
        """
        try:
            environment = self.window.project_data()['conda_environment']
            
            if sys.platform == 'win32':
                executable_path = '{}\\python' .format(environment)
            else:
                executable_path = '{}/bin/python' .format(environment)

            kwargs['cmd'][0] = os.path.normpath(executable_path)
        except KeyError:
            pass

        super(ExecuteCondaEnvironmentCommand, self).run(**kwargs)
