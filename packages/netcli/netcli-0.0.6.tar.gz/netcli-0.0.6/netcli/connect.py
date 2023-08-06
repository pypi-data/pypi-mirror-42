import time
import re
from os.path import expanduser, join
from threading import Thread
import json
import ipaddress
import difflib
import netmiko
from netcli.formatters import Spinner, color_string
from netcli.errors import NetcliError

TIMEOUT = 0.2


class ConnectThread(Thread):
    """
    Abstract Netmiko session to be run as separate thread
    """

    CONFIG_PATH = join(expanduser("~"), ".netcli.cfg")
    LOG_PATH = f'netcli_{time.strftime("%Y%m%d-%H%M%S")}.log'
    MAX_LINES = 1000
    GLOBAL_DELAY_FACTOR = 10
    TIMEOUT = 30

    def __init__(self, connection_config, custom_commands, queue):
        Thread.__init__(self)
        try:
            with open(self.CONFIG_PATH, 'r') as f:
                self.connection_defaults = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.connection_defaults = {}

        self.config = {
            'device_type':          connection_config['device_type'],
            'ip':                   self._get_target(connection_config['target']),
            'username':             connection_config['user'],
            'password':             connection_config['password'],
            'global_delay_factor':  self.connection_defaults.get('global_delay_factor', self.GLOBAL_DELAY_FACTOR),
            'timeout':              self.connection_defaults.get('timeout', self.TIMEOUT),
            'session_log':          self.connection_defaults.get('log_path', self.LOG_PATH),
        }
        self.custom_commands = custom_commands
        self.queue = queue
        self.connection = None

    def _get_target(self, target):
        '''Return target either is an IP or a fqdn, concatenating dns suffix'''
        try:
            ipaddress.ip_address(target)
            return target
        except ValueError:
            return target + self.connection_defaults.get('dns_suffix', "")

    def _establish(self):

        if self.config['password']:
            self.config['use_keys'] = False
        else:
            self.config['use_keys'] = True
            self.config['allow_agent'] = True

        try:
            return netmiko.ConnectHandler(**self.config)
        except Exception as error:
            raise NetcliError(f'ERROR: Unable to connect to device: {str(error)}')

    def _recommend_command(self, command):
        recommended_commands = difflib.get_close_matches(command, self.custom_commands.keys(), cutoff=0.3)
        response = ""
        for recommended_command in recommended_commands + [cmd for cmd in self.custom_commands.keys()
                                                           if (command in cmd and cmd not in recommended_commands)]:
            if response != "":
                response += ', '
            response += f'{recommended_command}'

        return response

    def _get_vendor_command(self, command):
        main_command = command.split("[")[0].strip()

        if main_command not in self.custom_commands:
            recommended_commands = self._recommend_command(main_command)
            response = f"Custom command {command} not recognized."
            if recommended_commands:
                response += f" Maybe you meant: {recommended_commands}"
            raise NetcliError(response)

        try:
            vendor_command = self.custom_commands[main_command]["types"][self.config['device_type']]
        except KeyError:
            raise NetcliError(f"Command {command} not implemented for vendor {self.config['type']}")

        return self._process_arguments(command, vendor_command)

    def _process_arguments(self, command, vendor_command):
        main_command = command.split("[")[0].strip()
        try:
            args_command = "[" + command.split("[")[1]
            regex = r"\[(.*?)\]"
            for arg in re.findall(regex, args_command):
                arg = arg.replace("[", "").replace("]", "")
                arg_key = arg.split(":")[0]
                if arg_key in self.custom_commands[main_command]["args"]:
                    try:
                        arg_value = arg.split(":")[1]
                    except IndexError:
                        arg_value = self.custom_commands[main_command]["args"][arg_key]
                    vendor_command = vendor_command.replace(f"[{arg_key}]", arg_value)
                else:
                    raise NetcliError(f"Unknown argument: {arg_key}")
        except IndexError:
            for arg_key in self.custom_commands[main_command]["args"]:
                arg_value = self.custom_commands[main_command]["args"][arg_key]
                vendor_command = vendor_command.replace(f"[{arg_key}]", arg_value)

        return vendor_command

    def _execute_command(self, requested_command):
        # Running raw vendor commands with "r- "
        if requested_command[0:3] == "r- ":
            vendor_command = requested_command[3:]
            raw = True
        else:
            raw = False
            # Getting vendor specific command from custom command
            vendor_command = self._get_vendor_command(requested_command.split(" | ")[0])

        with Spinner(f"- Running vendor command: {vendor_command}"):
            try:
                # response = self.connection.send_command(vendor_command)
                response = self.connection.send_command_timing(vendor_command)
            except netmiko.NetMikoTimeoutException as error:
                raise NetcliError(error)

        max_lines = self.connection_defaults.get('max_lines', self.MAX_LINES)
        response = "\n".join(response.split("\n")[:max_lines])

        if not raw:
            try:
                grep = requested_command.split(" | ")[1]
                grep_response = "\n"
                for line in response.split("\n"):
                    if grep in line:
                        grep_response += line
                response = grep_response
            except IndexError:
                pass

        return response

    def run(self):
        """
        Connect and run an interactive Netmiko session
        """
        try:
            self.connection = self._establish()
        except NetcliError as lacerror:
            self.queue.put((False, lacerror))
            return

        self.queue.put((True, ""))
        time.sleep(TIMEOUT)

        end_loop = False
        # Keeping the Netmiko session ongoing until user terminates cli session
        while not end_loop:
            requested_command = self.queue.get()[1]
            if requested_command.lower() in ['end', 'exit', 'quit']:
                end_loop = True
            else:
                try:
                    response = self._execute_command(requested_command)
                    success = True
                except NetcliError as nce:
                    success, response = False, nce
                self.queue.put((success, response))
            time.sleep(TIMEOUT)

        print(color_string(f"Disconnected from {self.config['ip']}. "
                           f"All your activity has been recorded in {self.config['session_log']}", 'yellow'))
