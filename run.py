from app.view.view import api
from flask import Flask
#from werkzeug.contrib.fixers import ProxyFix

app=Flask(__name__)
app.secret_key='123456'
app.register_blueprint(api)

		
if __name__=='__main__':
	#app.wsgi_app = ProxyFix(app.wsgi_app)
	app.run(host='0.0.0.0',debug=True)