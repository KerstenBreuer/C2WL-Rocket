import os, sys
import pytest
import shutil
import subprocess
import yaml
from . import *
sys.path.append(package_root)
from c2wl_rocket.worker import Worker


@pytest.mark.parametrize(
    "cwl, inputs, success_expected", 
    [
        get_cwl_job("touch")#,
        # get_cwl_job("touch_fail")
    ]
)
def test_basic_worker_process(cwl, inputs, success_expected):
    cleanup()
    
    with open(cwl, "r") as cwl_file:
        tool_dict = yaml.safe_load( cwl_file.read() )
    with open(inputs, "r") as input_file:
        inputs_dict = yaml.safe_load( input_file.read() )

    worker = Worker(
        tool=tool_dict,
        inputs=inputs_dict,
        workdir=test_out_dir,
        use_container=True,
        debug=True
    )

    worker.run()

    assert worker.success == success_expected, \
        f"Success status didn't met expections: {str(worker.success)}"

    # expected_output = 
    # assert os.path.join()


