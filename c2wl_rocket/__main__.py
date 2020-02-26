from __future__ import absolute_import
import argparse
import cwltool.main
import cwltool.argparser
from cwltool.executors import MultithreadedJobExecutor, SingleJobExecutor
from .tool_runner import make_custom_tool
from copy import copy

## get cwltool default args:
cwltool_ap = cwltool.argparser.arg_parser()
cwltool_default_args = cwltool_ap.parse_args([])

def main():
    parser = argparse.ArgumentParser(
        prog="C2WL-Rocket",
        description='Customizable CWL Rocket - A highly flexible CWL execution engine.'
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
    
    parsed_args = parser.parse_args()


    
    args = copy(cwltool_default_args)
    args.workflow = parsed_args.cwl_document
    args.job_order = parsed_args.input_params

    loading_context = cwltool.main.LoadingContext(vars(args))
    loading_context.construct_tool_object = make_custom_tool
    runtime_context = cwltool.main.RuntimeContext(vars(args))
    job_executor = MultithreadedJobExecutor() if args.parallel \
        else SingleJobExecutor()
    job_executor.max_ram = job_executor.max_cores = float("inf")
    
    # hand arguments over to main exec function:
    cwltool.main.main(
        args=args,
        executor=job_executor,
        loadingContext=loading_context,
        runtimeContext=runtime_context
    )

if __name__ == "__main__":
    main()
