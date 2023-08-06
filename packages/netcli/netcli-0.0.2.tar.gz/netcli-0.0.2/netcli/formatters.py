import sys
import time
import threading
from colorama import Fore, Style


class Spinner:
    """
    Class to create a spinner object as context manager
    """
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, msg, delay=None):
        self.spinner_generator = self.spinning_cursor()
        self.msg = msg
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        sys.stdout.write(self.msg + " ")
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()
        sys.stdout.write(" ")

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.stop()


def color_string(msg, color):
    colours = {
        'green': Fore.GREEN,
        'red': Fore.RED,
        'yellow': Fore.YELLOW,
        'cyan': Fore.CYAN,
        'magenta': Fore.MAGENTA,
    }
    try:
        return f"{colours[color]}{msg}{Style.RESET_ALL}"
    except IndexError:
        return msg
