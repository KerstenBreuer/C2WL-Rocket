"""
    This module makes adaptions to the CommandLineTool class of cwltool.command_line_tool
    so that tool execution is handle via the functions defined in the execution profile.
"""

from cwltool.job import JobBase
from cwltool.command_line_tool import CommandLineTool
from cwltool.workflow import default_make_tool
import json
import functools
from .worker import Task
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
        tool=None, # tool object
        exec_profile_class=None,
        workflow_metadata=None
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
        self.exec_profile_class = exec_profile_class if exec_profile_class is not None \
            else LocalToolExec
        self.workflow_metadata = workflow_metadata

    def run(
        self,
        runtimeContext     # type: RuntimeContext
    ):  # type: (...) -> None
        tool_dict = json.loads(json.dumps(self.tool))
        if "cwlVersion" not in tool_dict:
            tool_dict["cwlVersion"] = self.workflow_metadata["cwlVersion"]
        
        exec_profile = self.exec_profile_class(
            tool=tool_dict,
            inputs=self.joborder,
            resources=self.builder.resources,
            commandline=self.command_line,
            workflow_metadata=self.workflow_metadata
        )

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
    def __init__(
        self, 
        toolpath_object, 
        loadingContext,
        exec_profile_class=None,
        workflow_metadata=None
    ):
        super().__init__(
            toolpath_object, 
            loadingContext
        )
        self.exec_profile_class = exec_profile_class
        self.workflow_metadata = workflow_metadata

    def make_job_runner(self,
        runtimeContext       # type: RuntimeContext
    ):  # type: (...) -> Type[JobBase]


        return functools.partial(
            ExecProfileJob, 
            tool=self.tool, # bind tool object to job
            exec_profile_class=self.exec_profile_class, # bind custom exec profile class to job
            workflow_metadata=self.workflow_metadata
        )


def make_custom_tool(spec, loading_context, exec_profile_class, workflow_metadata):
    """
        custom tool maker: 
            only use ExecProfileCommandlineTool if spec if the spec is a "CommandLineTool",
            otherwise use the cwltool's standard tool maker
    """
    if "class" in spec and spec["class"] == "CommandLineTool":
        return ExecProfileCommandlineTool(
            spec, 
            loading_context, 
            exec_profile_class, 
            workflow_metadata
        )
    return default_make_tool(spec, loading_context)