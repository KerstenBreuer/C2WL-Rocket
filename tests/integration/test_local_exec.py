import os, sys
import pytest
import argparse
import shutil
import subprocess
from . import test_out_dir, package_root, fixtures_dir, \
    c2wl_cmdl_entry_point, dir_of_this_script
sys.path.append(package_root)
from .exec_profiles import LocalToolExec
import c2wl_rocket.__main__

def get_job(name_cwl, name_input=None):
    name_input = name_input if name_input is not None else name_cwl
    inputs = os.path.join(fixtures_dir, f"{name_input}.yaml") 
    cwl = os.path.join(fixtures_dir, f"{name_cwl}.cwl") 
    success_expected = "fail" not in name_cwl and "fail" not in name_input
    return cwl, inputs, success_expected


# @pytest.mark.parametrize(
#     "cwl, inputs, success_expected", 
#     [
#         get_job("touch"),
#         get_job("trim_and_map")
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
        get_job("touch"),
        get_job("trim_and_map")
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
    final_status = stderr[-2]
    assert "Final process status" in final_status, \
        f"No final process status detected in log."
    if success_expected:
        assert final_status == "Final process status is success", \
            f"Success expected but final status message was: \"{final_status}\""
    else:
        assert final_status == "Final process status is permanentFail", \
            f"Fail expected but final status message was: \"{final_status}\""
    
    # check exit code:
    if success_expected:
        assert exit_code == 0, "Success expected but exit code is non-zero."
    else:
        assert exit_code != 0, "Fail expected but exit code is zero."


