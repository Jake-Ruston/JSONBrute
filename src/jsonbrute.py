class JSONBrute:
    def info(self, message):
        print(f"\033[94m[*]\033[0m {message}")

    def success(self, message):
        print(f"\033[92m[+]\033[0m {message}")

    def warning(self, message):
        print(f"\033[93m[!]\033[0m {message}")

    def error(self, message):
        print(f"\033[91m[-]\033[0m {message}")

    def parse_arguments(self):
        from argparse import ArgumentParser

        parser = ArgumentParser(description="A simple JSON bruteforce tool for penetration testers or hobbyists")

        parser.add_argument("--url", type=str, required=True, help="The URL to post the data to.")
        parser.add_argument("--wordlist", type=str, required=True, help="The wordlist to use to fuzz with.")
        parser.add_argument("--data", type=str, required=True, help="The JSON data to post.")
        parser.add_argument("--verbose", nargs="?", const="false", help="Print every request.")
        parser.add_argument("--code", type=int, nargs="?", const="201", help="The response code for a successful request (default 201).")

        return parser.parse_args()

    def parse_wordlist(self, file):
        with open(file) as data:
            wordlist = data.read().splitlines()

            return wordlist

    def parse_json(self, data):
        json = data.split(",")
        json = [pair.strip().split("=") for pair in json]
        json = {key: value for [key, value] in json}

        return str(json)

    def find(self, args, wordlist):
        from json import loads
        import requests
        import sys

        for entry in wordlist:
            try:
                headers = {
                    "Content-Type": "application/json"
                }
                json = self.parse_json(args.data)
                json = json.replace("FUZZ", entry)
                json = json.replace("'", "\"")
                json = loads(json)

                username = json["username"]
                password = json["password"]

                request = requests.post(args.url, headers=headers, json=json)

                # --code default value = 201
                if not args.code:
                    args.code = 201

                if request.status_code == args.code:
                    self.success(f"Password for {username} found: {password}")
                    sys.exit()
                else:
                    if args.verbose:
                        self.warning(f"Incorrect password for {username}: {password}")
            except requests.ConnectionError:
                self.error(f"Failed to connect to {args.url}")
                sys.exit()
            except KeyboardInterrupt:
                self.error("Exiting...")
                sys.exit()
        else:
            self.warning(f"Password for {username} not found")

    def run(self):
        args = self.parse_arguments()
        wordlist = self.parse_wordlist(args.wordlist)

        self.info(f"Starting JSONBrute on {args.url}")

        self.find(args, wordlist)


JSONBrute().run()
