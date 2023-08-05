import json
import shutil
from os.path import isfile, isdir, exists, join, dirname
import os
from os import listdir
from time import sleep

import requests
from boto3.exceptions import S3UploadFailedError

from dccli.constants import CODE_DIR_NAME, TEMP_LOG_FOLDER
from dccli.error_codes import SUCCESS, MASTER_FAILURE, USER_INPUT_ERROR
from dccli.s3_util import create_s3_client, upload_dir_to_s3, upload_file_to_s3, download_files_from_s3, \
    upload_using_git, download_file_from_s3
from dccli.user import request_file_share_token, get_login_token
from dccli.utils import load_yaml, BaseCase

from dccli.constants import DATASET_TAR_GZ
from dccli.utils import make_tarfile


def submit_job(job_data, s3_temp_token, auth, master_endpoint, allow_dirty):
    if job_data["dataset"]["dataset_name"] is not None:
        dataset_tar_location = None
    else:
        validate_tf_param(job_data)

        # compress dataset
        dataset_tar_location = join(job_data["dataset"]["dataset_path"], DATASET_TAR_GZ)
        make_tarfile(dataset_tar_location, job_data["dataset"]["dataset_path"])

    code_location_s3, dataset_location_s3 = upload_to_s3(
        dataset_tar_location,
        s3_temp_token['job_uuid'],
        s3_temp_token,
        allow_dirty)

    if dataset_tar_location is not None and exists(dataset_tar_location):
        os.remove(dataset_tar_location)

    job_data["model_location"] = code_location_s3
    job_data["dataset"]["dataset_location"] = job_data["dataset"]["dataset_name"] if job_data["dataset"]["dataset_name"] is not None else dataset_location_s3

    print("model_location: {0}, dataset_location: {1}".format(job_data["model_location"],
                                                              job_data["dataset"]["dataset_location"]))
    return submit_job_to_master_server(job_data, s3_temp_token, auth, master_endpoint)


def submit_job_to_master_server(job_data, s3_temp_token, auth, master_endpoint):
    job_type_mapping = {'tensorflow': 'tf',
                        'pytorch': 'pt'}
    _job_type = job_data.get("job_type", "pytorch")  # set as pytorch by default now instead of new parameter in config

    request_body = {
        'parameters': json.dumps(job_data),
        'job_uuid': s3_temp_token['job_uuid']
    }

    create_task_request = requests.post("{}/api/v1/user/{}/job/".format(master_endpoint, job_type_mapping[_job_type]),
                                        data=request_body, auth=auth)
    create_task_resp = json.loads(create_task_request.text)
    print("Status: {}".format(create_task_request.status_code))
    if not create_task_request.ok:
        print("Error: {}".format(create_task_resp.get("error")))
        print("Message: {}".format(create_task_resp.get("message")))
        return MASTER_FAILURE

    print("job_uuid: {}".format(create_task_resp.get("job_uuid")))
    print("job_type: {}".format(create_task_resp.get("job_type")))
    return SUCCESS


def validate_tf_param(tf_param):
    dataset_path = tf_param["dataset"]["dataset_path"]
    if not isdir(dataset_path) and not isfile(dataset_path):
        raise ValueError("cannot find dataset path {}".format(dataset_path))


def upload_to_s3(dataset_path, uuid, s3_temp_token, allow_dirty):
    retry = 3
    latest_exception = None
    while retry > 0:
        try:
            client = create_s3_client(s3_temp_token)
            s3_bucket_name = s3_temp_token['s3_bucket_name']
            code_folder_s3 = "{0}/{1}".format(uuid, CODE_DIR_NAME)
            is_success, error_msg = upload_using_git(s3_bucket_name, code_folder_s3, client, allow_dirty)
            if not is_success:
                raise Exception(error_msg)

            folder_name = "{0}/{1}".format(uuid, "dataset")
            dataset_location_s3 = None
            if dataset_path is not None and exists(dataset_path):
                if isfile(dataset_path):
                    dataset_location_s3 = upload_file_to_s3(dataset_path, s3_bucket_name, folder_name, client)
                else:
                    dataset_location_s3 = upload_dir_to_s3(dataset_path, s3_bucket_name, folder_name, client)

            return code_folder_s3, dataset_location_s3

        except S3UploadFailedError as ex:
            latest_exception = str(ex)
            sleep(2)
            retry -= 1

    raise Exception("failed to upload to s3 with exception: {}".format(latest_exception))


class Download(BaseCase):
    def add_arguments(self):
        self.parser.add_argument(
            '--dest',
            type=str,
            required=True,
            help="Destination folder to save the logs")

        self.parser.add_argument(
            '--job_uuid',
            type=str,
            required=True,
            help="Your job uuid shown when you submit a training job")

    def execute(self, FLAGS):
        print("===========================================")
        print("Download model outputs")
        print("===========================================")
        auth = get_login_token()
        s3_temp_token = request_file_share_token(self.master_endpoint, auth, FLAGS.job_uuid)

        client = create_s3_client(s3_temp_token)
        if not exists(FLAGS.dest):
            os.makedirs(FLAGS.dest)
        elif not isdir(FLAGS.dest):
            raise Exception("{} is a file but not a directory".format(FLAGS.dest))

        s3_bucket_name = s3_temp_token['s3_bucket_name']
        download_files_from_s3(s3_bucket_name, FLAGS.job_uuid + "/out", FLAGS.dest, client)
        print("Finished download for job: {}".format(FLAGS.job_uuid))
        return SUCCESS


