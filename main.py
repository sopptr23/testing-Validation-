from pydantic import Field
from speckle_automate import AutomateBase, AutomationContext, execute_automate_function
import xml.etree.ElementTree as ET

class FunctionInputs(AutomateBase):
    """Define inputs for the Speckle Automate function."""
    ids_xml_file: str = Field(
        title="IDS XML File Path",
        description="Path to the XML file containing BIM validation requirements."
    )


def parse_xml_requirements(xml_file_path):
    """Parse XML to extract BIM requirements for different check categories."""
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    checks = {
        "performance": [],
        "location": [],
        "views": [],
        "family": [],
        "custom": []
    }

    for check in root.findall('.//Check'):
        check_info = {
            'name': check.get('CheckName'),
            'description': check.get('Description'),
            'type': check.get('CheckType'),
            'condition': check.get('ResultCondition'),
            'failure_message': check.get('FailureMessage'),
            'filters': []
        }
        
        # Extract filters that define specific property checks
        for filter_elem in check.findall('Filter'):
            filter_info = {
                'property': filter_elem.get('Property'),
                'condition': filter_elem.get('Condition'),
                'value': filter_elem.get('Value')
            }
            check_info['filters'].append(filter_info)
        
        # Organize checks by their intended category
        if "performance" in check_info['name'].lower():
            checks["performance"].append(check_info)
        elif "location" in check_info['name'].lower():
            checks["location"].append(check_info)
        elif "view" in check_info['name'].lower():
            checks["views"].append(check_info)
        elif "family" in check_info['name'].lower():
            checks["family"].append(check_info)
        else:
            checks["custom"].append(check_info)

    return checks


def check_performance(model_data, checks):
    """Run performance checks on the model data."""
    results = []
    for check in checks:
        if check['type'] == "CountOnly":
            count = sum(1 for obj in model_data if obj.get(check['filters'][0]['property']))
            results.append({
                'name': check['name'],
                'result': count,
                'status': 'Passed' if count <= int(check['filters'][0]['value']) else 'Failed',
                'message': check['failure_message'] if count > int(check['filters'][0]['value']) else ''
            })
    return results


def check_location(model_data, checks):
    """Run location checks on the model data."""
    results = []
    for check in checks:
        passed = True
        for obj in model_data:
            for filter_ in check['filters']:
                if obj.get(filter_['property']) != filter_['value']:
                    passed = False
                    break
            if not passed:
                break
        results.append({
            'name': check['name'],
            'status': 'Passed' if passed else 'Failed',
            'message': '' if passed else check['failure_message']
        })
    return results


def run_all_checks(model_data, xml_file_path):
    """Run all validation checks on the model data."""
    checks = parse_xml_requirements(xml_file_path)
    performance_results = check_performance(model_data, checks['performance'])
    location_results = check_location(model_data, checks['location'])
    all_results = performance_results + location_results
    return all_results


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs
) -> None:
    """Speckle Automate function to validate model based on XML requirements."""

    # Receive model data from Speckle context
    version_root_object = automate_context.receive_version()
    model_data = version_root_object.get("model")  # Flatten if necessary

    # Run all validation checks
    results = run_all_checks(model_data, function_inputs.ids_xml_file)

    # Log results
    for result in results:
        status = result['status']
        message = result['message']
        if status == "Failed":
            automate_context.log_failure(f"{result['name']} failed: {message}")
        else:
            automate_context.log_info(f"{result['name']} passed.")

    # Set output data as the final report
    automate_context.set_output_data("validation_results", results)


# Execute the function
execute_automate_function(automate_function)
