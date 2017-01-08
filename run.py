from flask import Flask
from flask_restful import Resource, Api, reqparse

from crequest import RequestWithMsgPack
from cresponse import output_msgpack


class FlaskWithMsgPackRequest(Flask):
    """
    Extending on Flask to specify the usage of our custom Request class
    """
    request_class = RequestWithMsgPack


class FlaskRestfulWithMsgPackResponse(Api):
    """
    Extended Flask-RESTful to support the usage of our custom Response class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add msgpack support
        self.representations['application/msgpack'] = output_msgpack


app = FlaskWithMsgPackRequest(__name__)
api = FlaskRestfulWithMsgPackResponse(app)


class HelloMsgPack(Resource):
    """
    Class containing our endpoints
    """

    def get(self):
        return {'hello': 'You sent a GET request'}

    def post(self):
        parse = reqparse.RequestParser()
        # Important: define your 'location' to whatever function you
        # defined in your custom Request class
        parse.add_argument('data', location='msgpack', help='data in msgpack form', required=True)

        args = parse.parse_args()

        return {'Received data': args['data']}


api.add_resource(HelloMsgPack, '/')

if __name__ == "__main__":
    app.run(debug=False)
