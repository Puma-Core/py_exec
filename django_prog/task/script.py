import traceback
from django_prog.celery import app
from asgiref.sync import async_to_sync
from aiohttp import ClientSession
from pistonpy import PistonApp

python_app = PistonApp()


@app.task(name='run_script')
def run_script(script_code: str,) -> bool:
    """
    Run a Python script in a sandboxed environment.
    This task is asynchronous and can be executed by Celery workers.
    """
    output = python_app.run(
        language="python",
        version="3.10.0",
        code=script_code,
    )
    print(f"Running script in sandbox... {output}")
    return True
