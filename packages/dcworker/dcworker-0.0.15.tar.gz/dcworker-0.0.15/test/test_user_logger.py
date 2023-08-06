import multiprocessing as mp
from os.path import dirname, join
from time import sleep

from worker.worker_log.user_logger import streaming_user_log

_test_log = join(dirname(__file__), "test.log")
_test_error_log = join(dirname(__file__), "test.error.log")


class MockTaskContext:

    def __init__(self, exec_process):
        self.exec_process = exec_process

    def flush_from_exec_process_queue(self):
        return True, True


def wait_5_then_write_log():
    sleep(4)
    with open(_test_log, "w") as f:
        for i in range(5):
            if i == 2:
                print("enter sleep")
                sleep(10)
            f.write("this is log {}\n".format(i))
            f.flush()
            print("write")


def test_user_logger():
    process = mp.Process(target=wait_5_then_write_log)
    task_context = MockTaskContext(process)
    process.start()

    streaming_user_log(task_context, "521856ca-b060-413c-9edc-687ab08cb813", "521856ca-b060-413c-9edc-687ab08cb824",
                       _test_log, _test_error_log)
    process.join()


if __name__ == '__main__':
    test_user_logger()
