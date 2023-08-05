import boto3
import os
from os import listdir
from os.path import isfile, join, isdir, exists, basename
from subprocess import Popen
import subprocess

from dccli.constants import TAR_GZ_EXTENSION, CODE_DIR_NAME, DEBUG


def create_s3_client(s3_temp_token):
    client = boto3.client(
        's3',
        region_name=s3_temp_token["s3_region"],
        aws_access_key_id=s3_temp_token["access_key_id"],
        aws_secret_access_key=s3_temp_token["secret_access_key"],
        aws_session_token=s3_temp_token['session_token'])
    return client


def upload_dir_to_s3(dir_path, bucket_name, folder_name, client):
    assert client is not None

    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            print("uploading file {0} to {1}".format(join(dir_path, f), construct_s3_path(bucket_name, folder_name)))
            upload_file_to_s3(join(dir_path, f), bucket_name, folder_name, client)
        elif isdir(join(dir_path, f)):
            print("uploading directory {0} to {1}".format(join(dir_path, f), construct_s3_path(bucket_name, folder_name)))
            s3_dir_name = folder_name + "/" + f
            upload_dir_to_s3(join(dir_path, f), bucket_name, s3_dir_name, client)

    return folder_name


def upload_file_to_s3(file_path, bucket_name, folder_name, client):
    invalid_extension = [".c", ".cpp", ".js", ".java", ".exe", ".dll", ".o"]

    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        name, extension = os.path.splitext(filename)
        if extension not in invalid_extension:
            s3_file_name = "{0}/{1}".format(folder_name, filename)
            print("uploading file {0} to {1}".format(file_path, construct_s3_path(bucket_name, s3_file_name)))
            client.upload_file(file_path, bucket_name, s3_file_name)
            return s3_file_name
    else:
        raise ValueError("file {0} does not exist".format(file_path))


def download_files_from_s3(bucket_name, code_location, dest_dir, client):
    bucket = client.list_objects_v2(Bucket=bucket_name, Prefix=code_location)
    assert bucket is not None
    if "Contents" not in bucket:
        print("task does not exists or not available for download")

    for f in bucket["Contents"]:
        if os.path.basename(f["Key"]) != '':
            client.download_file(bucket_name, f["Key"],
                                 join(dest_dir, os.path.basename(f["Key"])))


def download_file_from_s3(bucket_name, s3_file_path, dest_dir, client):
    file_name = basename(s3_file_path)
    file_destination = join(dest_dir, file_name)
    client.download_file(bucket_name, s3_file_path, file_destination)
    return


def construct_s3_path(bucket_name, folder_name):
    return "s3://{0}/{1}".format(bucket_name, folder_name)


def upload_using_git(bucket_name, folder_name, client, allow_dirty):
    # upload current git directory and its sub directories
    repo_tar_path = '{}.{}'.format(CODE_DIR_NAME, TAR_GZ_EXTENSION)
    if exists(repo_tar_path):
        print("Found previously generated code package. Remove it and generate a new one")
        os.remove(repo_tar_path)

    process = None

    # start packaging code into tar.gz
    if allow_dirty:
        print("Code package includes uncommitted changes")
        #  git ls-files -z | xargs -0 tar -czvf archive.tar.gz

        stash_process = Popen(['git', 'stash'], stdout=subprocess.PIPE)
        stash_process.wait()

        archive_process = Popen(['git', 'archive', '--format={}'.format(TAR_GZ_EXTENSION), 'stash@{0}', '--output={}'.format(repo_tar_path)], stderr=subprocess.PIPE)
        archive_process.wait()

        pop_stash_process = Popen(['git', 'stash', 'pop'], stdout=subprocess.PIPE)
        pop_stash_process.wait()

    else:
        # check if there is uncommitted change in the working dir
        diff_process = Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
        diff_process.wait()
        diffs = diff_process.stdout.read().decode("utf-8").split("\n")
        # if there is no diff, process will output empty string
        if len(diffs) > 1:
            # user has uncommitted change in working directory
            error_msg = "You have uncommitted change in working directory. " \
                        "If you want to package current directory with uncommitted changes, " \
                        "please use -d or --dirty flag in cli"
            if DEBUG:
                print(error_msg)
            else:
                return False, error_msg

        archive_process = Popen(['git', 'archive', '--format={}'.format(TAR_GZ_EXTENSION), 'HEAD', '--output={}'.format(repo_tar_path)], stderr=subprocess.PIPE)
        archive_process.wait()

    if exists(repo_tar_path):
        upload_file_to_s3(repo_tar_path, bucket_name, folder_name, client)

        # remove repo tar after uploading
        os.remove(repo_tar_path)
    else:
        # remove repo tar when failed
        if exists(repo_tar_path):
            os.remove(repo_tar_path)

        error = process.stderr.read().decode("utf-8") if process is not None else "unknown"
        return False, "Failed to generate code package with error {}".format(error)
    return True, None

