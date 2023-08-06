# this task is chief if task_index = 0

from common.global_variable import JOB_TYPE_SUPPORTED

class TrainingTask(object):
    def __init__(self,
                 task_uuid=None,
                 keep_alive_interval=None,
                 signal_finish=None,
                 ask_finish=None,
                 job_name=None,
                 job_type=None,
                 cluster_spec=None,
                 task_index=None,
                 model_location=None,
                 dataset=None,
                 requirement_location=None):

        # Validate task_uuid
        if task_uuid is None:
            raise ValueError("task_uuid is None")

        self.task_uuid = task_uuid

        # Validate keep_alive_interval
        if keep_alive_interval is None:
            raise ValueError("keep_alive_interval is None")

        try:
            self.keep_alive_interval = int(keep_alive_interval)
        except:
            raise ValueError("keep_alive_interval is not integer")

        if self.keep_alive_interval <= 0:
            raise ValueError("keep_alive_interval is not greater than 0")

        # Validate signal_finish
        if signal_finish is None:
            raise ValueError("signal_finish is None")

        try:
            self.signal_finish = bool(signal_finish)
        except:
            raise ValueError("signal_finish is not boolean")

        # Validate ask_finish
        if ask_finish is None:
            raise ValueError("ask_finish is None")

        try:
            self.ask_finish = bool(ask_finish)
        except:
            raise ValueError("ask_finish is not boolean")

        # Validate task cannot be both ask and signal finish
        if self.signal_finish and self.ask_finish:
            raise ValueError("unexpected task both signal and ask finish")

        # Validate job_name
        if job_name is None:
            raise ValueError("job_name is None")

        if job_name != "worker" and job_name != "ps":
            raise ValueError("job_name {} is not valid".format(job_name))

        # Validate job_type
        if job_type is None:
            raise ValueError("job_type is None")

        if job_type not in JOB_TYPE_SUPPORTED:
            raise ValueError("job_type is not supported")

        # Task state is set to False by default. It is only set to true when
        # the worker reported to master that the task has terminated successfully.
        self.finished = False
        self.job_name = job_name
        self.cluster_spec = cluster_spec
        self.job_type = job_type
        self.task_index = task_index
        self.model_location = model_location
        self.dataset = dataset
        self.dataset_local_path = None
        self.job_id = None
        self.tensorboard_process = None
        # Validate for worker job
        if job_name == "worker":
            if self.model_location is None:
                raise ValueError("worker job requires model_location")

            if self.dataset is None:
                raise ValueError("worker job requires dataset")

            if "dataset_location" not in self.dataset:
                raise ValueError("dataset requires dataset_location")