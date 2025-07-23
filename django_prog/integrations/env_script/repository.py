from typing import Any
from httpcore import URL
from requests import Session

from django_prog.integrations.env_script.interfaces import ENVInterface
from django_prog.integrations.languages import PYTHON


class ENVRepository:
    """
    A repository for managing environment scripts.
    """
    def __init__(self, env_integration: ENVInterface) -> None:
        self.env_integration = env_integration

    def run_code(self, code: str, python_version: PYTHON.VERSION) -> dict[str, Any]:
        """
        Run the provided code using the Piston API.
        """
        return self.env_integration.run_code(code, python_version)