from os.path import expanduser, join
import json
import yaml
from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE
from netcli.errors import NetcliError
from netcli.formatters import color_string


class Config:
    COMMANDS_PATH = join(expanduser("~"), ".my_netcli_commands.json")
    EXIT_WORDS = ["end", 'exit', 'save']

    CLI_HELP = """
CLI shortcuts:
  - Using 'r- ' you can run raw commands
  - Using ' | ' you can match specific words
"""

    def __init__(self):
        try:
            with open(self.COMMANDS_PATH, 'r') as f:
                self.custom_commands = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.custom_commands = {}

    def add(self, command):
        """
        Example: "custom_command arg1:default"
        [
            "ip table":
                "description": "what it is supposed to do",
                "args": {
                    "v": "4",
                    "vrf": "default"
                },
                "type": {
                    "junos": "show ip route vrf [vrf] ipv[v]",
                    "iosxr": "show ip route vrf [vrf] ipv[v]"
                }
        ]
        """

        custom_command, args = self._get_custom_command_and_args(command)

        if custom_command in self.custom_commands:
            print(color_string("Sorry, custom command {custom_command} already there.", 'red'))
            return

        self.custom_commands[custom_command] = {
            "args": {},
        }
        for arg in args:
            self.custom_commands[custom_command]['args'][arg[0]] = arg[1]

        self.custom_commands[custom_command]['description'] = input("\nPlease provide a useful description that"
                                                                    " will remind you what this command is"
                                                                    " supposed to do: \n")

        resp = input("\nDo you want to add a concrete vendor implementation (y/N)?")
        if resp.lower() not in ['y', 'yes']:
            print(color_string("Keep in mind that no actual implementation added", 'yellow'))
        else:
            self._define_vendor_commands(custom_command)

        self._save_to_file()
        print(color_string(f"Added command {command}", 'green'))

    def delete(self, command):

        res = self.custom_commands.pop(command, None)
        if not res:
            print(color_string("Command doesn't exit", 'red'))
            return

        self._save_to_file()
        print(color_string(f"Deleted command {command}", 'green'))

    @staticmethod
    def update():
        print(color_string(f"Update feature not available yet", 'red'))

    def show(self):
        print(yaml.dump(self.custom_commands, default_flow_style=False))

    def show_brief(self, cli=False):
        if cli:
            print(color_string(self.CLI_HELP, 'yellow'))
        if self.custom_commands:
            print(color_string("  - List of your custom commands:", 'yellow'))
            for command in self.custom_commands:
                print(color_string(f'    * {command}: {self.custom_commands[command]["description"]}', 'yellow'))

    def show_details(self, command):
        for custom_command in self.custom_commands:
            if command in custom_command:
                print(color_string(f' * {custom_command}: {self.custom_commands[custom_command]["description"]}',
                                   'yellow'))
                print(color_string(f'   {" " * len(custom_command)}  {self.custom_commands[custom_command]["args"]}',
                                   'yellow'))

    def _save_to_file(self):
        try:
            with open(self.COMMANDS_PATH, 'w') as destination_file:
                json.dump(self.custom_commands, destination_file)
        except Exception as error:
            raise NetcliError(error)

    def _define_vendor_commands(self, custom_command):
        vendor_commands = {}
        print("Time to add type implementation, hint: <type> - <command vrf [vrf]>. Remember to end/save")
        user_input = ""
        while user_input.lower() not in self.EXIT_WORDS:
            user_input = input(color_string("=> ", 'cyan'))
            if user_input in ['']:
                continue
            if user_input.lower() not in self.EXIT_WORDS:
                try:
                    vendor_type = user_input.split(" - ")[0]
                    if vendor_type not in CLASS_MAPPER_BASE:
                        print(color_string(f"Vendor type {vendor_type} not supported by Netmiko", 'red'))
                        continue

                    vendor_command = user_input.split(" - ")[1]
                    vendor_commands.update({vendor_type: vendor_command})
                except IndexError:
                    print(color_string("Your command is not following the proper pattern", 'red'))
        self.custom_commands[custom_command]["types"] = vendor_commands

    @staticmethod
    def _get_custom_command_and_args(command):
        fields = command.split()
        custom_command = []
        args = []
        for field in fields:
            if ":" in field:
                arg = field.split(":")
                args.append((arg[0], arg[1]))
                continue
            custom_command.append(field)

        return " ".join(custom_command), args
