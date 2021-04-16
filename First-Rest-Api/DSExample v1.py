# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:35:29 2021

@author: hayes
"""

# pulled from https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f
# conda install -c anaconda flask
# conda install -c conda-forge flask-restplus



from flask import Flask, request
# from flask_restplus import Api, Resource, fields
try:
    from flask_restplus import Api, Resource, fields
except ImportError:
    import werkzeug
    werkzeug.cached_property = werkzeug.utils.cached_property
    from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "Name Recorder", 
		  description = "Manage names of various users of the application")

name_space = app.namespace('names', description='Manage names')

model = app.model('Name Model', 
		  {'name': fields.String(required = True, 
					 description="Name of the person", 
					 help="Name cannot be blank.")})


list_of_names = {}

@name_space.route("/<int:id>")
class MainClass(Resource):

	@app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Specify the Id associated with the person' })
	def get(self, id):
		try:
			name = list_of_names[id]
			return {
				"status": "Person retrieved",
				"name" : list_of_names[id]
			}
		except KeyError as e:
			name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
		except Exception as e:
			name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

	@app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Specify the Id associated with the person' })
	@app.expect(model)		
	def post(self, id):
		try:
			list_of_names[id] = request.json['name']
			return {
				"status": "New person added",
				"name": list_of_names[id]
			}
		except KeyError as e:
			name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
		except Exception as e:
			name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")

if __name__ == '__main__':
    flask_app.run()