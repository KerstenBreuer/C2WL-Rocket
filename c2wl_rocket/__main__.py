from __future__ import absolute_import
import os
import argparse
import cwltool.main
import cwltool.argparser
import cwltool.utils
from c2wl_rocket.exec_profile import LocalToolExec 
from cwltool.executors import MultithreadedJobExecutor, SingleJobExecutor
from .tool_handling import make_custom_tool
from copy import copy
import typing_extensions

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
     
        parser.add_argument("--outdir", 
            type=typing_extensions.Text,
            help="Output directory, default current directory",
            default=os.path.abspath('.')
        ) 
        
        exgroup = parser.add_mutually_exclusive_group()
        exgroup.add_argument("--tmp-outdir-prefix", 
            type=typing_extensions.Text,
            help="Path prefix for intermediate output directories",
            default=cwltool.utils.DEFAULT_TMP_PREFIX
        )

        exgroup.add_argument("--cachedir", 
            type=typing_extensions.Text,
            help="Directory to cache intermediate workflow outputs to avoid recomputing steps.",
            default=""
        )

        exgroup = parser.add_mutually_exclusive_group()
        exgroup.add_argument("--move-outputs", 
            action="store_const", 
            const="move", 
            default="move",
            help="Move output files to the workflow output directory and delete "
            "intermediate output directories (default).", 
            dest="move_outputs"
        )

        exgroup.add_argument("--leave-outputs", 
            action="store_const", 
            const="leave", 
            default="move",
            help="Leave output files in intermediate output directories.",
            dest="move_outputs"
        )

        exgroup.add_argument("--copy-outputs", 
            action="store_const", 
            const="copy", 
            default="move",
            help="Copy output files to the workflow output directory, don't delete intermediate output directories.",
            dest="move_outputs"
        )
        
        args = parser.parse_args()


    cwltool_args = copy(cwltool_default_args)
    cwltool_args.workflow = args.cwl_document
    cwltool_args.job_order = args.input_params
    cwltool_args.outdir = args.outdir
    cwltool_args.tmp_outdir_prefix = args.tmp_outdir_prefix
    cwltool_args.cachedir = args.cachedir
    cwltool_args.move_outputs = args.move_outputs
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

def run(
    cwl_document:str,
    input_params:str, 
    exec_profile=LocalToolExec, 
    outdir=os.path.abspath('.'),
    tmp_outdir_prefix=cwltool.utils.DEFAULT_TMP_PREFIX,
    cachedir="",
    move_outputs="move", # one of "move", "copy", or "leave"
    debug=False
):
    """
        Main API entry point. Executes c2wl_rocket.__main__.main"
    """
    args = argparse.Namespace(
        debug=debug,
        exec_profile=exec_profile,
        cwl_document=cwl_document,
        input_params=[input_params],
        outdir=outdir,
        tmp_outdir_prefix=tmp_outdir_prefix,
        cachedir=cachedir,
        move_outputs=move_outputs
    )
    main(args)

if __name__ == "__main__":
    main()