from flask_appbuilder.api import BaseApi, expose

class ExampleApi(BaseApi):

    route_base = '/api/v2/example'

    @expose('/greeting')
    def greeting(self):
        return self.response(200, message="Hello")