from typing import Any
from httpx import URL
from requests import Session
from django_prog.integrations.env_script.interfaces import ENVInterface
from django_prog.integrations.languages import PYTHON

class PistonIntegration(ENVInterface):
    class Endpoints:
        Execute = "execute"
    
    def __init__(self, piston_api: URL, session: Session) -> None:
        super().__init__()
        self.piston_api = piston_api
        self.session = session


    def run_code(self, code: str, python_version: PYTHON.VERSION) -> dict[str, Any]:
        """
        Run the provided code using the Piston integration.
        This method sends the code to the Piston service and returns the output.
        """
        payload = {
            "language": PYTHON,
            "version": python_version,
            "files": [
                {
                    "name": "main.py",
                    "content": code
                }
            ]
        }
        try:
            full_url = self.piston_api / self.Endpoints.Execute
            response = self.session.post(
                url=full_url,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error running code: {e}")
            return e.__dict__
        except Exception as e:
            print(f"Error running code: {e}")
            return e.__dict__
        