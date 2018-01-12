import xml.etree.ElementTree as eT
from . import dtos
from .consts import ReplyConst, DEFAULT_BILL_ID
from datetime import datetime


def parse_data(web_data):
    if len(web_data) == 0:
        return None
    xml_data = eT.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return dtos.TextMsg(xml_data)
    elif msg_type == 'image':
        return dtos.ImageMsg(xml_data)


def convert_date(bill_date):
    """
    convert datetime to "YYYY-mm-dd"
    """
    return "{}-{}-{}".format(bill_date.year, bill_date.month, bill_date.day)


def return_wrapper(func):
    def add_return_info(*args, **kwargs):
        xml_form = """
                <xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{content}]]></Content>
                </xml>
                """
        reply_dict = args[0].__dict__
        try:
            content = func(*args, **kwargs)
        except Exception as e:
            print(e)
        reply_dict["content"] = content
        return xml_form.format(**reply_dict)

    return add_return_info


def convert_reply(return_str, rec_msg):
    xml_form = """
                    <xml>
                    <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                    <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                    <CreateTime>{create_time}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{content}]]></Content>
                    </xml>
                    """
    rec_msg_dict = rec_msg.__dict__
    rec_msg_dict["content"] = return_str
    return xml_form.format(**rec_msg_dict)


def joint_bill_info(bills):
    if len(bills) == 0:
        return ReplyConst.NO_DATA_REPLY.value
    reply_info = list()
    reply_info.append("编号 时间 描述 金额")
    amount_sum = 0
    for bill in bills:
        reply_info.append("{} {} {} {}".format(bill.id, convert_date(bill.created_time), bill.bill_description,
                                               bill.bill_amount))
        amount_sum += bill.bill_amount
    reply_info.append("{} {} {} {}".format(DEFAULT_BILL_ID, convert_date(datetime.now()), "总计花费", amount_sum))
    return "\n".join(reply_info)
