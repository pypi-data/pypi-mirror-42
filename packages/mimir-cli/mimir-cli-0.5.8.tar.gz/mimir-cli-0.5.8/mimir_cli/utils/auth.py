"""
authentication related helper functions
"""
import json
import os
import requests
from mimir_cli.strings import API_LOGIN_URL, MIMIR_DIR
from mimir_cli.utils.io import mkdir
from mimir_cli.utils.state import debug


def login_to_mimir(email, password):
    """logs into the platform api"""
    login_request = requests.post(
        API_LOGIN_URL, data={"email": email, "password": password}
    )
    data = json.loads(login_request.text)
    debug(data)
    if data["success"]:
        cookies = login_request.cookies.get_dict()
        write_credentials(cookies)
    return data["success"]


def logout_of_mimir():
    """logs out of mimir"""
    credentials_path = "{dir}.credentials".format(dir=MIMIR_DIR)
    os.remove(credentials_path)
    return True


def read_credentials():
    """reads the user credentials from the mimir directory"""
    mkdir(MIMIR_DIR)
    credentials_path = "{dir}.credentials".format(dir=MIMIR_DIR)
    if os.path.isfile(credentials_path):
        mimir_credentials_file = open(credentials_path, "r")
        credentials = json.loads(mimir_credentials_file.read())
        mimir_credentials_file.close()
        return credentials
    return False


def write_credentials(cookies):
    """writes the user credentials to the mimir directory"""
    mkdir(MIMIR_DIR)
    credentials_path = "{dir}.credentials".format(dir=MIMIR_DIR)
    credentials = json.dumps(cookies)
    with open(credentials_path, "w") as mimir_credentials_file:
        mimir_credentials_file.write(credentials)
