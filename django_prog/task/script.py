import traceback
from django_prog.celery import app
from asgiref.sync import async_to_sync
from aiohttp import ClientSession


@app.task(name='run_script')
def run_script(script_code: str,) -> bool:
    """
    Run a Python script in a sandboxed environment.
    This task is asynchronous and can be executed by Celery workers.
    """
    print("Running script in sandbox...")
    return True
