from worker.worker_start import *

from worker.worker_runtime import WorkerStateMachine

def worker_entry(runtime,
                 workdir,
                 toplevel_datadir,
                 port,
                 worker_uuid,
                 passcode,
                 gpu_id):

    worker = Worker(runtime,
                    port,
                    workdir,
                    toplevel_datadir,
                    worker_uuid=worker_uuid,
                    gpu_id=gpu_id,
                    passcode=passcode)


    worker_stm = WorkerStateMachine(worker)
    worker_stm.start()