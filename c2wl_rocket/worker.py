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
            global task 
            task = Task(
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
            task.run()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
class GetStatus(Resource):
    def get(self):
        out = task.out
        status = "finished successfully" if task.success else \
            "failed"
        return {
            "task_status": status,
            "task_output": out
        }


def start_worker(web_server_host, web_server_port):
    app = create_app(
        web_server_host=web_server_host,
        web_server_port=web_server_port
    )

    api = Api(app)
    api.add_resource(SubmitTask, '/submit_task')
    api.add_resource(GetStatus, '/get_status')
    
    app.run()
