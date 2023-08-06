import argparse

from dccli.job import Submit, CheckProgress, Download, QueryLog, StreamLog
from dccli.user import Login, Register
from dccli.utils import BaseCase
import signal


def signal_handler(signal, frame):
    pass


signal.signal(signal.SIGINT, signal_handler)


def main():
    support_functions = {
        "submit": Submit(),
        "register": Register(),
        "progress": CheckProgress(),
        "download": Download(),
        "log": QueryLog(),
        "login": Login(),
        "stream": StreamLog()
    }

    function_lists = [k for k in support_functions.keys()]

    parser = argparse.ArgumentParser()

    parser.add_argument("function_name", type=str,
                        help="function name you want to invoke, supported functions are : {}".format(function_lists))

    FLAGS, _ = parser.parse_known_args()
    function_name = FLAGS.function_name

    try:
        if function_name in support_functions and isinstance(support_functions[function_name], BaseCase):
            support_functions[function_name].parse_and_execute()
        else:
            print("{} is not one of the supported functions.".format(function_name))
    except Exception as e:
        print(str(e))
