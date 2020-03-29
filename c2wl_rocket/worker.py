import os
import json
from cwltool.executors import SingleJobExecutor
from cwltool.context import LoadingContext, RuntimeContext
from cwltool.factory import Factory

from .log_handling import error_message

from random import choice as random_choice
from string import ascii_letters, digits
from random import random
import shutil

class Worker():
    def __init__(
        self,
        job_info:dict,
        workdir = None, # contains tmp and out dir 
                        # if tmp not specified separately
        tmpdir = None, 
        use_containers = True,
        user_space_docker_cmd = "",
        force_docker_pull = False,
        singularity = True,
        debug = False,
        default_container = ""
    ):
        random_string = "".join([random_choice(ascii_letters + digits) for c in range(0,14)])
        self.tool = job_info["tool"]
        self.inputs = job_info["inputs"]
        if workdir is None:
            workdir = os.getcwd()

        assert (not os.path.exists(workdir)) or os.path.isdir(workdir), \
            error_message(
                "worker",
                f"Message workdir exists but is not a directory: {workdir}",
                is_known=True
            )

        self.workdir = workdir if not os.path.exists(workdir) \
            else os.path.join(workdir, random_string)
        os.makedirs(self.workdir)
        
        self.inputs_file = os.path.join(self.workdir, "inputs.json")
        with open(self.inputs_file, "w") as inp_file:
            inp_file.write(json.dumps(self.inputs, indent=2))

        self.cwl_file = os.path.join(self.workdir, "tool.cwl")
        with open(self.cwl_file, "w") as cwl_file:
            cwl_file.write(json.dumps(self.tool, indent=2))

        self.tmpdir = tmpdir if tmpdir \
            else os.path.join(self.workdir, "tmp")
        os.mkdir(self.tmpdir)
        self.outdir = os.path.join(self.workdir, "out")
        os.mkdir(self.outdir)

        self.loading_context = LoadingContext()
        self.runtime_context = RuntimeContext()

        self.runtime_context.use_containers = use_containers
        self.runtime_context.user_space_docker_cmd = user_space_docker_cmd
        self.runtime_context.force_docker_pull = force_docker_pull
        self.runtime_context.singularity = singularity
        self.runtime_context.use_containers = use_containers
        self.runtime_context.use_containers = use_containers
        self.runtime_context.use_containers = use_containers


        fac = Factory(
            loading_context=self.loading_context, 
            runtime_context=self.runtime_context
        )
        self.callable_tool = fac.make(self.cwl_file)

        self.out = {}
        
    def run(self):
        try:
            self.out = self.callable_tool(**self.inputs)
            self.success = True
        except:
            self.success = False
    
    def delete_workdir(self):
        shutil.rmtree(self.workdir)

            


    
