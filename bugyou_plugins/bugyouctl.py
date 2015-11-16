import cmd
import ConfigParser
import importlib


CONFIG_PATH = '/etc/bugyou/plugins.conf'

class CommandPrompt(cmd.Cmd):

    def __init__(self, *args, **kwargs):
        self.prompt = 'bugyou> '
        self.load_config()
        cmd.Cmd.__init__(self, *args, **kwargs)

    def load_config(self):
        self.parser = ConfigParser.RawConfigParser()
        self.parser.read(CONFIG_PATH)

    def do_start(self, args):
        if not args:
            return 1
        self.parse_plugin_config(args)

    def parse_plugin_config(self, args):
        plugins = args.split()
        sections = self.parser.sections()

        for plugin in plugins:
            if plugin not in sections:
                logging.info('Invalid plugin name: %s' % plugin)
                continue

            topic = self.parser.get(plugin, 'topic')
            klasspath = self.parser.get(plugin, 'klass')
            self.load_plugin(klasspath)

    def load_plugin(self, klasspath):
        path, klass = klasspath.split(':')
        module = importlib.import_module(path)

        if hasattr(module, klass):
            plugin_obj = getattr(module, klass)()

    def do_EOF(self, args):
        return 1

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        return 1

def main():
    prompt = CommandPrompt()
    prompt.cmdloop()

if __name__ == '__main__':
    main()
