# JSONBrute

A simple JSON bruteforce tool for penetration testers or hobbyists.

## Why is this useful?
Have you ever been on an engagement where you've had to bruteforce a JSON API, and industry standard tools such as [hydra](https://github.com/vanhauser-thc/thc-hydra) and [wfuzz](https://github.com/xmendez/wfuzz) can't handle the data type? That's where JSONBrute excels.

## Installation
```bash
git clone https://github.com/Jake-Ruston/JSONBrute.git
```

## Usage
```bash
./jsonbrute.py -u 10.10.10.10 -d 'username=admin, password=FUZZ' -w rockyou.txt
```
The above will send the following payload, replacing *FUZZ* with every word in the wordlist:
```json
{
	"username": "admin",
	"password": "FUZZ"
}
```

## Checklist
- [x] Create an argument parser
- [x] Get each word in the given wordlist
- [x] Make a request to the given URL for each word
- [x] Send the given data to the URL for each word
- [x] Replace the FUZZ keyword with each word
- [ ] Move separate functionality into their own files
- [ ] Error checking
	- [ ] URL given
	- [ ] Data given
	- [ ] Wordlist given
	- [ ] Request exception
- [ ] Threading
- [x] Add extra argument for verbosity
- [x] Add extra argument for status code
- [ ] Add extra argument for user agent

## TODO
- [ ] Fix the `verbose` and `code` arguments in the help display
- [ ] Use a more efficient way to replace the FUZZed word with the entry in the given wordlist