import msgpack
from flask import make_response


def output_msgpack(data, code, headers=None):
    """
    msgpack Response

    For more info: http://flask-restful-cn.readthedocs.io/en/0.3.5/extending.html
    """
    resp = make_response(msgpack.packb(data, use_bin_type=True), code)
    resp.headers.extend(headers or {})
    return resp
