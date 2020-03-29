import os, sys

dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
package_root = os.path.join(dir_of_this_script, "..", "..")
test_out_dir = os.path.join(package_root, "test_out")
fixtures_dir = os.path.join(dir_of_this_script, "fixtures")
c2wl_cmdl_entry_point = os.path.join(dir_of_this_script, "../../c2wl_rocket.py")