class CheckProgress(BaseCase):
    def add_arguments(self):
        self.parser.add_argument(
            '--job_uuid',
            type=str,
            required=True,
            help="Your job uuid shown when you submit the job")

    def execute(self, FLAGS):
        print("===========================================")
        print("Check Job Progress")
        print("===========================================")
        auth = get_login_token()
        job_progress_request = requests.get("{}/api/v1/user/progress/{}/".format(self.master_endpoint, FLAGS.job_uuid),
                                            auth=auth)
        job_progress_resp = json.loads(job_progress_request.text)
        print("Status: {}".format(job_progress_request.status_code))
        if not job_progress_request.ok:
            print("Error: {}".format(job_progress_resp.get("error", None)))
            print("Message: {}".format(job_progress_resp.get("message", None)))
            return MASTER_FAILURE
        else:
            print("job_uuid: {}".format(job_progress_resp.get('job_uuid', None)))
            print("job_state: {}".format(job_progress_resp.get('job_state', None)))
            print("tensorboard_location: {}".format(job_progress_resp.get('tensorboard_location', None)))
            return SUCCESS


class StreamLog(BaseCase):
    def add_arguments(self):
        self.parser.add_argument(
            '--job_uuid',
            type=str,
            required=True,
            help="Your job uuid shown when you submit the job")

    def execute(self, FLAGS):
        auth = get_login_token()
        print("===========================================")
        print("Query for logs")
        print("===========================================")
        has_all_log = False
        while not has_all_log:
            query_log_request = requests.get("{}/api/v1/user/stream/{}/".format(self.master_endpoint, FLAGS.job_uuid),
                                             auth=auth)

            # query log resp should be a list of string
            query_log_resp = json.loads(query_log_request.text)

            if not query_log_request.ok:
                print("Error: {}".format(query_log_resp.get("error", None)))
                # 200 means that is the last batch of log,
                # 202 means there is more
                if query_log_request.status_code == 200:
                    has_all_log = True
                elif 300 < query_log_request.status_code < 500:
                    return USER_INPUT_ERROR
                elif query_log_request.status_code >= 500:
                    return MASTER_FAILURE

            if len(query_log_resp) == 0:
                print("No log is found...")
            else:
                for log in json.loads(query_log_resp['log']):
                    print(log)

            sleep(3)

        return SUCCESS


class QueryLog(BaseCase):
    def add_arguments(self):
        self.parser.add_argument(
            '--job_uuid',
            type=str,
            required=True,
            help="Your job uuid shown when you submit the job")

        self.parser.add_argument(
            '-c',
            '--console',
            action="store_true",
            help="print model logs to console")

        self.parser.add_argument(
            '--dest',
            type=str,
            help='Destination folder to save the models')

    def execute(self, FLAGS):
        auth = get_login_token()
        print("===========================================")
        print("Query for logs")
        print("===========================================")
        query_log_request = requests.get("{}/api/v1/user/log/{}/".format(self.master_endpoint, FLAGS.job_uuid),
                                         auth=auth)
        query_log_resp = json.loads(query_log_request.text)
        print("Status: {}".format(query_log_request.status_code))
        if not query_log_request.ok:
            print("Error: {}".format(query_log_resp.get("error", None)))
            return MASTER_FAILURE
        else:
            auth = query_log_resp.get("auth", None)
            if auth is None:
                reason = query_log_resp.get("reason", None)
                if reason is not None:
                    print(reason)
                else:
                    print("Failed to query log: unknown error")

                return MASTER_FAILURE
            else:
                logs = query_log_resp.get("logs", None)
                if logs is None or len(logs) == 0:
                    print("No log is found...")
                else:
                    client = create_s3_client(auth)
                    s3_bucket_name = auth['s3_bucket_name']
                    count = 1

                    dest = FLAGS.dest

                    if not isdir(dest) and dest is not None:
                        print("dest is not a valid local directory")
                        return USER_INPUT_ERROR
                    temp_log_folder = join(dirname(__file__), TEMP_LOG_FOLDER)
                    if FLAGS.console:
                        if exists(temp_log_folder):
                            shutil.rmtree(temp_log_folder, ignore_errors=True)
                        os.mkdir(temp_log_folder)
                        dest = dest if dest is not None else temp_log_folder

                    for log in logs:
                        print("  [{}/{}] {}...".format(count, len(logs), log))
                        download_file_from_s3(s3_bucket_name, log, dest, client)
                        count += 1

                    if FLAGS.console:
                        logs = []
                        for f in listdir(dest):
                            if isfile(join(dest, f)) and ".log" in f:
                                logs.append(f)

                        # print out first then error
                        if len(logs) > 0:
                            print("===========================================")
                            print("===============start of logs===============")
                            logs.sort(reverse=True)

                            for l in logs:
                                with open(join(dest, l), "r") as f:
                                    log = f.readline()
                                    while log:
                                        log = log if log[-1] is not "\n" else log[0:-1]
                                        print(log)
                                        log = f.readline()

                            if exists(temp_log_folder):
                                shutil.rmtree(temp_log_folder, ignore_errors=True)

                return SUCCESS


class Submit(BaseCase):
    job_uuid = None

    def add_arguments(self):
        self.parser.add_argument(
            '-d',
            '--dirty',
            action="store_true",
            help="upload current git directory with uncommitted/untracked files"
        )

    def execute(self, FLAGS):
        auth = get_login_token()
        s3_temp_token = request_file_share_token(self.master_endpoint, auth)
        self.job_uuid = s3_temp_token.get("job_uuid", None)

        print("===========================================")
        print("Submit task")
        print("===========================================")

        config_path = "./config.yaml"
        if exists(config_path):
            job_data = load_yaml(config_path)
        else:
            raise Exception("Cannot find config.yaml")

        return submit_job(job_data, s3_temp_token, auth, self.master_endpoint, FLAGS.dirty)
