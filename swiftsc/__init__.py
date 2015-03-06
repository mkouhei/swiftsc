"""swiftsc

swiftsc is simple client of OpenStack Swift
"""
import urllib3
from swiftsc.client import Client  # silence pyflakes

# See: https://urllib3.readthedocs.org/en/latest/security.html
urllib3.disable_warnings()
