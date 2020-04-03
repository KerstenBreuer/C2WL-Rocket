import os, sys
import shutil
dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
package_root = os.path.join(dir_of_this_script, "..", "..")
test_out_dir = os.path.join(package_root, "test_out")
sys.path.append(package_root)
from c2wl_rocket.exec_profile import ExecProfileBase
from c2wl_rocket.worker import Worker


class LocalToolExec(ExecProfileBase):
    def prepare(self):
        shutil.rmtree(test_out_dir)
        os.makedirs(test_out_dir)

    def execute(self):
        self.async_exec = False
        worker = Worker(
            self.job_info,
            workdir=test_out_dir,
            use_container=False
        )

        worker.run()
        self.out = worker.out
        self.success = worker.success
