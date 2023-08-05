import argparse

from dccli.job import Submit, CheckProgress, Download, QueryLog, StreamLog
from dccli.user import Login, Register
from dccli.utils import BaseCase


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("function_name", type=str,
                        help="function name you want to invoke")

    FLAGS, _ = parser.parse_known_args()
    function_name = FLAGS.function_name

    try:
        support_functions = {
            "submit": Submit(),
            "register": Register(),
            "progress": CheckProgress(),
            "download": Download(),
            "log": QueryLog(),
            "login": Login(),
            "stream": StreamLog()
        }

        if function_name in support_functions and isinstance(support_functions[function_name], BaseCase):
            support_functions[function_name].parse_and_execute()
        else:
            print("{} is not one of the supported functions.".format(function_name))
    except Exception as e:
        print(str(e))
