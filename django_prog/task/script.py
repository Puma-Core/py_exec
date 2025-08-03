from requests import Session

from django_prog.celery import app
from django_prog.integrations.languages import PYTHON
from django_prog.integrations.env_script.repository import ENVRepository
from django_prog.integrations.env_script.piston import PistonIntegration
from django_prog.settings import PISTON_DOMAIN

@app.task(name='run_script')
def run_script(script_code: str) -> dict:
    """
    Run a Python script in a sandboxed environment.
    This task is asynchronous and can be executed by Celery workers.
    """
    session = Session()
    try:
        env_integration = PistonIntegration(
            piston_api=PISTON_DOMAIN,
            session=session
        )
        env_repo = ENVRepository(env_integration=env_integration)

        python_version = PYTHON.VERSION.v_3_12
        result = env_repo.run_code(
            code=script_code,
            python_version=python_version
        )
        
        return result

    except Exception as e:
        print(f"Error executing script: {e}")
        return {
            'success': False,
            'error': str(e),
            'output': None
        }
