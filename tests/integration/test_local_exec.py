import os, sys
import pytest
import argparse
import shutil
import subprocess

dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
test_out_dir = os.path.join(dir_of_this_script, "../../test_out")
fixtures_dir = os.path.join(dir_of_this_script, "fixtures")
c2wl_cmdl_entry_point = os.path.join(dir_of_this_script, "../../c2wl_rocket.py")

sys.path.append(os.path.join(dir_of_this_script, "..", ".."))
import c2wl_rocket.__main__

def get_job(name_cwl, name_input=None):
    name_input = name_input if name_input is not None else name_cwl
    input = os.path.join(fixtures_dir, f"{name_input}.yaml") 
    cwl = os.path.join(fixtures_dir, f"{name_cwl}.cwl") 
    return cwl, input


@pytest.mark.parametrize(
    "cwl, inputs", 
    [
        get_job("touch")
    ]
)
def test_succeeding_jobs(cwl, inputs):
    c2wl_rocket.__main__.run(
        cwl, 
        inputs, 
        outdir=test_out_dir,
        debug=True
    )
    shutil.rmtree(test_out_dir)



@pytest.mark.parametrize(
    "cwl, inputs", 
    [
        get_job("touch_fail")
    ]
)
def test_failing_jobs(cwl, inputs):
    p = subprocess.Popen(
            [
                "python3",
                c2wl_cmdl_entry_point,
                "--debug",
                "--outdir",
                test_out_dir,
                cwl,
                inputs
            ],
            stderr=subprocess.PIPE
        )
    exit_code = p.wait()
    stderr = str(p.stderr.read()).split("\\n")
    assert stderr[-2] == "Final process status is permanentFail", \
        "Final process status is not permanentFail."
    assert exit_code != 0, "Test passed but it should have failed."

