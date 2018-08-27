import sublime
import sublime_plugin

settings_file = "concord-helper.sublime-settings"
settings = sublime.load_settings(settings_file)


class CreateNewComponentCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)

        s = settings.get("output_directories")
        self.component_output_directory = s["components"]

    def run(self, edit):
        window = self.view.window()

        component_file = window.new_file()
        component_file.insert(edit, 0, self.component_output_directory)
