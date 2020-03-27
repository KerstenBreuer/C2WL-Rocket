from .worker import Worker
from .error_handling import error_message
from cwltool.loghandler import _logger as logger
from time import sleep
import sys



class ExecProfileBase:
    """
        Template for an exec profile:
            - method "exec" is required
            - methods "monitor", "prepare", "monitor", "finalize" are optional
            - method "monitor" is required when "exec" 
                is executing asynchonously (self.async_exec=True):
                    e.g. if "exec" only triggers the execution on a remote worker,
                    then "monitor" has to be invoked every few seconds to check
                    for completion / status of execution.
    """

    def __init__(
        self,
        job_info:dict
    ):
        self.job_info = job_info
        self.tool = job_info["tool"]
        self.inputs = job_info["inputs"]
        self.commandline = job_info["commandline"]
        self.resources = job_info["resources"]
        self.out = {}
        self.success = None # indicates success of task execution:
                            #   - None if not completed yet
                            #   - False if not completed with error
                            #   - True if not completed successfully
        self.seconds_between_monitor = 4


        if not hasattr(self, "execute"):
            logger.error(
                error_message(
                    "Initializing Exec Profile",
                    "The execute method is required but has not been described in the exec profile.",
                    is_known=True
                )
            )
            sys.exit(1)

        self.exec_plan = [
            {
                "name": "prepare",
                "method": self.prepare if hasattr(self, "prepare") else None
            },
            {
                "name": "execute",
                "method": self.execute
            },
            {
                "name": "monitor",
                "method": self.monitor if hasattr(self, "monitor") else None
            },
            {
                "name": "finalize",
                "method": self.finalize if hasattr(self, "finalize") else None
            },

        ]

    def deploy(self):
        for m in self.exec_plan:
            method_name = m["name"]
            method = m["method"]
            print(method_name)
            try:

                if method is None:
                    continue

                logger.debug(
                    f"[Exec Profile {method_name}] starting."
                )

                if method_name == "monitor":
                    while self.success is None:
                        logger.debug(
                            f"[Exec Profile {method_name}] Task execution not finished yet. Waiting."
                        )
                        sleep(self.seconds_between_monitor)
                        method()
                    
                    status = "success" if self.success else "failed"
                    logger.debug(
                        f"[Exec Profile {method_name}] Task execution finished with status: {status}"
                    )
                else:
                    method()

                    if method_name == "exec":
                        if self.success is None:
                            assert self.monitor is not None, \
                                "Exec method is done but task execution has not been finished " + \
                                "and no \"monitor\" methdod has been defined. " + \
                                "Have you forgot to set the output"
                            logger.debug(
                                f"[Exec Profile {method_name}] Execution is started " + \
                                "and continued in the background."
                            )
                        else:
                            status = "success" if self.success else "failed"
                            logger.debug(
                                f"[Exec Profile {method_name}] Task execution finished with status: {status}"
                            )
                    else:
                        logger.debug(
                            f"[Exec Profile {method_name}] completed."
                        )


            except AssertionError as e:
                logger.error(
                    f"[Exec Profile {method_name}] Error with known origin occured: {e}"
                )
                self.success = False
            except Exception as e:
                logger.error(
                    f"[Exec Profile {method_name}] Unkown error occured: {e}"
                )
                self.success = False
            
        


class LocalToolExec(ExecProfileBase):
    def execute(self):
        self.async_exec = False
        worker = Worker(
            self.job_info
        )

        worker.run()
        self.out = worker.out
        self.success = worker.success
