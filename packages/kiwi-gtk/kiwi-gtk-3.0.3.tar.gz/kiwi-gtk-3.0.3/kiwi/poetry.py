from poetry.plugins import Plugin


class MyPlugin(Plugin):

    def activate(self, poetry, io):
        version = self.get_custom_version()
        io.write_line("Setting package version to {}".format(version))

        poetry.package.version = version

    def get_custom_version(self):
        assert False
