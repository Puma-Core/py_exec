from abc import ABC
from typing import Any


class ENVInterface(ABC):
    """
    Abstract base class for environment script integrations.
    This class defines the interface for running code in different environments.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def run_code(self, code: str, python_version: str) -> dict[str, Any]:
        """
        Run the provided code using the integration.
        This method should be implemented by subclasses to execute code in the specific environment.
        """
        raise NotImplementedError("Subclasses must implement this method.")