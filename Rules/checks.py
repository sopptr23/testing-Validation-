# Required imports
from typing import Callable, Dict, Union

from specklepy.objects import Base


# We're going to define a set of rules that will allow us to filter and
# process parameters in our Speckle objects. These rules will be encapsulated
# in a class called `ParameterRules`.


class BaseObjectRules:
    """
    A collection of rules for processing parameters in Speckle objects.

    This class provides static methods that return lambda functions. These
    lambda functions serve as filters or conditions we can use in our main
    processing logic. By encapsulating these rules, we can easily extend
    or modify them in the future.
    """

    @staticmethod
    def speckle_type_rule(desired_type: str) -> Callable[[Base], bool]:
        """
        Rule: Check if a parameter's speckle_type matches the desired type.
        """
        return (
            lambda parameter: getattr(parameter, "speckle_type", None) == desired_type
        )

    @staticmethod
    def forbidden_prefix_rule(given_prefix: str) -> Callable[[Base], bool]:
        """
        Rule: check if a parameter's name starts with a given prefix.

        This is a simple check, but there could be more complex naming rules for parameters of
        different types. For example, a rule that checks if a parameter's name starts with a given string
        exists particularly within IFC where parameters are often prefixed with "Ifc" or "Pset".
        """
        return lambda parameter: parameter.name.startswith(given_prefix)

    # This example Automate function is for prefixed parameter removal. Additional example rules below follow the same
    # pattern, but with different logic. In some instances there is a strong coupling between the action and the checking
    # logic, and in others there is a looser coupling. Which is why I have defined the actions separately from the
    # checking logic.

    @staticmethod
    def has_missing_value(parameter: Union[Base, Dict[str, str]]) -> bool:
        """
        Rule: Missing Value Check.

        The AEC industry often requires all parameters to have meaningful values.
        This rule checks if a parameter is missing its value, potentially indicating
        an oversight during data entry or transfer.
        """
        return not getattr(parameter, "value")

    @staticmethod
    def has_default_value(parameter: Dict[str, str]) -> bool:
        """
        Rule: Default Value Check.

        Default values can sometimes creep into final datasets due to software defaults.
        This rule identifies parameters that still have their default values, helping
        to highlight areas where real, meaningful values need to be provided.
        """
        return parameter.get("value") == "Default"

    @staticmethod
    def parameter_exists(parameter_name: str, parent_object: Dict[str, str]) -> bool:
        """
        Rule: Parameter Existence Check.

        For certain critical parameters, their mere presence (or lack thereof) is vital.
        This rule verifies if a specific parameter exists within an object, allowing
        teams to ensure that key data points are always present.
        """
        return parameter_name in parent_object.get("parameters", {})

    @staticmethod
    def is_category(category: str) -> Callable[[Base], bool]:
        """
        Rule: Category Check.

        This rule checks if a parameter's category matches the desired category.
        """
        return lambda parameter: getattr(parameter, "category", None) == category

    @staticmethod
    def parameter_name_is(parameter_name: str) -> Callable[[Base], bool]:
        """
        Rule: Parameter Name Check.

        This rule checks if a parameter's name matches the desired name.
        """
        return (
            lambda parameter: getattr(parameter, "name") is not None
                              and parameter.name == parameter_name
        )

    @staticmethod
    def parameter_value_startswith(prefix: str) -> Callable[[Base], bool]:
        """
        Rule: Parameter Name Starts With.

        This rule checks if a parameter's name starts with a given prefix.
        """
        return lambda parameter: parameter.name.startswith(prefix)

    @staticmethod
    def is_revit_parameter(parameter: Union[Base, Dict[str, str]]):
        """
        Checks if a parameter is a Revit parameter.

        This function checks if a parameter is a Revit parameter by checking if it
        has a 'category' property.
        """
        return (
                getattr(parameter, "speckle_type", None)
                == "Objects.BuiltElements.Revit.Parameter"
        )

    @staticmethod
    def evaluate_parameter(parameter, function_inputs):

        """Evaluates a parameter and returns its evaluation state."""
        if not BaseObjectRules.is_revit_parameter(parameter):
            return None

        if BaseObjectRules.has_missing_value(parameter):
            return "missing"

        value = getattr(parameter, "value", None)
        if value is not None and isinstance(value, str) and value.startswith(function_inputs.single_rule):
            return "passing"
        else:
            return "invalid"