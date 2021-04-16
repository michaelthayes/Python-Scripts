# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:35:29 2021

@author: hayes
"""

# pulled from:
    # https://medium.com/koko-networks/automated-swagger-api-doc-with-flask-restful-a78119bc4473
    # https://github.com/anandtripathi5/flask-apispec-flask-restful/blob/master/app.py
# conda install -c anaconda flask-restful
# conda install -c conda-forge flask-apispec


from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs



flask_app = Flask(__name__)
# app = Api(app = flask_app, 
# 		  version = "1.0", 
# 		  title = "Name Recorder", 
# 		  description = "Manage names of various users of the application")
api = Api(flask_app)

flask_app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Name Recorder',
        description='Manage names of various users of the application',
        version='1.0',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
app = FlaskApiSpec(flask_app)
# app = Api(app=flask_app)


parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=True, help='id cannot be blank.')
parser.add_argument('name', type=str, required=True, help='Name cannot be blank.')



# class AwesomeResponseSchema(Schema):
#     message = fields.Str(default='Success')


class put_action(Schema):
    id = fields.Integer(required=True, description="API type of awesome API")
    name = fields.String(required=True, description="API type of awesome API")
    address = fields.String(required=True, description="API type of awesome API")
    
class get_action(Schema):
    id = fields.String(required=True, description="API type of awesome API")

# storage field
list_of_names = {}


#  Restful way of creating APIs through Flask Restful
class MainClass(MethodResource, Resource):

    @doc(description='My First GET Awesome API.', tags=['Name Model'])
    @use_kwargs(get_action, location=('json'))
    @marshal_with(get_action)  # marshalling
    def get(self, id):
        try:
            
            name = list_of_names[id]
            return {
				"status": "Person retrieved",
				"name" : list_of_names[id]
			}, 200
        except KeyError as e:
# 			name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
            abort(500, message='Could not retrieve information')
        except Exception as e:
# 			name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")
            abort(400, message='Could not retrieve information')

    @doc(description='My First POST Awesome API.', tags=['Name Model'])
    @use_kwargs(put_action, location=('json'))
    @marshal_with(put_action)  # marshalling
    def post(self):
        # try:
            # args = parser.parse_args()
            # list_of_names[args.id] = args.name
            return {
				'status': 'New person added',
				'name': 'Mike' #list_of_names[id]
 			}
#         except KeyError as e:
# # 			name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
#             abort(500, message='Could not retrieve information')
#         except Exception as e:
# # 			name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
#             abort(400, message='Could not retrieve information')

##
## Actually setup the Api resource routing here
##

api.add_resource(MainClass, '/')
app.register(MainClass)



if __name__ == '__main__':
    flask_app.run()