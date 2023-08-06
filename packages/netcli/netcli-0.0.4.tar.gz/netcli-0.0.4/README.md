[![Build Status](https://travis-ci.org/chadell/lazycli.svg?branch=master)](https://travis-ci.org/chadell/lazycli)

# NETCLI

netcli is the CLI for the people who is not able to remember every command for every vendor gear.

So, the idea it's simple, why you don't build your own language and then use it as you want?

netcli solves this problem using a simple approach:
* You have a **config** mode to handle your custom commands and the translation for all the specific vendors you are interested in.
* You have a **connect** mode to run an interactive CLI against your devices and enjoy your commands

## Installation

```
pip install netcli
```

## How to run it

## Config

> Your customs commands will be stored in `~/.my_netcli_commands.json`

### Add

```
$ netcli config add "bgp received routes neighbor:192.0.2.1"
```

Note:
* Use quotes to add your command
* Arguments should come at the end, using the pattern `<arg_name>:<default_value>`

This will enter an interactive mode to provide:
* Description: Useful to remember what this command is doing
* Vendor specific implementations, using this format: `<vendor_type> - <your command>`
    * **important** within `<your_command>` you can place the arguments provided using `[arg_name]`
    * `<vendor_type>` comes from [Netmiko library](https://github.com/ktbyers/netmiko/blob/develop/netmiko/ssh_dispatcher.py#L76)

### Delete

```
$ netcli config delete "bgp received routes"
```

### Show

```
$ netcli config show
```

It listes the custom commands with the description and ports.
If you need the vendor implementation, use `--verbose`


## Interactive CLI

```
$ netcli connect <target> -v <vendor_type>
```

Enjoy it!

Notes:
* To overwrite a default value use `[<arg_name>:<new_value>]`
* Execution of **raw commands** is possible starting the command with `r- ` 
* **Matching output** of custom commands can be achieved by adding ` | ` and the string to match
* Use `help`/`h` to get extra help
