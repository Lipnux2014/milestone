from flask import request, Blueprint
from app import db
from .consts import Commands, HELP_INFO, ReplyConst
from .models import BillBook
from .utils import parse_data, return_wrapper, joint_bill_info, convert_reply
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
    data = request.data
    if len(data) == 0:
        return ReplyConst.INVALID_PARAMETER_REPLY.value
    rec_msg = parse_data(data)
    try:
        if isinstance(rec_msg, Msg) and rec_msg.msg_type == 'text':
            if rec_msg.content.lower() == Commands.HELP.value:
                return load_help_info(rec_msg)
            if rec_msg.content.lower() == Commands.GET.value:
                return load_month(rec_msg)
            if rec_msg.content.lower() == Commands.GET_ALL.value:
                return load_all(rec_msg)
            if rec_msg.content.lower().startswith(Commands.DEL.value):
                return del_bill_by_id(rec_msg)
            else:
                return insert_bill(rec_msg)
        else:
            return ReplyConst.SILENCE_WX.value
    except InvalidInputError as e:
        return convert_reply(e.value, rec_msg)
    except ExceedAuthorityError as e:
        return convert_reply(e.value, rec_msg)
    except:
        return convert_reply(ReplyConst.UNKNOWN_ERROR_REPLY.value, rec_msg)


@return_wrapper
def load_help_info(rec_msg):
    print(rec_msg)
    return HELP_INFO


@return_wrapper
def load_month(rec_msg):
    now = datetime.now()
    bills = BillBook.query \
        .filter_by(is_valid=1) \
        .filter_by(bill_keeper=rec_msg.from_user_name) \
        .filter(BillBook.created_time >= str(datetime(now.year, now.month, 1))) \
        .order_by(BillBook.id) \
        .all()
    if len(bills) == 0:
        return ReplyConst.NO_DATA_REPLY.value
    return joint_bill_info(bills)


@return_wrapper
def load_all(rec_msg):
    bills = BillBook.query \
        .filter_by(is_valid=1) \
        .filter_by(bill_keeper=rec_msg.from_user_name) \
        .order_by(BillBook.id) \
        .all()
    if len(bills) == 0:
        return ReplyConst.NO_DATA_REPLY.value
    return joint_bill_info(bills)


@return_wrapper
def del_bill_by_id(rec_msg):
    try:
        bill_id = rec_msg.content.strip().split()[1]
        bill_id = int(bill_id)
    except ValueError:
        raise InvalidInputError
    bill = BillBook.query.get(bill_id)
    if bill.bill_keeper == rec_msg.from_user_name:
        bill.is_valid = 0
        db.session.commit()
        return ReplyConst.DEL_SUCCESS_REPLY.value
    else:
        raise ExceedAuthorityError


@return_wrapper
def insert_bill(rec_msg):
    try:
        bill_amount, bill_desc = rec_msg.content.split(" ")
        bill_amount = float(bill_amount)
    except ValueError:
        raise InvalidInputError
    try:
        bill = BillBook(rec_msg.from_user_name, bill_amount, bill_desc, 1, datetime.now(), datetime.now())
        db.session.add(bill)
        db.session.commit()
    except Exception as e:
        print(e)
        raise Exception
    return ReplyConst.INSERT_SUCCESS_REPLY.value
