import json
import xml.sax

from easyparse.pkg.xml_to_json_handler import XmlToJsonHandler


def xml_to_json(xml_input_path, json_output_path):
    """
    Utilizes the xml parser to convert the given xml to json
    """
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    xml_handler = XmlToJsonHandler()
    parser.setContentHandler(xml_handler)
    parser.parse(xml_input_path)

    with open(json_output_path, 'w') as f:
        json.dump(xml_handler.get_json_dict(), f)
