# import cwltool.factory
# from cwltool.job import JobBase
# from cwltool.command_line_tool import CommandLineTool

import sys
import json
import importlib.util
spec = importlib.util.find_spec('cwltool')
_cwltool_ = importlib.util.module_from_spec(spec)
sys.modules['_cwltool_'] = _cwltool_



import sys
import importlib.util
import cwltool

SPEC_CWLTOOL = importlib.util.find_spec('cwltool')
cwltool_ = importlib.util.module_from_spec(SPEC_CWLTOOL)
SPEC_CWLTOOL.loader.exec_module(cwltool_)
sys.modules['cwltool_'] = cwltool_
del SPEC_CWLTOOL


cwltool_.co

assert os1 is not os2, \
    "Module `os` instancing failed"




###########################################################
class CustomExecProfileJob(_cwltool_.job.JobBase):
    def run(
        self,
        runtimeContext     # type: RuntimeContext
    ):  # type: (...) -> None
        tool_dict = json.loads(json.dumps(self.tool))
        job_info = {
            "inputs": self.joborder,
            "resources": self.builder.resources,
            "commandline": self.command_line,
            "tool_dict": tool_dict
        }
        outputs = {
            "test_file": {
                "location": "file:///mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/test",
                "basename": "test",
                "class": "File",
                "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
                "size": 0,
                "path": "/mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/test"
            }
        }
        processStatus="success"
        with runtimeContext.workflow_eval_lock:
            self.output_callback(outputs, processStatus)

def make_job_runner(self,
    runtimeContext       # type: RuntimeContext
):  # type: (...) -> Type[JobBase]
    return( CustomExecProfileJob )

_cwltool_.command_line_tool.CommandLineTool.make_job_runner = make_job_runner

####################################################################

prepare_job = _cwltool_.CommandLineTool.job

def job(self,
            job_order,         # type: Dict[Text, Text]
            output_callbacks,  # type: Callable[[Any, Any], Any]
            runtimeContext     # type: RuntimeContext
):
    prep_j = prepare_job(self,
            job_order,
            output_callbacks,
            runtimeContext
    )
    for j in prep_j:
        j.tool = self.tool
        yield j

_cwltool_.CommandLineTool.job = job

#######################################

fac = _cwltool_.factory.Factory()
touch = fac.make("touch.cwl")
result = touch(filename="test")
