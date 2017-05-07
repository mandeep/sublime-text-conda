import os

import sublime
import sublime_plugin


class CondaCommand(sublime_plugin.WindowCommand):
    """Contains all of the methods that will be inherited by other commands."""

    def __init__(self):
        """Initialize values from the settings file."""
        self.settings = sublime.load_settings('conda.sublime-settings')
        self.executable = self.settings.get('executable')
        self.environments = self.settings.get('environment_directory')

    def find_conda_environments(self):
        """Find all conda environments in the specified directory."""
        return [environment for environment in os.listdir(self.environments)]
