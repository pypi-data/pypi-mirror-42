#!/usr/bin/env python
import os
import time
# pylint: disable=useless-import-alias,unnecessary-pass,unused-argument,too-many-statements,no-value-for-parameter
try:
    import queue as queue
except ImportError:
    import Queue as queue
import click

from netcli.config import Config
from netcli.connect import ConnectThread
from netcli.formatters import Spinner, color_string
from netcli.errors import NetcliError

TIMEOUT = 0.1


@click.group()
@click.pass_context
def cli(ctx):
    """
    If you can't remember any fu....ing CLI command, this is your CLI!
    -> Here you can create your own aliases and apply to every specific CLI language.
    """
    ctx.obj = {
        "config": Config()
    }


@click.group()
@click.pass_context
def config(ctx):
    """
    Manage your custom CLI command to rule the world
    """
    pass


cli.add_command(config)


@config.command()
@click.argument('command')
@click.pass_context
def add(ctx, command):
    """
    Add a custom command (Example: "custom_command arg1:default)"
    """
    ctx.obj['config'].add(command)


@config.command()
@click.argument('command')
@click.pass_context
def delete(ctx, command):
    """
    Delete a custom command. Example: "custom_command"
    """
    ctx.obj['config'].delete(command)


@config.command()
@click.option(
    '--verbose/--no-verbose',
    default=False,
)
@click.pass_context
def show(ctx, verbose):
    """
    List all the available custom commands
    """
    if verbose:
        ctx.obj['config'].show()
    else:
        ctx.obj['config'].show_brief()
        print()
        print("Please, if you need more info add --verbose option")


@config.command()
@click.argument('command')
@click.pass_context
def update(ctx, command):
    """
    Update a custom command
    """
    pass


@cli.command()
@click.argument('target')
@click.option(
    '--user', '-u',
    default=os.getlogin(),
)
@click.option(
    '--password', '-p',
    default=None,
)
@click.option(
    '--vendor', '-v',
    required=True,
)
@click.pass_context
def connect(ctx, target, user, password, vendor):
    """
    Connect to a device and run and interactive CLI session
    """
    print(color_string(f"\nWelcome {user} to the laziest CLI ever!!!\n", 'green'))

    cli_queue = queue.Queue()
    with Spinner(f"Connecting to {target} using vendor {vendor}"):
        try:
            connection_config = {
                "target": target,
                "user": user,
                "password": password,
                "device_type": vendor,
            }
            connection_thread = ConnectThread(connection_config,
                                              ctx.obj['config'].custom_commands,
                                              cli_queue)
            connection_thread.start()
            thread_response = cli_queue.get()
            if not thread_response[0]:
                Spinner.result('KO', 'red')
                print(color_string(thread_response[1], 'red'))
                return
        except NetcliError as error:
            Spinner.result('KO', 'red')
            print(color_string(error, 'red'))
            return

    Spinner.result('OK', 'green')
    print()
    print(color_string("Interactive NETCLI", 'green'))
    print()

    end_loop = False
    while not end_loop:
        try:
            user_input = input(color_string('=> ', 'cyan'))
        except (EOFError, KeyboardInterrupt):
            cli_queue.put((True, "end"))
            end_loop = True
            break
        if user_input in ['']:
            continue
        if user_input in ['help', 'h']:
            ctx.obj['config'].show_brief(cli=True)
            continue
        if user_input[-1] == '?':
            ctx.obj['config'].show_details(user_input[:-2])
            continue
        print()
        cli_queue.put((True, user_input))
        time.sleep(TIMEOUT)

        if user_input not in ['end', 'exit', 'quit']:
            res = cli_queue.get()
            print(color_string(res[1], "green" if res[0] else "red"))
        else:
            end_loop = True

    time.sleep(TIMEOUT*3)
    print(color_string("Bye, bye!", 'yellow'))


if __name__ == "__main__":
    cli()
