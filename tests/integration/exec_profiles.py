import os, sys
import shutil
from . import test_out_dir, package_root
sys.path.append(os.path.join(package_root, "c2wl_rocket"))
from c2wl_rocket.exec_profile import ExecProfileBase
from c2wl_rocket.worker import Worker


class LocalToolExec(ExecProfileBase):
    def prepare(self):
        shutil.rmtree(test_out_dir)

    def execute(self):
        self.async_exec = False
        worker = Worker(
            self.job_info,
            workdir=test_out_dir
        )

        worker.run()
        self.out = worker.out
        self.success = worker.success
