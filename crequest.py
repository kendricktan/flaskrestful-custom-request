import msgpack
from flask import Request, _request_ctx_stack
from flask.wrappers import _get_data
from werkzeug.exceptions import BadRequest


class RequestWithMsgPack(Request):
    """
    Extending on Flask's Request class to support msgpack mimetype
    """

    @property
    def is_msgpack(self):
        """
        Checks if request is msgpack type or not.
        """
        mt = self.mimetype
        return mt.startswith('application/') and mt.endswith('msgpack')

    def msgpack(self, force=False, silent=False):
        """
        NOTE: This function name needs to be the same name specified on the
        'location' variable of the request parser. e.g.
        parser.add_argument('data', location='msgpack') `location needs to have the same
                                                        name as the callable function

        Parses the incoming request data and decodes it from msgpack to python
        __dict__ type. By default this function will return `None` if the mimetype
        is not `application/msgpack` but can be overridden by the ``force`` parameter.
        If parsing fails the

        :param force: if set to ``True`` the mimetype is ignored
        :param silent: if set to ``True`` this method will fail silently and return ``None``
        """
        if not (force or self.is_msgpack):
            return None

        request_charset = self.mimetype_params.get('charset', 'utf-8')

        try:
            data = _get_data(self, False)
            rv = msgpack.unpackb(data, encoding=request_charset)

        except ValueError as e:
            if silent:
                return None
            else:
                rv = self.on_msgpack_loading_failed(e)

        # Returns a converted dictionary (byte literal dict to unicode dict)
        # reason why this is done is because in Python3
        # my_dict[u'key'] is different to my_dict['key']
        return rv

    def on_msgpack_loading_failed(self, e):
        """
        Called if decoding of msgpack data failed
        """
        ctx = _request_ctx_stack.top

        if ctx is not None and ctx.app.config.get('DEBUG', False):
            raise BadRequest('Failed to decode msgpack object: {0}'.format(e))

        raise BadRequest()
