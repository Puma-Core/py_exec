from typing import Any
from requests import Session
from django_prog.integrations.env_script.interfaces import ENVInterface
from django_prog.integrations.languages import PYTHON

class PistonIntegration(ENVInterface):
    class Endpoints:
        Execute = "api/v2/execute"
        Runtimes = "api/v2/runtimes"
    
    def __init__(self, piston_api: str, session: Session) -> None:
        super().__init__()
        self.piston_api = piston_api.rstrip('/')  # Remover slash final si existe
        self.session = session


    def run_code(self, code: str, version: PYTHON.VERSION) -> dict[str, Any]:
        """
        Run the provided code using the Piston integration.
        This method sends the code to the Piston service and returns the output.
        """
        payload = {
            "language": PYTHON.NAME,
            "version": version,
            "files": [
                {
                    "name": "main.py",
                    "content": code
                }
            ]
        }
        try:
            full_url = f"{self.piston_api}/{self.Endpoints.Execute}"
            
            response = self.session.post(
                url=full_url,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            print(f"Error running code: {e}")
            return {"error": str(e)}

    def get_runtimes(self) -> list[dict[str, Any]]:
        """
        Get available runtimes from Piston
        """
        try:
            full_url = f"{self.piston_api}/{self.Endpoints.Runtimes}"
            
            response = self.session.get(url=full_url, timeout=30)
            
            response.raise_for_status()
            runtimes = response.json()
            return runtimes
        except Exception as e:
            print(f"Error getting runtimes: {e}")
            return []
        