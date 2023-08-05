import os
import json
from os.path import splitext, basename
import tarfile
import requests
import yaml
import argparse


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Token ' + self.token
        return r


class BaseCase:
    master_endpoint = None
    parser = argparse.ArgumentParser()

    def __init__(self, master_endpoint="http://dtf-masterserver-dev.us-west-1.elasticbeanstalk.com"):
        self.master_endpoint = master_endpoint

    def add_arguments(self):
        # add case specific arguments
        pass

    def execute(self, FLAGS):
        # add your specific logic functions
        raise Exception("must be overridden")

    def parse_and_execute(self):
        self.add_arguments()
        FLAGS, _ = self.parser.parse_known_args()
        self.execute(FLAGS)


def load_yaml(task_path):
    with open(task_path) as f:
        config = None
        filename, file_extension = splitext(basename(task_path))
        if file_extension == ".json":
            config = json.load(f)
        elif file_extension == ".yaml":
            config = yaml.load(f)
        else:
            raise ValueError("{} is not a valid config".format(str(f)))
    return config


def make_tarfile(output_filename, source_dir):
    if source_dir is not None:
        if not source_dir.endswith(os.path.sep):
            source_dir = source_dir + os.path.sep
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))


def unzip_tarfile(source_tar, target_dir):
    tar = tarfile.open(source_tar, "r:gz")
    tar.extractall(path=target_dir)
    tar.close()


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)
