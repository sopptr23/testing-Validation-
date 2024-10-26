from Rules.checks import BaseObjectRules


# Function to get type and family based on conditions
def get_type_and_family(obj):
    if getattr(obj, "speckle_type", None) == "Objects.Other.Revit.RevitInstance" and hasattr(obj, "definition"):
        return getattr(obj.definition, "type", "Unknown"), getattr(obj.definition, "family", "Unknown")
    return getattr(obj, "type", "Unknown"), getattr(obj, "family", "Unknown")


# Function to create object info
def create_object_info(obj, type_, family):
    return {
        "name": getattr(obj, "name", "Unknown"),
        "type": type_,
        "family": family,
        "id": getattr(obj, "id", "Unknown"),
    }


# Function to process parameters
def process_parameters(current_object, function_inputs):
    parameters = getattr(current_object, "parameters", None)
    if not parameters:
        return

    parameter_name_is = BaseObjectRules.parameter_name_is(function_inputs.single_property)

    for parameter_key in getattr(parameters, 'get_dynamic_member_names', lambda: [])():
        parameter = parameters[parameter_key]
        if parameter_name_is(parameter):
            return BaseObjectRules.evaluate_parameter(parameter, function_inputs)