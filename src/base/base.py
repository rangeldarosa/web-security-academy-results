import requests as req
from abc import ABC, abstractmethod
import argparse
import logging
import sys
import urllib3
from bs4 import BeautifulSoup
# Disable the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Base(ABC):
    def __init__(self, *args, **kwargs):
        """
        Initialize the base class for all scripts.
        """
        logging.basicConfig(level=logging.INFO)

        # Create a formatter for consistent log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        
        # Add console handler with the formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Remove default handlers to avoid duplicate logs
        root_logger = logging.getLogger()
        root_logger.handlers = []
        root_logger.addHandler(console_handler)
        
        # Custom log formats using ANSI escape codes
        self.ERROR_PREFIX = "\033[91m[-]\033[0m"  # Red color
        self.SUCCESS_PREFIX = "\033[92m[+]\033[0m"  # Green color
        self.INFO_PREFIX = "\033[94m[~]\033[0m"  # Blue color
        self.WARNING_PREFIX = "\033[93m[!]\033[0m"  # Yellow color

        self.session = req.Session()

        self.parser = argparse.ArgumentParser(description='Web Security Academy Scripts')
        args = self._parse_default_args()
        self._add_args()
        
        self.target_session = args.target
        self.verbose = args.verbose
        self.proxy = args.proxy


        if self.target_session:
            self.base_url = f"https://{self.target_session}.web-security-academy.net/"

        if self.verbose:
            self.log(f"Executing basic checks", "info")

        self._do_basic_checks()

        if self.verbose:
            self.log(f"Basic checks passed", "info")
    
    def _do_basic_checks(self):
        if self.verbose:
                self.log(f"Testing connectivity with session: {self.target_session}", "info")


        if self.proxy:
            self.log(f"Setting proxy: {self.proxy}", "info")

            self.session.proxies = {
                'http': f"http://{self.proxy}",
                'https': f"http://{self.proxy}"
            }
            
            self.session.verify = False
        else:
            self.session.proxies.clear()

        if self.verbose:
            self.log(f"Setting User-Agent", "info")

            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

        if self.verbose:
            self.log(f"Testing connectivity with session: {self.target_session}", "info")

        response = self.session.get(self.base_url)

        if response.status_code != 200:
            self.log(f"Failed to connect to {self.base_url}", "error")
            sys.exit(1)

    def _parse_default_args(self):
        self.parser.add_argument('--target', type=str, help='Target Session ID. e.g. 0a1b2c3d04ef5678a90b1c2d3e4f5a6b', required=True)
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
        self.parser.add_argument('--proxy', type=str, help='Proxy configuration')
        return self.parser.parse_args()

    @abstractmethod
    def _add_args(self):
        """Add arguments to the parser"""
        raise NotImplementedError("Subclasses must implement _add_args()")
        
    @abstractmethod
    def run(self):
        """Run the exploit (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement run()")
    
    def is_lab_solved(self):
        if self._check_if_lab_solved():
            self.log("Lab Solved", "success")
        else:
            self.log("Lab Not Solved", "error")


    def _check_if_lab_solved(self):
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        lab_status = soup.find('div', class_='widgetcontainer-lab-status')
        if lab_status:
            if 'is-notsolved' in lab_status.get('class'):
                return False
        return True
        
    def log(self, message, type="info"):
        if type == "info":
            logging.info(f"{self.INFO_PREFIX} {message}")
        elif type == "error":
            logging.error(f"{self.ERROR_PREFIX} {message}")
        elif type == "warning":
            logging.warning(f"{self.WARNING_PREFIX} {message}")
        elif type == "success":
            logging.info(f"{self.SUCCESS_PREFIX} {message}")
        elif type == "verbose":
            if self.verbose:
                logging.info(f"{self.INFO_PREFIX} {message}")