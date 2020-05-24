import os
from .task_executor import TaskExecutor
from .web_app import create_app
from flask_restful import Resource, Api

task_executor = None

class SubmitTask(Resource):
    def post(
        self, 
        tool,
        inputs,
        workdir = None,
        tmpdir = None, 
        use_container = True,
        user_space_docker_cmd = "",
        force_docker_pull = False,
        singularity = False,
        debug = False,
        default_container = ""
    ):
        try:
            global task_executor 
            task_executor = TaskExecutor(
                tool = tool,
                inputs = inputs,
                workdir = workdir,
                tmpdir = tmpdir, 
                use_container = use_container,
                user_space_docker_cmd = user_space_docker_cmd,
                force_docker_pull = force_docker_pull,
                singularity = singularity,
                debug = debug,
                default_container = default_container
            )
            task_executor.run()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
class TaskStatus(Resource):
    def get(self):
        data = {}
        if task_executor is None:
            status = "No task submitted yet."
        else:
            data["task_output"] = task_executor.out
            status = "finished successfully" if task_executor.success else \
                "failed"
        data["task_status"] = status
        return data


def start(web_server_host, web_server_port):
    """
        Starts a remote worker service.
    """
    app = create_app(
        web_server_host=web_server_host,
        web_server_port=web_server_port
    )

    api = Api(app)
    api.add_resource(SubmitTask, '/submit_task')
    api.add_resource(TaskStatus, '/task_status')
    
    app.run()
