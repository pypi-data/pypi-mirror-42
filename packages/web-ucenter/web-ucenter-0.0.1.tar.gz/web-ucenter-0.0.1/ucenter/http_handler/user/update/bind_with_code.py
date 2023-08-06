import json

from tornado import gen

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler
from tweb import myweb
from tweb.error_exception import ErrException, ERROR
from ucenter.services import verify_code


class CodeBinding(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))

        user_id = self.request.headers.get('x-user-id')

        code_token = data.get('code_token')
        code = data.get('code')

        # 校验验证码，同时取出记录信息
        record = yield verify_code.verify_code(code_token, code)

        id_type = record.get('type')
        indicator = record.get('indicator')

        temp = yield ctrl_user.get(indicator)
        if temp is not None:
            # 手机或邮箱已被注册
            raise ErrException(ERROR.E40302, extra=indicator)

        user = yield ctrl_user.get(user_id)

        if id_type in user:
            raise ErrException(ERROR.E40303, extra=id_type)

        user = yield ctrl_user.bind(user_id, id_type, indicator)

        self.write({'user': user})
