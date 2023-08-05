import getpass
import os
from os import listdir
from os.path import join, dirname, exists
from datetime import datetime, timedelta
import requests
import json

from dccli.constants import TEMP_AUTH_TOKEN, TEMP_S3_AUTH_TOKEN
from dccli.error_codes import SUCCESS, MASTER_FAILURE, LOGIN_NEED_REGISTER
from dccli.utils import TokenAuth, BaseCase


def get_login_token():
    temp_token_path = join(dirname(__file__), TEMP_AUTH_TOKEN)
    if not exists(temp_token_path):
        raise Exception("You need to login first")

    with open(temp_token_path, "r") as f:
        auth_token = f.read()
        return TokenAuth(auth_token)


def request_file_share_token(master_endpoint, auth, job_uuid=None):
    # check if there is a local token that is not expired
    s3_temp_token_path = join(dirname(__file__), TEMP_S3_AUTH_TOKEN)
    temp_token = None
    token_list = []
    if exists(s3_temp_token_path):
        with open(s3_temp_token_path, "r") as f:
            token_list_str = f.read()
            if token_list_str != '':
                token_list = json.loads(token_list_str)
                for token in token_list:
                    expiration_date = token.get("expiration", None)
                    temp_token_job_uuid = token.get("job_uuid", None)
                    if expiration_date is not None and temp_token_job_uuid is not None:
                        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
                        expiration_date += timedelta(minutes=10)
                        if expiration_date > datetime.now():
                            if job_uuid == temp_token_job_uuid:
                                temp_token = token
                        else:
                            # remove expired token
                            token_list.remove(token)

    if not temp_token:
        # submit a request without job_uuid
        # server will assign one for you
        request_token_request = requests.get("{}/api/v1/user/token/{}/".format(master_endpoint, job_uuid), auth=auth)

        response = json.loads(request_token_request.text)
        print("Status: {}".format(request_token_request.status_code))
        if not request_token_request.ok:
            print("Error: {}".format(response.get("error")))
            print("Message: {}".format(response.get("message")))
            exit(-1)

        with open(s3_temp_token_path, "w") as f:
            token_list.append(response)
            f.write(json.dumps(token_list))

        return response
    else:
        return temp_token


class Login(BaseCase):
    def execute(self, FLAGS):
        email = input("Please enter your email address: ")
        password = getpass.getpass("Please enter your password: ")

        data = {
            'email': email,
            'password': password
        }

        self.login(data)

    def login(self, data):
        login_request = requests.post("{}/api/v1/user/login/".format(self.master_endpoint), data=data)
        login_response = json.loads(login_request.text)

        if not login_request.ok:
            if login_request.status_code == 401:
                print("You need to register before login")
                return LOGIN_NEED_REGISTER
            else:
                print("Error: {}".format(login_response.get("error")))
                return MASTER_FAILURE

        auth_token = login_response.get('auth_token', None)
        with open(join(dirname(__file__), TEMP_AUTH_TOKEN), "w+") as f:
            # TODO: token need to expire after certain time
            f.write(auth_token)
        print("Login successfully")
        return SUCCESS


class Register(BaseCase):
    def execute(self, FLAGS):
        email = input("Please enter your email address: ")
        password = getpass.getpass("Please enter your password: ")
        re_password = getpass.getpass("Please re-enter your password: ")

        if password != re_password:
            print("Your passwords do not match")
            return

        data = {
            'email': email,
            'password': password
        }

        self.register(data)

    def register(self, data):
        r = requests.post("{}/api/v1/user/register/".format(self.master_endpoint), data=data)
        print("Status: {}".format(r.status_code))
        resp = json.loads(r.text)
        if not r.ok:
            print("Error: {}".format(resp.get("error")))
            return MASTER_FAILURE
        else:
            print("Registered successfully")
            log_in_case = Login(self.master_endpoint)
            log_in_case.login(data)
            return SUCCESS
