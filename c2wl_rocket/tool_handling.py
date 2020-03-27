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
from .exec_profile import LocalToolExec


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
        
        exec_profile = LocalToolExec(job_info)

        exec_profile.deploy()

        outputs = exec_profile.out
        processStatus = "success" if exec_profile.success \
            else "permanentFail"

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