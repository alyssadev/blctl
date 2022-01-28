#!/usr/bin/env python3
from appdirs import user_config_dir
from os import environ
import requests
import os.path

TOKEN = None
API_URL = "https://api.binarylane.com.au/v2"

def get(endpoint, **kwargs):
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"]["Authorization"] = f"Bearer {TOKEN}"
    return requests.get(f"{API_URL}{endpoint}", **kwargs).text

def post(endpoint, **kwargs):
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"]["Authorization"] = f"Bearer {TOKEN}"
    return requests.post(f"{API_URL}{endpoint}", **kwargs)

def put(endpoint, **kwargs):
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"]["Authorization"] = f"Bearer {TOKEN}"
    return requests.put(f"{API_URL}{endpoint}", **kwargs).status_code in range(200,300)

def delete(endpoint, **kwargs):
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"]["Authorization"] = f"Bearer {TOKEN}"
    return requests.delete(f"{API_URL}{endpoint}", **kwargs).status_code in range(200,300)

def get_token():
    global TOKEN
    if TOKEN:
        return TOKEN
    token = None
    try:
        token = environ["BL_TOKEN"]
    except KeyError:
        try:
            with open(os.path.join(user_config_dir("blctl"), "token")) as f:
                token = f.read().strip()
        except FileNotFoundError:
            pass
    if not token:
        raise Exception(f"Generate token at https://home.binarylane.com.au/api-info, then write token to {os.path.join(user_config_dir('blctl'), 'token')} or provide as env BL_TOKEN")
    TOKEN = token
    return token

def get_help_page(header="", usage="", available={}):
    from sys import stderr
    list_joiner = "\n  " # https://stackoverflow.com/a/67680321
    print(f"""
{header}

Usage:
  {usage}

Additional Commands:
  {list_joiner.join(f"{k}{' '*(15-len(k))} {v}" for k,v in available.items())}

Use {usage} --help for more information about a command.\n""", file=stderr)

def main():
    global TOKEN
    from sys import argv, stderr
    TOKEN = get_token()
    prog = argv[0].split(os.path.sep)[-1]

    if len(argv) == 1:
        get_help_page(
            header=f"{prog} is a command line interface (CLI) for the BinaryLane API.",
            usage=f"{prog} [command]",
            available={
                "account": "Display commands that retrieve account details",
                "server": "Display commands that manage servers"
            }
        )
        return 0

    if argv[1] == "account":
        if len(argv) == 2 or argv[2] == "--help":
            get_help_page(
                header=f"""The subcommands of `{prog} account` retrieve information about BinaryLane accounts.

For example, `{prog} account get` retrieves account profile details, and `blctl account keys` retrieves account SSH keys.""",
                usage=f"{prog} account [command]",
                available={
                    "get": "Retrieve account profile details",
                    "keys": "Retrieve SSH keys added to account"
                }
            )
        elif argv[2] == "get":
            print(get("/account"))
        elif argv[2] == "keys":
            print(get("/account/keys"))

    if argv[1] == "server":
        if len(argv) == 2 or argv[2] == "--help":
            get_help_page(
                header=f"The subcommands under `{prog} server` are for managing BinaryLane servers.",
                usage=f"{prog} server [command]",
                available={
                    "list": "List servers",
                    "info": "Show info for a particular server, given the server's ID",
                    "neighbors": "List neighbors of a given server, given the server's ID. This command is aliased to `neighbours`."
                }
            )
        elif argv[2] == "list":
            print(get("/servers"))
        elif argv[2] == "info":
            if len(argv) == 3 or argv[3] == "--help":
                print(f"""
This command requires an argument: server_id
{" ".join(argv[:2])} [server_id]\n""", file=stderr)
            else:
                print(get(f"/servers/{argv[3]}"))
        elif argv[2] == "neighbors" or argv[2] == "neighbours":
            if len(argv) == 3 or argv[3] == "--help":
                print(f"""
This command requires an argument: server_id
{" ".join(argv[:2])} [server_id]\n""", file=stderr)
            else:
                print(get(f"/servers/{argv[3]}/neighbors"))
    return 0

if __name__ == "__main__":
    from sys import exit
    exit(main())
