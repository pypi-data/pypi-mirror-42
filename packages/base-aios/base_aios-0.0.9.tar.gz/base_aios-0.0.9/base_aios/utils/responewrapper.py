from base_pkg_duke.utils.returncode import ReturnCode
class ResponeResult():
    """
    返回数据：
     对象：
       data={name:aaa,age:11}
     数组：
       data = [{name:aaa, age:111},{name:bbb, age:222}]
    """
    data = {}

    """
    返回码
    """
    code = None

    """
    返回信息内容
    """
    msg = ""

    """
    返回状态，是否成功，成功：True，失败：False
    """
    status = True

    '''初始化
    
    Returns:
        [type] -- [description]
    '''

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.data = kwargs.get("data", {})
        self.status = kwargs.get("status", True)
        self.msg = kwargs.get("msg")

    '''转成json
    
    Returns:
        [type] -- [description]
    '''

    def to_json(self):
        ret = {}
        ret["status"] = self.status
        ret["data"] = self.data
        ret["code"] = self.code
        ret["msg"] = self.msg
        return ret

    '''
     异常信息解析
    '''

    def res_exception(self, msg='', status=False, data=[], code=ReturnCode.FAILED):
        self.data = data
        self.code = code
        self.msg = str(msg)
        self.status = status

        return self.to_json()

    def res_success(self, msg='success', status=True, data=[], code=ReturnCode.SUCCESS):
        self.data = data
        self.code = code
        self.msg = msg
        self.status = status

        return self.to_json()

    def res_badrequest(self, msg='', status=False, data=[], code=ReturnCode.PARAMS_ERROR, field_name=''):

        msg_txt = msg if msg else 'required parameter \'{}\' is missing or invalidate.'.format(field_name)

        self.data = data
        self.code = code
        self.msg = msg_txt
        self.status = status

        return self.to_json()


class ResponePageResult(ResponeResult):
    curCount = 0
    totalCount = 0
    pageNO = 0
    pageSize = 0
    totalPage = 0
    nextPage = {}
    prePage = {}

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.data = kwargs.get("data")
        self.status = kwargs.get("status")
        self.msg = kwargs.get("msg")
        self.curCount = kwargs.get("curCount")
        self.totalCount = kwargs.get("totalCount")
        self.pageNO = kwargs.get("pageNO")
        self.pageSize = kwargs.get("pageSize")
        self.totalPage = kwargs.get("totalPage")
