import os

import sublime
import sublime_plugin


SETTINGS = sublime.load_settings('conda.sublime-settings')


class CondaCommand(sublime_plugin.WindowCommand):
    """Contains all of the methods that will be inherited by other commands."""

    def find_conda_environments(self):
        """Find all conda environments in the specified directory."""
        directory = os.path.expanduser(SETTINGS.get('environment_directory'))
        return [[environment, os.path.join(directory, environment)]
                for environment in os.listdir(directory)]


class ActivateCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to activate a conda environment."""

    def run(self):
        """Display 'Conda: Activate' in Sublime Text's command palette.

        When 'Conda: Activate' is clicked by the user, the command
        palette will show all available conda environments.
        """
        try:
            self.window.show_quick_panel(self.find_conda_environments(), "")
        except AttributeError:
            sublime.status_message("No conda environments found.")


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
                                     self.create_environment, None, None)

    def create_environment(self, environment):
        """Create a conda environment in the envs directory."""
        python = os.path.expanduser(SETTINGS.get('executable'))
        cmd = [python, '-m', 'conda', 'create', '--name', environment, '-y']
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
        try:
            self.window.show_quick_panel(self.find_conda_environments(),
                                         self.remove_environment)
        except AttributeError:
            sublime.status_message("No conda environments found.")

    def remove_environment(self, index):
        """Remove a conda environment from the envs directory."""
        if index != -1:
            python = os.path.expanduser(SETTINGS.get('executable'))
            environment = self.find_conda_environments()[index][0]
            cmd = [python, '-m', 'conda', 'remove', '--name', environment, '--all', '-y']
            self.window.run_command('exec', {'cmd': cmd})
