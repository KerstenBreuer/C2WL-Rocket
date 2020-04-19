import os, sys

dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
package_root = os.path.join(dir_of_this_script, "..", "..")
test_out_dir = os.path.join(package_root, "test_out")
fixtures_dir = os.path.join(dir_of_this_script, "fixtures")
c2wl_cmdl_entry_point = os.path.join(dir_of_this_script, "../../c2wl_rocket.py")

def get_cwl_job(name_cwl, name_input=None):
    name_input = name_input if name_input is not None else name_cwl
    inputs = os.path.join(fixtures_dir, f"{name_input}.yaml") 
    cwl = os.path.join(fixtures_dir, f"{name_cwl}.cwl") 
    success_expected = "fail" not in name_cwl and "fail" not in name_input
    return cwl, inputs, success_expected