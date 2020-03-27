from __future__ import absolute_import
import argparse
import cwltool.main
import cwltool.argparser
from c2wl_rocket.exec_profile import LocalToolExec 
from cwltool.executors import MultithreadedJobExecutor, SingleJobExecutor
from .tool_handling import make_custom_tool
from copy import copy

## get cwltool default args:
cwltool_ap = cwltool.argparser.arg_parser()
cwltool_default_args = cwltool_ap.parse_args([])

def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(
            prog="C2WL-Rocket",
            description='Customizable CWL Rocket - A highly flexible CWL execution engine.'
        )

        parser.add_argument("--debug", 
            action="store_true", 
            help="Print debugging level messages."
        )

        parser.add_argument('-p', '--exec-profile',
            help="Specify an exec profile."
        )

        parser.add_argument('cwl_document',
            help="Provide a CWL workflow or tool."
        )
        
        parser.add_argument('input_params',
            nargs=argparse.REMAINDER,
            help="Provide input parameters in YAML or JSON format."
        )
        
        args = parser.parse_args()


    cwltool_args = copy(cwltool_default_args)
    cwltool_args.workflow = args.cwl_document
    cwltool_args.job_order = args.input_params
    cwltool_args.debug = args.debug


    loading_context = cwltool.main.LoadingContext(vars(cwltool_args))
    loading_context.construct_tool_object = make_custom_tool
    runtime_context = cwltool.main.RuntimeContext(vars(cwltool_args))
    job_executor = MultithreadedJobExecutor() if cwltool_args.parallel \
        else SingleJobExecutor()
    job_executor.max_ram = job_executor.max_cores = float("inf")

    # hand arguments over to main exec function:
    cwltool.main.main(
        args=cwltool_args,
        executor=job_executor,
        loadingContext=loading_context,
        runtimeContext=runtime_context
    )

def run(cwl_document, input_params, exec_profile=LocalToolExec, debug=False):
    """
        Main API entry point. Executes c2wl_rocket.__main__.main"
    """
    args = argparse.Namespace(
        debug=debug,
        exec_profile=exec_profile,
        cwl_document=cwl_document,
        input_params=[input_params]
    )
    main(args)

if __name__ == "__main__":
    main()