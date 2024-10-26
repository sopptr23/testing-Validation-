import json
from typing import List, Dict

from fpdf import FPDF  # To install: `pip install fpdf2`


def save_html_report(data: str, filename: str) -> None:
    """
    Saves HTML content as a file, handy for viewing in web browsers.

    Args:
        data (str): HTML content.
        filename (str): File path to save HTML content.
    """
    with open(filename, "w") as file:
        file.write(data)


def save_json_report(
    data: Dict[str, List[Dict[str, str]]],
    filename: str,
    single_category: str,
    single_property: str,
    single_value: str,
) -> None:
    """
    Saves data as JSON. Ideal for data exchange or further processing.

    Args:
        data: The structured data to save.
        filename: Where to save the JSON file.
        single_category: Assessment category.
        single_property: Assessment criteria.
        single_value: Assessment value rule.
    """
    report_data = {
        "Assessment Criteria": {
            "Category": single_category,
            "Property": single_property,
            "Value": single_value,
        },
        "Results": data,
    }
    with open(filename, "w") as file:
        json.dump(report_data, file, indent=4)


def generate_pdf_report(
    data: Dict[str, List[Dict[str, str]]],
    filename: str,
    single_category: str,
    single_property: str,
    single_value: str,
) -> None:
    """
    Generates a PDF report. Suitable for official documentation.

    Args:
        data: Data to be included in the report.
        filename: PDF file to save.
        single_category: Assessment category.
        single_property: Assessment criteria.
        single_value: Assessment value rule.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Report", ln=True, align="C")
    criteria_info = f"Criteria: {single_category} - {single_property} - {single_value}"
    pdf.cell(200, 10, txt=criteria_info, ln=True)
    pdf.cell(200, 10, txt="Name | Type | Family | ID | Status", ln=True)

    for status, objects in data.items():
        for obj in objects:
            obj_info = f"{obj['name']} | {obj['type']} | {obj['family']} | {obj['id']} | {status}"
            pdf.cell(200, 10, txt=obj_info, ln=True)

    pdf.output(filename)


def generate_html_report(
    data: Dict[str, List[Dict[str, str]]],
    single_category: str,
    single_property: str,
    single_value: str,
) -> str:
    """
    Generates HTML content for the report. Easily styled and readable.

    Args:
        data: The data to display.
        single_category: Assessment category.
        single_property: Assessment criteria.
        single_value: Assessment value rule.
    """
    html_content = "<html><head><title>Report</title></head><body>"
    criteria_header = (
        f"<h1>Report: {single_category} - {single_property} - {single_value}</h1>"
    )
    html_content += criteria_header
    html_content += "<table border='1'>"
    html_content += (
        "<tr><th>Name</th><th>Type</th><th>Family</th><th>ID</th><th>Status</th></tr>"
    )

    for status, objects in data.items():
        for obj in objects:
            row = (
                f"<tr><td>{obj['name']}</td><td>{obj['type']}</td>"
                f"<td>{obj['family']}</td><td>{obj['id']}</td><td>{status}</td></tr>"
            )
            html_content += row

    html_content += "</table></body></html>"
    return html_content


def generate_report(
    assessed_objects: Dict[str, List[Dict[str, str]]],
    report_format: str,
    single_category: str,
    single_property: str,
    single_value: str,
) -> str:
    """
    Main function to orchestrate report generation in various formats.

    Args:
        assessed_objects: Categorized assessment data.
        report_format: The format to generate ('HTML', 'JSON', 'PDF').
        single_category: Assessment category.
        single_property: Assessment criteria.
        single_value: Assessment value rule.
    """
    report_filename = f"report.{report_format.lower()}"

    if report_format == "HTML":
        html_report = generate_html_report(
            assessed_objects, single_category, single_property, single_value
        )
        save_html_report(html_report, report_filename)
    elif report_format == "JSON":
        save_json_report(
            assessed_objects,
            report_filename,
            single_category,
            single_property,
            single_value,
        )
    elif report_format == "PDF":
        generate_pdf_report(
            assessed_objects,
            report_filename,
            single_category,
            single_property,
            single_value,
        )
    else:
        raise ValueError("Unsupported report format")

    return report_filename