"""
    This module makes adaptions to the CommandLineTool class of cwltool.command_line_tool
    so that tool execution is handle via the functions defined in the execution profile.
"""

from cwltool.job import JobBase
from cwltool.command_line_tool import CommandLineTool
from cwltool.workflow import default_make_tool
import json
import functools
from .worker import Worker


class ExecProfileJob(JobBase):
    """
        Defines a custom JobBase class with a run method 
        that interates over the exec profile functions:
    """
    def __init__(
        self,
        builder,   # type: Builder
        joborder,  # type: Dict[Text, Union[Dict[Text, Any], List, Text, None]]
        make_path_mapper,  # type: Callable[..., PathMapper]
        requirements,  # type: List[Dict[Text, Text]]
        hints,  # type: List[Dict[Text, Text]]
        name,   # type: Text
        tool=None # tool object
    ):  # type: (...) -> None
        super().__init__(
                 builder,
                 joborder,
                 make_path_mapper,
                 requirements,
                 hints,
                 name
        )
        self.tool = tool

    def run(
        self,
        runtimeContext     # type: RuntimeContext
    ):  # type: (...) -> None
        tool_dict = json.loads(json.dumps(self.tool))
        job_info = {
            "inputs": self.joborder,
            "resources": self.builder.resources,
            "commandline": self.command_line,
            "tool": tool_dict
        }
        print(job_info)
        worker = Worker(job_info)
        worker.run()
        outputs = worker.out
        print(outputs)

        # outputs = {
        #     "test_file": {
        #         "location": "file:///mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/test",
        #         "basename": "test",
        #         "class": "File",
        #         "checksum": "sha1$da39a3ee5e6b4b0d3255bfef95601890afd80709",
        #         "size": 0,
        #         "path": "/mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/test"
        #     }
        # }
        processStatus="success"
        with runtimeContext.workflow_eval_lock:
            self.output_callback(outputs, processStatus)


class ExecProfileCommandlineTool(CommandLineTool):
    """
        Overwrite the make_job_runner
        so that it always returns the ExecProfileJob class:
    """
    def make_job_runner(self,
        runtimeContext       # type: RuntimeContext
    ):  # type: (...) -> Type[JobBase]


        return functools.partial(
            ExecProfileJob, 
            tool=self.tool # bind tool object to job
        )


def make_custom_tool(spec, loading_context):
    """
        custom tool maker: 
            only use ExecProfileCommandlineTool if spec if the spec is a "CommandLineTool",
            otherwise use the cwltool's standard tool maker
    """
    if "class" in spec and spec["class"] == "CommandLineTool":
        return ExecProfileCommandlineTool(spec, loading_context)
    return default_make_tool(spec, loading_context)