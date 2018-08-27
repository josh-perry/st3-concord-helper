import os
import sublime
import sublime_plugin


settings_file = "concord-helper.sublime-settings"
settings = sublime.load_settings(settings_file)


class CreateNewEcsFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window

        language = settings.get("language")
        base = os.path.dirname(os.path.realpath(__file__))
        self.templates_path = os.path.join(base, "templates", language)

        f = "component.{0}".format(language)
        self.component_template = os.path.join(self.templates_path, f)

        f = "system.{0}".format(language)
        self.system_template = os.path.join(self.templates_path, f)

        project_path = window.extract_variables()["project_path"]

        s = settings.get("output_directories")
        self.component_output_dir = os.path.join(project_path, s["components"])
        self.system_output_dir = os.path.join(project_path, s["systems"])

        window.show_input_panel("Name", "", self.component_on_done, None, None)

    def component_on_done(self, input):
        window = self.window

        filename = "{0}.{1}".format(input, settings.get("language"))
        output_file = os.path.join(self.component_output_dir, filename)

        if os.path.isfile(output_file):
            status = "File already exists!"
            window.active_view().set_status("concord-helper", status)
            return

        data = {
            "components_path": settings.get("project_concord_path"),
            "component_name": input
        }

        if self.write_file(data, output_file):
            window.open_file(output_file)
        else:
            status = "Failed to write to file!"
            window.active_view().set_status("concord-helper", status)

    def write_file(self, data, output_file):
        # Read template
        with open(self.component_template, 'r') as in_file:
            content = in_file.read()

            # Write template
            with open(output_file, 'w+') as out_file:
                out_file.write(content.format(**data))
                return True

        return False
