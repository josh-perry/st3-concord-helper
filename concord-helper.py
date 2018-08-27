import os
import sublime
import sublime_plugin


settings_file = "concord-helper.sublime-settings"
settings = sublime.load_settings(settings_file)


class CreateNewComponentCommand(sublime_plugin.WindowCommand):
    def run(self):
        language = settings.get("language")
        base = os.path.dirname(os.path.realpath(__file__))
        self.templates_path = os.path.join(base, "templates", language)

        f = "component.{0}".format(language)
        self.component_template = os.path.join(self.templates_path, f)

        f = "system.{0}".format(language)
        self.system_template = os.path.join(self.templates_path, f)

        project_path = self.window.extract_variables()["project_path"]
        s = settings.get("output_directories")
        self.component_output_dir = os.path.join(project_path, s["components"])

        self.window.show_input_panel("Name", "", self.on_done, None, None)

    def on_done(self, input):
        window = self.window

        filename = "{0}.{1}".format(input, settings.get("language"))
        output_file = os.path.join(self.component_output_dir, filename)

        if os.path.isfile(output_file):
            status = "Component file already exists!"
            window.active_view().set_status("concord-helper", status)
            return

        # Read template
        with open(self.component_template, 'r') as in_file:
            content = in_file.read()

            # Write template
            with open(output_file, 'w+') as out_file:
                out_file.write(content)
                window.open_file(output_file)
