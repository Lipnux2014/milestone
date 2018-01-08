# wx web data msg type class


class Msg(object):
    def __init__(self, xml_data):
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_id = xml_data.find('MsgId').text
        self.content = ""


class TextMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.content = xml_data.find('Content').text.encode("utf-8")


class ImageMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.pic_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text
