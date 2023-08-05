from os.path import join, dirname

from dccli.error_codes import SUCCESS
from dccli.user import Register, Login
from test.test_common import test_config

master_endpoint = test_config["master_endpoint"]
job_uuid = test_config["job_uuid"]
output_path = join(dirname(__file__), "test_out")


def test_register_user():
    register_case = Register(master_endpoint)
    user_data = {
        'email': test_config["email"],
        'password': test_config["password"]
    }

    assert register_case.register(user_data) == SUCCESS


def test_login_user():
    login = Login(master_endpoint)
    user_data = {
        'email': test_config["email"],
        'password': test_config["password"]
    }

    assert login.login(user_data) == SUCCESS
