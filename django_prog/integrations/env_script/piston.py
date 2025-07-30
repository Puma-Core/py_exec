import traceback
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
            print(f"Sending request to: {full_url}")
            print(f"Payload: {payload}")
            
            response = self.session.post(
                url=full_url,
                json=payload,
                timeout=30
            )
            

            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"Response content: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            print(f"Response JSON: {result}")
            return result
        except Exception as e:
            traceback.print_exc()
            print(f"Error running code: {e}")
            return {"error": str(e)}

    def get_runtimes(self) -> list[dict[str, Any]]:
        """
        Get available runtimes from Piston
        """
        try:
            full_url = f"{self.piston_api}/{self.Endpoints.Runtimes}"
            print(f"Getting runtimes from: {full_url}")
            
            response = self.session.get(url=full_url, timeout=30)
            print(f"Runtimes response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Runtimes response content: {response.text}")
            
            response.raise_for_status()
            runtimes = response.json()
            print(f"Available runtimes: {runtimes}")
            return runtimes
        except Exception as e:
            traceback.print_exc()
            print(f"Error getting runtimes: {e}")
            return []
        