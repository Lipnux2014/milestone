from flask import request, Blueprint
from app import db
from .consts import Commands, HELP_INFO, ReplyConst
from .models import BillBook
from .utils import parse_data
from .dtos import *
from .errors import InvalidInputError, ExceedAuthorityError
from datetime import datetime
import hashlib

mod_bill = Blueprint("bill", __name__)


@mod_bill.route("/")
def hello():
    return "Hello world!"


@mod_bill.route("/wx", methods=["GET"])
def verify():
    try:
        data = request.args
        if len(data) == 0:
            return "hello, this is handle view"
        signature = data.get("signature")
        timestamp = data.get("timestamp")
        nonce = data.get("nonce")
        echo_str = data.get("echostr")
        token = "lipnux"  # 请按照公众平台官网\基本配置中信息填写

        request_info_list = [token, timestamp, nonce]
        request_info_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, request_info_list)
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        return echo_str
        # if hashcode == signature:
        #     return echo_str
        # else:
        #     return ""
    except Exception as e:
        return e


@mod_bill.route("/wx", methods=["POST"])
def proxy():
    print(request.data)
    print(request.form)
    return
    data = request.data
    if len(data) == 0:
        return ReplyConst.INVALID_PARAMETER_REPLY.value
    rec_msg = parse_data(data)
    try:
        if isinstance(rec_msg, Msg) and rec_msg.msg_type == 'text':
            if rec_msg.content == Commands.HELP.value:
                return HELP_INFO
            if rec_msg.content == Commands.GET.value:
                return load_month(rec_msg)
            if rec_msg.content.startswith(Commands.DEL.value):
                return del_bill_by_id(rec_msg)
            else:
                return insert_bill(rec_msg)
        else:
            return ReplyConst.SILENCE_WX.value
    except InvalidInputError as e:
        return e.value
    except ExceedAuthorityError as e:
        return e.value
    except:
        return ReplyConst.UNKNOWN_ERROR_REPLY


def load_month(rec_msg):
    bills = BillBook.query \
        .filter_by(is_valid=1) \
        .filter_by(bill_keeper=rec_msg.from_user_name) \
        .filter(BillBook.create_time.year == datetime.now().year) \
        .filter(BillBook.create_time.month == datetime.now().month) \
        .order_by(BillBook.id) \
        .all()
    if len(bills) == 0:
        return ReplyConst.NO_DATA_REPLY
    return repr(bills)


def load_all(rec_msg):
    bills = BillBook.query \
        .filter_by(is_valid=1) \
        .filter_by(bill_keeper=rec_msg.from_user_name) \
        .order_by(BillBook.id) \
        .all()
    if len(bills) == 0:
        return ReplyConst.NO_DATA_REPLY
    return repr(bills)


def del_bill_by_id(rec_msg):
    try:
        bill_id = rec_msg.content.split(" ")[0]
        bill_id = int(bill_id)
    except ValueError:
        raise InvalidInputError
    bill = BillBook.query.get(bill_id)
    if bill.bill_keeper == rec_msg.from_user_name:
        bill.is_valid = 0
        db.session.commit()
        return ReplyConst.DEL_SUCCESS_REPLY
    else:
        raise ExceedAuthorityError


def insert_bill(rec_msg):
    try:
        bill_amount, bill_desc = rec_msg.content.split(" ")
        bill_amount = float(bill_amount)
    except ValueError:
        raise InvalidInputError
    bill = BillBook(rec_msg.from_user_name, bill_amount, bill_desc, 1, datetime.now(), datetime.now())
    db.session.add(bill)
    db.session.commit()
    return ReplyConst.INSERT_SUCCESS_REPLY
