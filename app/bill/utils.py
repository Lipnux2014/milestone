import xml.etree.ElementTree as eT
from . import dtos


def parse_data(web_data):
    if len(web_data) == 0:
        return None
    xml_data = eT.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return dtos.TextMsg(xml_data)
    elif msg_type == 'image':
        return dtos.ImageMsg(xml_data)

