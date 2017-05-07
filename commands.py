import os

import sublime
import sublime_plugin


SETTINGS = sublime.load_settings('conda.sublime-settings')


class CondaCommand(sublime_plugin.WindowCommand):
    """Contains all of the methods that will be inherited by other commands."""

    def find_conda_environments(self):
        """Find all conda environments in the specified directory."""
        directory = os.path.expanduser(SETTINGS.get('environment_directory'))
        return [environment for environment in os.listdir(directory)]


class ActivateCondaEnvironmentCommand(CondaCommand):
    """Contains the methods needed to activate a conda environment."""

    def run(self):
        """Display 'Conda: Activate' in Sublime Text's command palette."""
        self.window.show_quick_panel(self.find_conda_environments(), "")
