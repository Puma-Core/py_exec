from django_prog.celery import app
from pistonpy import PistonApp
import json

python_app = PistonApp()


@app.task(name='check_runtimes')
def check_runtimes():
    """
    Check available runtimes in Piston
    """
    try:
        runtimes = python_app.get_runtimes()
        python_runtimes = [r for r in runtimes if r['language'] == 'python']
        print(f"All Python runtimes: {json.dumps(python_runtimes, indent=2)}")
        
        installed_runtimes = [r for r in python_runtimes if r.get('installed', False)]
        print(f"Installed Python runtimes: {json.dumps(installed_runtimes, indent=2)}")
        
        return {
            'all_python': python_runtimes,
            'installed': installed_runtimes
        }
    except Exception as e:
        print(f"Error checking runtimes: {e}")
        return None


@app.task(name='run_script')
def run_script(script_code: str) -> dict:
    """
    Run a Python script in a sandboxed environment.
    This task is asynchronous and can be executed by Celery workers.
    """
    print("Executing script...")

    try:
        # Verificar runtimes disponibles primero
        runtimes = python_app.get_runtimes()
        python_runtimes = [r for r in runtimes if r['language'] == 'python' and r.get('installed', False)]

        if not python_runtimes:
            return {
                'success': False,
                'error': 'No Python runtimes installed',
                'output': None
            }

        # Usar el primer runtime disponible
        runtime = python_runtimes[0]
        print(f"Using Python {runtime['language_version']}")

        output = python_app.run(
            language="python",
            version=runtime['language_version'],
            code=script_code,
        )

        print("Script executed successfully.")
        return {
            'success': True,
            'output': output,
            'runtime_used': runtime['language_version']
        }

    except Exception as e:
        print(f"Error executing script: {e}")
        return {
            'success': False,
            'error': str(e),
            'output': None
        }
