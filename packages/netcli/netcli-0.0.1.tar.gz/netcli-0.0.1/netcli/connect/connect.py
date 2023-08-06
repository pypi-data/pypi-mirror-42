import time
import re
from threading import Thread
import netmiko
from netcli.formatters import Spinner, color_string
from netcli.errors import NetcliError

TIMEOUT = 0.2


class ConnectThread(Thread):
    """
    Abstract Netmiko session to be run as separate thread
    """
    def __init__(self, connection_config, custom_commands, queue):
        Thread.__init__(self)
        self.target = connection_config['target']
        self.user = connection_config['user']
        self.password = connection_config['password']
        self.type = connection_config['device_type']
        self.custom_commands = custom_commands
        self.queue = queue
        self.connection = None

    def _establish(self):
        config = {
            'device_type':          self.type,
            'ip':                   self.target,
            'username':             self.user,
            'global_delay_factor':  10,
            'timeout':              30,
        }

        if self.password:
            config['password'] = self.password
            config['use_keys'] = False
        else:
            config['use_keys'] = True
            config['allow_agent'] = True

        try:
            return netmiko.ConnectHandler(**config)
        except Exception as error:
            raise NetcliError(f'ERROR: Unable to connect to device: {str(error)}')

    def _get_vendor_command(self, command):
        args = True
        main_command = command.split("[")[0].strip()

        if main_command not in self.custom_commands:
            print(color_string(f"Custom command {command} not recognized. Use help", "red"))
            return None

        try:
            vendor_command = self.custom_commands[main_command]["types"][self.type]
        except KeyError:
            print(color_string(f"Command {command} not implemented for vendor {self.type}", "red"))
            return None

        try:
            args_command = "[" + command.split("[")[1]
        except IndexError:
            args = False

        if args:
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
                    print(color_string(f"Unknown argument: {arg_key}", 'red'))
                    return None
        else:
            for arg_key in self.custom_commands[main_command]["args"]:
                arg_value = self.custom_commands[main_command]["args"][arg_key]
                vendor_command = vendor_command.replace(f"[{arg_key}]", arg_value)

        return vendor_command

    def _execute_command(self, requested_command):
        # Running raw vendor commands with "r- "
        if requested_command[0:3] == "r- ":
            vendor_command = requested_command[3:]
            grep = False
        else:
            # Getting vendor specific command from custom command
            vendor_command = self._get_vendor_command(requested_command.split(" | ")[0])
            try:
                grep = requested_command.split(" | ")[1]
            except IndexError:
                grep = False

        raw = ""
        success = True
        if vendor_command:
            with Spinner(f"- Running vendor command: {vendor_command}"):
                try:
                    raw = self.connection.send_command(vendor_command)
                except netmiko.NetMikoTimeoutException as error:
                    raw = error
                    success = False

        if grep:
            response = "\n"
            for line in raw.split("\n"):
                if grep in line:
                    response += line
        else:
            response = raw

        return success, response

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
            command = self.queue.get()
            requested_command = command[1]
            if requested_command.lower() in ['end', 'exit']:
                end_loop = True
            else:
                success, response = self._execute_command(requested_command)
                self.queue.put((success, response))

            time.sleep(TIMEOUT)

        print(color_string(f"Disconnected from {self.target}", 'yellow'))
