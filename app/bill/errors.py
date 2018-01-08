class InvalidInputError(Exception):
    def __init__(self):
        self.value = "非法输入，请输入help查看帮助"

    def __str__(self):
        return repr(self.value)


class ExceedAuthorityError(Exception):
    def __init__(self):
        self.value = "无权操作"

    def __str__(self):
        return repr(self.value)
