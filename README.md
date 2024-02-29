# Joomla Brute-force Script (Enhanced Version)

This version of the Joomla brute-force script is a fork of an existing project by ajnik, enhanced to provide real-time feedback during the password testing process.

## Enhanced Features

- **Real-time Feedback**: The script now displays the current password being tested along with its position in the overall list (e.g., "trying password 3 of 100: password123"). This feature provides better visibility into the script's progress and can be particularly useful for long-running brute-force attacks.

## Original Features
A Python script designed to perform a brute-force attack on Joomla site logins. This tool attempts to log in using a list of usernames and passwords, making it suitable for penetration testers and security researchers.

## Original Features

- Supports single username or a list of usernames
- Customizable wordlist for password attempts
- Proxy support for anonymous testing
- Verbose mode for detailed output
- Utilizes BeautifulSoup for parsing HTML responses

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.x
- Requests: `pip install requests`
- BeautifulSoup: `pip install beautifulsoup4`

## Installation

Clone the repository to your local machine:

```
git clone https://github.com/mdb-dev-io/joomla-bruteforce.git
cd joomla-bruteforce
```

## Usage

To use the script, you'll need to specify the Joomla site URL and the path to your wordlist file. Optionally, you can specify a proxy, enable verbose output, and choose between a single username or a list of usernames.

Basic usage:

```
python3 joomla_bruteforce.py -u <Joomla Site URL> -w <Path to Wordlist> -usr <Username>
```

Using a userlist and proxy:

```
python3 joomla_bruteforce.py -u <Joomla Site URL> -w <Path to Wordlist> -U <Path to Userlist> -p <Proxy>
```

For more options, use the help command:

```
python3 joomla_bruteforce.py -h
```

## Acknowledgements

This project builds upon the original Joomla brute-force script by [[Original Author ajink/Repository]](https://github.com/ajnik/joomla-bruteforce). The enhancements aim to improve usability and feedback for penetration testers and security researchers.

## Disclaimer

This tool is intended for educational and ethical testing purposes only. Unauthorized testing of websites and applications without explicit permission is illegal and unethical.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the script or suggest new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
