# operation commands
from enum import Enum


class Commands(Enum):
    # 查看帮助
    HELP = "help"
    # 获取本月记账信息
    GET = "get"
    # 获取所有记账信息
    GET_ALL = "get all"
    # 删除指定记账信息
    DEL = "del"


HELP_INFO = """
    欢迎使用里程记账，你可以使用如下命令：
    1、 {金额} {描述} // 增加一条记账信息，如：27.5 午餐
    2、 get ： 查询本月记账信息
    3、 get all ： 查询所有记账信息
    4、 del {ID} : 删除指定ID的记账信息
"""


class ReplyConst(Enum):
    INSERT_SUCCESS_REPLY = "新增成功"
    DEL_SUCCESS_REPLY = "删除成功"
    SILENCE_WX = ""  # 在程序出错的情况下返回给wx，避免wx重复调用服务
    INVALID_PARAMETER_REPLY = "输入错误，请输入help查看使用方法"
    UNKNOWN_ERROR_REPLY = "操作失败，发生了未知错误"
    NO_DATA_REPLY = "无记账信息"
