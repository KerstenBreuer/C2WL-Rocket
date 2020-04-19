import os, sys
import pytest
import argparse
import shutil
import subprocess
from . import test_out_dir, package_root, fixtures_dir, \
    c2wl_cmdl_entry_point, dir_of_this_script, get_cwl_job
sys.path.append(package_root)
from .exec_profiles import LocalToolExec
import c2wl_rocket.__main__


# @pytest.mark.parametrize(
#     "cwl, inputs, success_expected", 
#     [
#         get_cwl_job("touch"),
#         get_cwl_job("trim_and_map")
#     ]
# )
# def test_api_entry_point_jobs(cwl, inputs, success_expected):
#     c2wl_rocket.__main__.run(
#         cwl, 
#         inputs, 
#         outdir=test_out_dir,
#         exec_profile=LocalToolExec,
#         debug=True
#     )


@pytest.mark.parametrize(
    "cwl, inputs, success_expected", 
    [
        get_cwl_job("touch"),
        get_cwl_job("touch_fail")
    ]
)
def test_cmdl_entry_point_jobs(cwl, inputs, success_expected):
    p = subprocess.Popen(
            [
                "python3",
                c2wl_cmdl_entry_point,
                "--debug",
                "--exec-profile",
                os.path.join(dir_of_this_script, "exec_profiles.py") + ":LocalToolExec",
                "--outdir",
                test_out_dir,
                cwl,
                inputs
            ],
            stderr=subprocess.PIPE
        )
    exit_code = p.wait()
    stderr = str(p.stderr.read()).split("\\n")
    # check final status message in log:
    final_status = "\n".join(stderr[-2:-1])
    assert "Final process status" in final_status, \
        f"No final process status detected in log."
    if success_expected:
        assert "Final process status is success" in final_status, \
            f"Success expected but final status message was: \"{final_status}\""
    else:
        assert "Final process status is permanentFail" in final_status, \
            f"Fail expected but final status message was: \"{final_status}\""
    
    # check exit code:
    if success_expected:
        assert exit_code == 0, "Success expected but exit code is non-zero."
    else:
        assert exit_code != 0, "Fail expected but exit code is zero."


