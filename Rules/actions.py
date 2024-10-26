from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List

from speckle_automate import AutomationContext


# Base class for defining actions to be taken on parameters in Speckle data.
class ParameterAction(ABC):
    """
    A base class for creating actions that can be applied to parameters in
    Speckle objects. This abstract class outlines the structure and mandates
    the implementation of specific methods in derived classes.
    """

    def __init__(self) -> None:
        # Dictionary for tracking affected parameters. Key: parent object's ID,
        # Value: list of affected parameter names.
        self.affected_parameters: Dict[str, List[str]] = defaultdict(list)

    @abstractmethod
    def apply(self, parameter: Dict[str, str], parent_object: Dict[str, str]) -> None:
        """
        Applies the specific logic of the action to a parameter.

        Args:
            parameter: The parameter to which the action is applied.
            parent_object: The object that holds the parameter.
        """
        pass

    @abstractmethod
    def report(self, automate_context: AutomationContext) -> None:
        """
        Generates a report based on the results of applying the action.

        Args:
            automate_context: The context in which the automation is executed,
            providing mechanisms for attaching results to the Speckle model.
        """
        pass

# Further specific action classes can be defined here, inheriting from
# ParameterAction and implementing the abstract methods 'apply' and 'report'.