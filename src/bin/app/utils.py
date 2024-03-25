import yaml
import xml.etree.ElementTree as ET

from fastapi import Response
from pandas import DataFrame


def format_csv(df: DataFrame):
    """
    Method to transform our output into a CSV content
    """
    # Using pandas to get data into CSV format
    csv_data = df.to_csv(index=False)
    csv_data = csv_data.replace('"', "")
    # Return the adapted response
    return Response(csv_data, media_type="text/csv")


def format_xml(df: DataFrame):
    """
    Method to transform our output into an XML Content
    """
    # The main tree will be call logs
    root = ET.Element("logs")
    for index, row in df.iterrows():
        # We create a new element for each call log
        row_element = ET.SubElement(root, "log")
        for col_name, col_value in row.items():
            ET.SubElement(row_element, col_name).text = str(col_value)

    # Create the string XML
    xml_data = ET.tostring(root, encoding="unicode", method="xml")

    # Return response
    return Response(content=xml_data, media_type="application/xml")


def format_yml(df: DataFrame):
    """
    Method to transform our output into an YAML Content
    """
    # Using YAML we transform a list of dict into a yaml content
    yaml_data = yaml.dump(df.to_dict(orient='records'))

    # Return response
    return Response(content=yaml_data, media_type="application/x-yaml")


def format_json(df:DataFrame):
    """
    Method to transform our output into an YAML Content
    """
    # Return the dataframe transformed into a JSON
    return Response(df.to_json(orient='records'), media_type="application/json")
