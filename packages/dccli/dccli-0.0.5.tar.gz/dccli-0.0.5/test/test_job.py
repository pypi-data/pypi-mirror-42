from os.path import join, dirname

from dccli.error_codes import SUCCESS
from dccli.job import Submit, Download, CheckProgress, QueryLog, StreamLog
from dccli.user import Register, Login
from test.test_common import test_config, clean_up_login_token, s3_client

_master_endpoint = test_config["master_endpoint"]
_job_uuid = test_config["job_uuid"]
_output_path = join(dirname(__file__))

register = Register(_master_endpoint)
user_data = {
    'email': test_config["email"],
    'password': test_config["password"]
}
register.register(user_data)

# start a new login
clean_up_login_token()
login = Login(_master_endpoint)
login.login(user_data)


def test_end2end_submit():
    class DummyFlag:
        dummy = ""

    submit_case = None
    try:
        submit_case = Submit(_master_endpoint)
        assert submit_case.execute(DummyFlag()) == SUCCESS
    finally:
        print(submit_case.job_uuid)
        if submit_case is not None and submit_case.job_uuid is not None:
            s3_client.s3_delete_by_key(bucket=test_config["s3_bucket_name"], s3_folder=submit_case.job_uuid, key=None)


def test_download_output():
    class DummyFlag:
        job_uuid = _job_uuid
        dest = _output_path

    download_case = Download(_master_endpoint)
    print(DummyFlag.job_uuid)
    assert download_case.execute(DummyFlag) == SUCCESS


def test_check_progress():
    class DummyFlag:
        job_uuid = _job_uuid

    progress_case = CheckProgress(_master_endpoint)
    assert progress_case.execute(DummyFlag) == SUCCESS


def test_query_log_no_console():
    class DummyFlag:
        job_uuid = _job_uuid
        dest = _output_path
        console = False

    log_case = QueryLog(_master_endpoint)
    assert log_case.execute(DummyFlag) == SUCCESS


def test_query_log_with_console():
    class DummyFlag:
        job_uuid = _job_uuid
        dest = _output_path
        console = True

    log_case = QueryLog(_master_endpoint)
    assert log_case.execute(DummyFlag) == SUCCESS


def test_stream_log():
    class DummyFlag:
        job_uuid = '56b15448-e4fd-40f0-be13-c1522d5924f5'

    log_case = StreamLog(_master_endpoint)
    assert log_case.execute(DummyFlag) == SUCCESS

test_stream_log()