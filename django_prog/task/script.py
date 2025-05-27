import traceback
from microsandbox import PythonSandbox
from django_prog.celery import app
from asgiref.sync import async_to_sync
from microsandbox.execution import Execution
from aiohttp import ClientSession


@app.task(name='run_script')
def run_script(script_code: str,) -> bool:
    """
    Run a Python script in a sandboxed environment.
    This task is asynchronous and can be executed by Celery workers.
    """
    async def wrapper() -> Execution | None:
        session = ClientSession()

        sandbox = PythonSandbox(server_url="http://puma_sandbox:5556")
        result = None
        print(f"Executing script: {script_code}")
        try:
            sandbox._session = session
            await sandbox.start()
            async with sandbox.create() as sb:
                result = await sb.run(script_code)
                print(f"Script executed successfully: {result}")
        finally:
            await sandbox.stop()
            await session.close()
        return result
    try:
        print(f"Starting script execution: {script_code}")
        result = async_to_sync(wrapper)()
        print(f"Script result: {result}")
        if not result:
            print("Script execution failed.")
            return False
        return True
    except Exception as e:
        print("Error executing script:", e)
        traceback.print_exc()
        return False
