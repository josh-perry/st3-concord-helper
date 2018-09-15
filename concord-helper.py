import os
import sublime
import sublime_plugin

settings_file = "concord-helper.sublime-settings"
settings = sublime.load_settings(settings_file)


class CreateNewEcsFileCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
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

        if args["fileType"] == "component":
            window.show_input_panel("Component Name",
                                    "",
                                    self.component_on_done,
                                    None,
                                    None)
        elif args["fileType"] == "system":
            window.show_input_panel("System Name",
                                    "",
                                    self.system_on_done,
                                    None,
                                    None)

    def component_on_done(self, input):
        filename = "{0}.{1}".format(input, settings.get("language"))
        output_file = os.path.join(self.component_output_dir, filename)

        components_path = settings.get("project_concord_path") + ".component"
        data = {
            "components_path": components_path,
            "component_name": input
        }

        self.check_file(self.component_template, output_file, data)

    def system_on_done(self, input):
        filename = "{0}.{1}".format(input, settings.get("language"))
        output_file = os.path.join(self.system_output_dir, filename)

        system_path = settings.get("project_concord_path") + ".system"
        data = {
            "systems_path": system_path,
            "system_name": input,
            "component_requires": "",
            "component_list": "{Something, SomethingElse}",
            "system_callback": "draw"
        }

        self.check_file(self.system_template, output_file, data)

    def check_file(self, fileType, output_file, data):
        if os.path.isfile(output_file):
            status = "File already exists!"
            self.window.active_view().set_status("concord-helper", status)
            return False

        if self.write_file(fileType, data, output_file):
            self.window.open_file(output_file)
        else:
            status = "Failed to write to file!"
            self.window.active_view().set_status("concord-helper", status)

        return True

    def write_file(self, template, data, output_file):
        # Read template
        with open(template, 'r') as in_file:
            content = in_file.read()

            # Write template
            with open(output_file, 'w+') as out_file:
                out_file.write(content.format(**data))
                return True

        return False
